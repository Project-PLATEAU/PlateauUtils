import math
from shapely.geometry import Point, Polygon


def _deg2num(lat_deg, lon_deg, zoom):
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def _num2deg(xtile, ytile, zoom):
    # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
    n = 1 << zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


class TileRangeException(Exception):
    pass


def point_to_tile(point: Point, zoom: int, ext: str = ".mvt") -> str:
    """緯度経度をタイルに変換して返す

    Parameters
    ----------
    point : shapely.geometry.Point
        緯度経度を示すPointオブジェクト
    zoom : int
        ズームレベル
    ext : str, optional
        タイルの拡張子, by default ".mvt"

    Returns
    -------
    str
        タイルのパス
    """
    # 緯度経度の取得
    longitude = point.x
    latitude = point.y

    # タイルの取得
    xtile, ytile = _deg2num(latitude, longitude, zoom)

    return f"{zoom}/{xtile}/{ytile}{ext}"


def tile_to_polygon(tile_path: str) -> Polygon:
    """
    タイルのパスをポリゴンに変換して返す

    Parameters
    ----------
    tile_path : str
        タイルのパス

    Returns
    -------
    shapely.geometry.Polygon
        タイルのパスに対応するポリゴン
    """

    # タイルのパスからタイルの座標を取得
    zoom, xtile, ytile = tile_path.split("/")[:3]
    zoom = int(zoom)
    xtile = int(xtile)
    ytile = int(ytile.split(".")[0])
    if zoom < 0 or xtile < 0 or ytile < 0:
        raise TileRangeException("Tile range must be positive integer")
    max_tile = 2**zoom
    if xtile >= max_tile or ytile >= max_tile:
        raise TileRangeException(f"Tile range must be less than {max_tile}")

    # タイルの座標から緯度経度を取得
    from_latitude, from_longitude = _num2deg(xtile, ytile, zoom)
    to_latitude, to_longitude = _num2deg(xtile + 1, ytile + 1, zoom)

    coords = (
        (from_longitude, from_latitude),
        (to_longitude, from_latitude),
        (to_longitude, to_latitude),
        (from_longitude, to_latitude),
        (from_longitude, from_latitude),
    )
    return Polygon(coords)
