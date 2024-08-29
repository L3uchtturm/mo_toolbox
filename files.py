def dataframe_to_excel(dataframe: GeoDataFrame | pandas.DataFrame, name: str, export_path: str = None) -> None:
    dataframe.to_csv(fr'{export_path + "/" + name if export_path else name}.csv')

def save_pickle(file: str | Path, data) -> None:
    try:
        x = open(file, 'w+')
        x.close()
    finally:
        with open(file, 'wb') as l_obj:
            pickle.dump(data, l_obj)


def load_pickle(file:  str | Path) -> Any:
    try:
        with open(file, 'rb') as l_obj:
            return pickle.load(l_obj)
    except FileNotFoundError:
        logger.exception(f'{FileNotFoundError} {file}')


def open_json(path: Path | str) -> dict | list:
    if path.exists():
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return json.loads('{}')


def save_json(file_name: str | Path, items: list | dict) -> json:
    with open(fr"{file_name}.json", "w+", encoding='utf-8') as file:
        json.dump(items, file,  indent=4, ensure_ascii=True)

def open_config(config_path: str | Path) -> ConfigParser:
    config = ConfigParser()
    config.read_file(open(Path(config_path).resolve()))
    return config