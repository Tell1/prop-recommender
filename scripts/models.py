from pathlib import Path
from typing import Protocol, Union

import numpy as np
import pandas as pd
import yaml

MODEL_CONFIG_DIR = Path(__file__).parent.parent / "models"


class Predictor(Protocol):
    def predict(self, X):
        ...

def train( config: dict, dataset: pd.DataFrame ) -> Predictor:
    """
    Train a predictor using the given configuration and dataset.

    Parameters:
        config (dict): A dictionary containing the configuration for training the predictor.
        dataset (pd.DataFrame): A pandas DataFrame containing the dataset for training the predictor.

    Returns:
        Predictor: A trained Predictor object.
    """
    
    y = dataset[config['dataset']['target_name']]
    if config['dataset']['feature_names']:
        X = dataset[config['dataset']['feature_names']]
    else:
        X = dataset[[col for col in dataset.columns if col != y.name]]
        config['dataset']['feature_names'] = X.columns

    if config['name'] == 'ridgereg':
        return _train_ridge_regression(X, y, config)
    
    raise NotImplementedError(f"Unknown model: {config['name']=}")
    


def _load_config(config_name: Union[str, Path]) -> dict:
    """
    Load a configuration .yaml file from `MODEL_CONFIG_DIR` and return its contents as a dictionary.

    Parameters:
        config_name (Union[str, Path]): The name or path of the configuration file.

    Returns:
        dict: The contents of the configuration file as a dictionary.
    """
    
    if Path(config_name).exists():
        config_path = Path(config_name)
    else:
        config_path = Path(__file__).parent / MODEL_CONFIG_DIR / config_name
        
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    config['name'] = config_path.stem
    return config


def _train_ridge_regression(X, y, config) -> Predictor:
    _min, _max, _num = config['alphas'].split(',')
    alphas = np.logspace(float(_min), float(_max), num=int(_num))
        
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import GridSearchCV

    # Create a Ridge regression model
    ridge = Ridge()

    # Create a Pipeline with StandardScaler and Ridge
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('ridge', ridge)
    ])

    # Set up the parameter grid for GridSearchCV
    param_grid = {'ridge__alpha': alphas}

    # Perform cross-validation with GridSearchCV
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)  # Use 5-fold cross-validation
    grid_search.fit(X, y)

    # Get the best model
    best_ridge_model = grid_search.best_estimator_

    # Get the best alpha value
    best_alpha = grid_search.best_params_['ridge__alpha']

    # Print the best alpha value and the best model
    print(f"The best alpha value is: {best_alpha}")
    print(f"The best Ridge model is: {best_ridge_model}")
    
    class Model:
        
        def __init__(self, model):
            self.model = model
            
        def predict(self, X):
            return self.model.predict(X)

    model = Model(model=best_ridge_model)
    
    return model


if __name__ == "__main__":
    
    config = _load_config("ridgereg.yaml")
    datapath = MODEL_CONFIG_DIR.parent / "data" / "00_raw" / "cali-housing" / "cali-housing.csv"
    df = pd.read_csv(datapath)
    
    model = train(config, df)
    y_hat = model.predict(df[config['dataset']['feature_names']])
    print(y_hat)
