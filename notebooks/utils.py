import asyncio
from typing import List
import aiohttp
import asyncio
import requests
import urllib.parse
import csv
import os


def get_lat_lon(addresses: List[str], verbose=False):
    once = False
    l = []
    for address in  addresses:
        # Example address = 'Shivaji Nagar, Bangalore, KA 560001'
        url = f"https://nominatim.openstreetmap.org/search.php?q={urllib.parse.quote(address)}&format=jsonv2"

        response = requests.get(url).json()
        lat_lon = (response[0]['lat'], response[0]['lon'])
        if verbose and not once:
            once = True
            print(f"Latitude: {response[0]['lat']} Longitude: {response[0]['lon']}")
        l.append(lat_lon)
    return l


async def fetch_lat_lon(session, address, semaphore):
    url = f"https://nominatim.openstreetmap.org/search.php?q={urllib.parse.quote(address)}&format=jsonv2"
    retry_delay = 1  # seconds to wait before retrying
    max_retries = 3  # maximum number of retries
    retries = 0

    while retries < max_retries:
        try:
            async with semaphore:
                async with session.get(url) as response:
                    response.raise_for_status()
                    json_response = await response.json()
                    return (address, (json_response[0]['lat'], json_response[0]['lon']))
        except aiohttp.ClientResponseError as e:
            if e.status == 429:  # HTTP status code for Too Many Requests
                retries += 1
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                return (address, e)
        except Exception as e:
            return (address, e)
    return (address, Exception("Max retries reached"))

async def aget_lat_lon(addresses, concurrency_limit=5):
    results = {}
    semaphore = asyncio.Semaphore(concurrency_limit)  # Limit the number of concurrent requests

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_lat_lon(session, address, semaphore) for address in addresses]
        for future in asyncio.as_completed(tasks):
            address, result = await future
            results[address] = result
    return results


cache_file = 'lat_lon_cache.csv'

# Function to read the cache from the CSV file
def read_cache():
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                address, lat, lon = row
                cache[address] = (lat, lon)
    return cache

# Function to write the cache to the CSV file
def write_cache(cache):
    with open(cache_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for address, lat_lon in cache.items():
            if isinstance(lat_lon, tuple):
                writer.writerow([address, lat_lon[0], lat_lon[1]])

# The main function that updates the cache and writes results
async def update_results_with_cache(addresses):
    # Read the existing cache
    cache = read_cache()
    # Get the results that are not in the cache
    new_addresses = [address for address in addresses if address not in cache]
    # Fetch the lat-lons for new addresses
    new_results = await aget_lat_lon(new_addresses)
    # Update the cache with new results
    cache.update(new_results)
    # Write the updated cache back to the CSV file
    write_cache(cache)
    return cache

if __name__ == '__main__':
    import pandas as pd

    df_dat = pd.read_csv("../data/01_interim/valuergeneral/001_SALES_DATA_NNME.csv")
    
    # csv is without index name
    df_dat.rename(columns={"Unnamed: 0": "index"}, inplace=True)
    def addressstr(df_dat, 
                   prop_cols = ["propertyUnitNumber", "propertyHouseNumber", "propertyStreetName", "propertyLocality", "propertyPostCode"]
                ) -> List[str]:
        """Create string address from address columns. Converts NaNs to blanks."""
        a = []
        for row in df_dat.loc[:,prop_cols].itertuples():
            address_template = ((f"U {str(row[1])}" if not pd.isna(row[1]) else "") \
                                + f"{str(row[2])} {row[3]} {row[4]}" + f" {str(int(row[5]))}" if not pd.isna(row[5]) else "")
            a.append(address_template)
        return a
    
    addresses = addressstr(df_dat)
    addresses = list(set(addresses))
    # Use the function to update the cache with new results
    lat_lons = asyncio.run(update_results_with_cache(addresses))
    for address, result in lat_lons.items():
        if isinstance(result, Exception):
            print(f"Error for {address}: {result}")
        else:
            print(f"Coordinates for {address}: {result}")