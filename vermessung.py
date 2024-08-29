def flaechenkorr_utm_riliv(geometry: GeoSeries | MultiPolygon | Polygon | GeometryCollection) -> int:
    """
    Anlage 1.1 RiLiV 2020_05
    """
    if isinstance(geometry, GeoSeries):
        centroid_x = geometry.centroid.iloc[0].x
    elif isinstance(geometry, MultiPolygon) or isinstance(geometry, Polygon) or isinstance(geometry, GeometryCollection):
        centroid_x = geometry.centroid.x
    else:
        raise ValueError(type(geometry), __name__)

    area = geometry.area
    massstabsfaktor: float = 0.9996
    mittl_kruemm_rad: float = 6381.8
    abstand_mittel_merid: float = (centroid_x - 32000000) / 10000
    return int(round(area + (area / (massstabsfaktor**2) * (1-(massstabsfaktor**2) - (abstand_mittel_merid**2 / mittl_kruemm_rad**2)))))