import json
import pickle
from configparser import ConfigParser
from pathlib import Path
from typing import Any

from pandas import DataFrame
from geopandas import GeoDataFrame


#  Pandas / GeoPandas

def df_to_csv(df: GeoDataFrame | DataFrame, name: str, export_path: str | Path = None) -> None:
    """
    Creates a cvs file from a (Geo)DataFrame
    """
    df.to_csv(fr'{export_path + "/" + name if export_path else name}.csv')


#  Pickle

def save_pickle(file_path: str | Path, data: Any) -> None:
    """
    Saves Data a pickle File
    """
    try:
        file = open(file_path, 'w+')
        file.close()
    finally:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)


def load_pickle(file_path:  str | Path) -> Any:
    """
    opens a pickle file
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)


#  json
def save_json(file_name: str | Path, items: list | dict) -> json:
    """
    Saves Data to a json file
    """
    with open(fr"{file_name}.json", "w+", encoding='utf-8') as file:
        json.dump(items, file,  indent=4, ensure_ascii=True)


def load_json(file_path: Path | str) -> dict | list:
    """
    opens a json file is existing, else creating an empty one
    """
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return json.loads('{}')


#  config
def open_config(config_path: str | Path) -> ConfigParser:
    """
    returns a configparser from a .ini file
    """
    config = ConfigParser()
    config.read_file(open(Path(config_path).resolve()))
    return config
