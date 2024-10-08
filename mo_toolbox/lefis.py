import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from pandas import DataFrame, ExcelWriter

from mo_toolbox.debugging import timer


@dataclass
class AnredeVar:
    pers_anr: str
    var_weiblich: str
    var_maennlich: str
    var_gruppe: str
    var: dict[str, str] = field(init=False)

    """
    Wählt den richtigen Text anhand der Anrede
    pers_anr: str
    var_weiblich: str
    var_maennlich: str
    var_gruppe: str
    """
    def __post_init__(self):
        self.var = {
            '0': self.var_gruppe,
            'Sehr geehrte Damen und Herren': self.var_gruppe,
            '1000': self.var_weiblich,
            'Sehr geehrte Frau': self.var_weiblich,
            '2000': self.var_maennlich,
            'Sehr geehrter Herr': self.var_maennlich,
            '3000': self.var_maennlich
        }

    def rv(self) -> str:
        """return value"""
        return self.var[self.pers_anr] if self.pers_anr else f'{self.var_weiblich} / {self.var_maennlich} / {self.var_gruppe}'


@dataclass
class FlstVar:
    anz_flst: int
    var_single: str
    var_multiple: str

    def rv(self):
        """return value"""
        return self.var_single if self.anz_flst == 1 else self.var_multiple


def decode_uuids(internal_uuid: str) -> str:
    return uuid.UUID(internal_uuid[1:]).bytes.decode()


def excel_export(df_ausgabe: DataFrame,
                 doc_name: str,
                 vnr: str,
                 output_dir: str | Path,
                 index: bool = False,
                 float_format='%.2f',
                 date_format: str = "%d%m%y_%H%M%S"
                 ) -> None:

    filename = fr'{output_dir}\{doc_name}_{vnr}_{datetime.now().strftime(date_format)}{"_LEER" if df_ausgabe.empty else ""}.xlsx'
    sheet_name = f'{doc_name}_{vnr}'

    if not output_dir.exists():
        output_dir.mkdir()

    # https://stackoverflow.com/a/72464621
    with ExcelWriter(path=filename, engine='xlsxwriter') as writer:
        df_ausgabe.to_excel(writer, sheet_name=sheet_name, index=index, float_format=float_format)
        try:
            for column in df_ausgabe:
                column_length = max(df_ausgabe[column].astype(str).map(len).max(), len(column)) + 4
                col_idx = df_ausgabe.columns.get_loc(column)
                writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

        except ValueError:
            pass
    timer(fr'Erzeuge {filename}')


def convert_uuid_in_df(df: DataFrame, fields: list) -> DataFrame:
    df_mod = df.copy()
    for value in fields:
        df_mod[value] = df[value].map(decode_uuids)
    return df_mod


def obsolete_projekte(year: int, month: int, day: int, amt: str) -> None:
    simmern = Path(r"\\AV-RLP\.si-fcl1_EXT22.si.dlr\lefis\LEFIS_Projekte")
    kreuznach = Path(r"O:\LEFIS_Projekte")
    amt = kreuznach if amt == "kh" else simmern if amt == "si" else Path()

    if amt.exists():
        counter = 0
        for verfahren in amt.iterdir():
            if verfahren.parts[-1].__contains__('VNR'):
                projektordner = verfahren / 'Projekte'
                projekte = projektordner.iterdir()
                if projektordner.exists() and any(projekte):
                    for file in projekte:
                        if ((not (
                                re.findall(pattern='(..)nderungsdienst', string=str(file))
                                or re.findall(pattern='(.)orplanung', string=str(file))
                                or re.findall(pattern='(.)ueffeld', string=str(file))
                                or re.findall(pattern='pompe', string=str(file))))
                                and datetime.fromtimestamp(file.stat().st_mtime) < datetime.strptime(f'{year}{month}{day}', "%Y%m%d")):
                            print(file)
                            counter += 1
        print(f"Obsolete Projekte: {counter}")
    else:
        print(f"{amt} nicht erreichbar")