from pathlib import Path

import pandas as pd

import geopandas as gpd

def project_to_from_cea(df: gpd.GeoDataFrame, column: str) -> gpd.GeoDataFrame:
    """Project coordinates to and from CEA, to account for shape of earth"""
    df.loc[:,column] = gpd.GeoSeries(df.loc[:,column].values.to_crs('+proj=cea'))
    return df

def add_geometry(data: pd.DataFrame, digital_boundaries: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    assert data.loc[:,'REGION'].dtype == 'int64', "REGION dtype must be int64"
    assert len(set(data.loc[:,'REGION_TYPE'].unique())) == 1, "One region code for this file"

    digital_boundaries = project_to_from_cea(digital_boundaries, 'geometry')
    region_code = data.loc[:,'REGION_TYPE'][0]

    # Cast data.REGION to the same type as digital_boundaries.REGION
    data.loc[:,'REGION'] = data.loc[:,'REGION'].astype(type(digital_boundaries.loc[:,f'{region_code}_CODE21'][0]))
    digital_boundaries = digital_boundaries[digital_boundaries.loc[:,f'{region_code}_CODE21'].isin(data.loc[:,'REGION'])]

    # Append geometry to data, using the SA2 code as the index on REGION
    data = gpd.GeoDataFrame(data)
    data = data.merge(digital_boundaries.loc[:,[f'{region_code}_CODE21', 'geometry', f'{region_code}_NAME21', 'STE_NAME21']], left_on='REGION', right_on=f'{region_code}_CODE21')
    return data

def variable_codes_to_names(data: pd.DataFrame, variable_mapping_path: Path, code_map = {}):
    import json

    # Load the JSON file
    with open(variable_mapping_path) as f:
        mapping = json.load(f)

    # Create a new column for gender description from the code
    # if name is not in the mapping, use a default value to replace it
    for code, name in code_map.items():
        data[name] = data[code].map(mapping[code]).fillna('NA')
    return data
    

DATA_DIR = (Path(__file__).parent.parent / "data" ).resolve()

if __name__ == '__main__':
    filepath = DATA_DIR / "00_raw" / "nationalmaps" / "Census_2021_G17_Total_personal_income_weekly_by_age_by_sex_Main_Statistical_Areas_Level_2_and_up_SA2_.txt"
                # data/00_raw/nationalmaps/Census_2021_G17_Total_personal_income_weekly_by_age_by_sex_Main_Statistical_Areas_Level_2_and_up_SA2_.txt
    metadata_filepath = DATA_DIR / "00_raw" / "nationalmaps" / "metadata"
    digital_boundaries_filepath = metadata_filepath / "SA2_2021_AUST_GDA2020.shp"
    variable_mapping_path = metadata_filepath / "variable_indices_mapping.json"
    save_path = DATA_DIR / "01_interim" / "nationalmaps" / "Census_2021_G17_Total_personal_income_weekly_by_age_by_sex_Main_Statistical_Areas_Level_2_and_up_SA2_.shp"


    data = pd.read_csv(filepath)
    digital_boundaries: gpd.GeoDataFrame = gpd.read_file(digital_boundaries_filepath)

    data = add_geometry(data, digital_boundaries)

    data = variable_codes_to_names(data, variable_mapping_path, {'SEXP': 'gender'})
    
    # Save geopandas
    for n in data.columns:
        if type(data[n][0]) != str and not n.startswith('geometry'):
            data[n] = data[n].astype(str)
            
    print(len(data.SA2_CODE21.unique()))
    data.to_file(save_path, driver='ESRI Shapefile', index=False)
