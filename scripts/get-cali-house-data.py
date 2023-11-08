"""
Script to download California housing data, and save to data/00_raw/cali-housing

>>> python scripts/get-cali-house-data.py

"""

from operator import index
from pathlib import Path

# Get directoroy structure expected of this repo
root_dir = Path(".").parent.parent
raw_data_dir = root_dir / "data" / "00_raw"

dataset_name = "cali-housing"
dataset_path = raw_data_dir / dataset_name / "cali-housing.csv"

if dataset_path.exists():
    print(f"{dataset_name} already exists at: {str(dataset_path.resolve())}. But meta.")        
    exit()

dataset_path.parent.mkdir(parents=True, exist_ok=True)

# Sometimes errors with dataset downloads. Bug fix: https://github.com/pytorch/vision/issues/1938#issuecomment-594623431
from six.moves import urllib

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

from sklearn.datasets import fetch_california_housing

california_housing = fetch_california_housing(as_frame=True)


california_housing.frame.to_csv(raw_data_dir / dataset_name / "cali-housing.csv",
                                index=False)
print(f"Saved {dataset_name} at: {str(dataset_path.resolve())}.")
