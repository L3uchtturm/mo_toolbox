from pathlib import Path

from geopandas import GeoSeries
from pandas import read_excel
from shapely import MultiPolygon, Polygon, GeometryCollection

from mo_toolbox.files import save_pickle, load_pickle


def flaechenkorr_utm_riliv(geometry: GeoSeries | MultiPolygon | Polygon | GeometryCollection, round_result: bool = True) -> int:
    """
    Anlage 1.1 RiLiV 2020_05

    """
    if isinstance(geometry, GeoSeries):
        centroid_x = geometry.centroid.iloc[0].x
    elif isinstance(geometry, (MultiPolygon, Polygon, GeometryCollection)):
        centroid_x = geometry.centroid.x
    else:
        raise ValueError(type(geometry), __name__)

    area = geometry.area
    massstabsfaktor: float = 0.9996
    mittl_kruemm_rad: float = 6381.8
    abstand_mittel_merid: float = (centroid_x - 32000000) / 10000
    reduced = area + (area / (massstabsfaktor**2) * (1-(massstabsfaktor**2) - (abstand_mittel_merid**2 / mittl_kruemm_rad**2)))
    return int(round(reduced)) if round_result else reduced


def import_gkverz_rlp() -> None:
    """AX73007"""
    #  Gemarkungsverzeichnis https://lvermgeo.rlp.de/fileadmin/lvermgeo/pdf/open-data/gkverz_rlp.xlsx
    file_path = Path().resolve()
    pkl_file = Path(fr'{file_path}\GKVERZ_RLP.pkl').resolve()

    if not pkl_file.exists():
        gkverz_rlp = read_excel(Path(fr'{file_path}\gkverz_rlp.xlsx').resolve(),
                                usecols='A,B,I,J',
                                converters={'07..': str, 'Gemarkung': str, 'Unnamed: 8': str, 'Grundbuchbezirk': str}
                                ).rename(
            columns={'07..': 'GKZ',
                     'Gemarkung': 'GEM_NAM',
                     'Unnamed: 8': 'BBB',
                     'Grundbuchbezirk': 'GBB_NAM'}
        )

        save_pickle(file_path=pkl_file, data=gkverz_rlp)

    return load_pickle(file_path=pkl_file)
