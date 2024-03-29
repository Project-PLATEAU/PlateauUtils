# coding: utf-8

import math
from shapely.geometry import Point, Polygon


class MeshException(Exception):
    pass


class MeshCodeException(Exception):
    pass


def _validate_mesh(mesh: str) -> None:
    """メッシュのバリデーション"""
    if mesh not in ["1", "2", "2/1", "3", "4/1"]:
        raise MeshException("Mesh must be one of 1, 2, 2/1, 3, 4/1")


def point_to_meshcode(point: Point, mesh: str = "2") -> str:
    """緯度経度をメッシュコードに変換して返す

    Parameters
    ----------
    point : shapely.geometry.Point
        緯度経度を示すPointオブジェクト
    mesh : str, optional
        メッシュの種類, by default "2"

    Returns
    -------
    str
        メッシュコード
    """
    # メッシュのバリデーション
    _validate_mesh(mesh)

    # メッシュコードの初期化
    mesh_code = ""

    # 緯度経度の取得
    longitude = point.x
    latitude = point.y

    # https://qiita.com/yoshiyama_hana/items/8a9fc012cb02db7cbeb0
    # 1次メッシュ
    longitude_1st = int(longitude - 100)
    latitude_1st = int(math.floor(latitude * 60 / 40))
    mesh_code = f"{latitude_1st:02d}{longitude_1st:02d}"
    if mesh == "1":
        return mesh_code
    # 2次メッシュ
    longitude_2nd = int((longitude - math.floor(longitude)) * 60 / 7.5)
    latitude_2nd = int((latitude * 60) % 40 / 5)
    mesh_code = mesh_code + f"{latitude_2nd}{longitude_2nd}"
    if mesh == "2":
        return mesh_code

    # 3次メッシュ
    longitude_3rd = math.floor(
        ((longitude - math.floor(longitude)) * 60) % 7.5 * 60 / 45
    )
    latitude_3rd = int(math.floor(((latitude * 60) % 40) % 5 * 60 / 30))
    mesh_code = mesh_code + f"{latitude_3rd}{longitude_3rd}"
    if mesh == "3":
        return mesh_code

    # 2分の1メッシュ
    mesh_2nd1 = int(
        math.floor(((latitude * 60) % 40) % 5 * 60 % 30 / 15) * 2
        + math.floor(((longitude - math.floor(longitude)) * 60) % 7.5 * 60 % 45 / 22.5)
        + 1
    )
    mesh_code = mesh_code + f"{mesh_2nd1:01d}"
    if mesh == "2/1":
        return mesh_code

    # 4分の1メッシュ
    mesh_4th1 = int(
        math.floor(((latitude * 60) % 40) % 5 * 60 % 30 % 15 / 7.5) * 2
        + math.floor(
            ((longitude - math.floor(longitude)) * 60) % 7.5 * 60 % 45 % 22.5 / 11.25
        )
        + 1
    )

    mesh_code = mesh_code + f"{mesh_4th1}"
    if mesh == "4/1":
        return mesh_code


def meshcode_to_polygon(mesh_code: str) -> Polygon:
    """
    メッシュコードをポリゴンに変換して返す

    Parameters
    ----------
    mesh_code : str
        メッシュコード

    Returns
    -------
    shapely.geometry.Polygon
        メッシュコードに対応するポリゴン
    """
    if len(mesh_code) < 4:
        raise MeshCodeException("Mesh code must be 4 or more digits")
    if len(mesh_code) > 10:
        raise MeshCodeException("Mesh code must be 10 or less digits")
    if len(mesh_code) not in [4, 6, 8, 9, 10]:
        raise MeshCodeException("Mesh code must be 4, 6, 8, 9 or 10 digits")

    left_x = 0
    right_x = 0
    left_y = 0
    right_y = 0

    # 1次メッシュ
    mesh_y_1st = int(mesh_code[:2])
    mesh_x_1st = int(mesh_code[2:4])
    left_x = float(mesh_x_1st + 100)
    left_y = float(mesh_y_1st * 40 / 60)

    # 1次メッシュの場合
    if len(mesh_code) == 4:
        right_x = left_x + 1
        right_y = left_y + 1 * 40 / 60
        return _create_polygon(left_x, left_y, right_x, right_y)

    # 2次メッシュ
    mesh_y_2nd = int(mesh_code[4:5])
    mesh_x_2nd = int(mesh_code[5:6])
    left_x = left_x + mesh_x_2nd * 7.5 / 60
    left_y = left_y + mesh_y_2nd * 5 / 60

    # 2次メッシュの場合
    if len(mesh_code) == 6:
        right_x = left_x + (1 * 7.5 / 60)
        right_y = left_y + (1 * 5 / 60)
        return _create_polygon(left_x, left_y, right_x, right_y)

    # 3次メッシュ
    mesh_y_3rd = int(mesh_code[6:7])
    mesh_x_3rd = int(mesh_code[7:8])
    left_x = left_x + mesh_x_3rd * 45 / 60 / 60
    left_y = left_y + mesh_y_3rd * 30 / 60 / 60

    # 3次メッシュの場合
    if len(mesh_code) == 8:
        right_x = left_x + (1 * 45 / 60 / 60)
        right_y = left_y + (1 * 30 / 60 / 60)
        return _create_polygon(left_x, left_y, right_x, right_y)

    # 2分の1メッシュ
    mesh_2nd1 = int(mesh_code[8:9])
    if (mesh_2nd1 < 1) or (mesh_2nd1 > 4):
        raise MeshCodeException("2nd mesh must be 1 to 4")
    mesh_2nd1 = mesh_2nd1 - 1
    lon_section = mesh_2nd1 % 2
    min_lon_section = lon_section * 22.5 / 60
    max_lon_section = (lon_section + 1) * 22.5 / 60
    lat_section = mesh_2nd1 // 2
    min_lat_section = lat_section * 15 / 60
    max_lat_section = (lat_section + 1) * 15 / 60
    min_latitude = math.floor(min_lat_section / 60) + min_lat_section % 60 / 60
    max_latitude = math.floor(max_lat_section / 60) + max_lat_section % 60 / 60
    min_longitude = math.floor(min_lon_section / 60) + min_lon_section % 60 / 60
    max_longitude = math.floor(max_lon_section / 60) + max_lon_section % 60 / 60
    left_x = left_x + min_longitude
    left_y = left_y + min_latitude

    # 2分の1メッシュの場合
    if len(mesh_code) == 9:
        right_x = left_x + (max_longitude - min_longitude)
        right_y = left_y + (max_latitude - min_latitude)
        return _create_polygon(left_x, left_y, right_x, right_y)

    # 4分の1メッシュ
    mesh_4th1 = int(mesh_code[9:10])
    if (mesh_4th1 < 1) or (mesh_4th1 > 4):
        raise MeshCodeException("4th mesh must be 1 to 4")
    mesh_4th1 = mesh_4th1 - 1
    lon_section = mesh_4th1 % 2
    min_lon_section = lon_section * 11.25 / 60
    max_lon_section = (lon_section + 1) * 11.25 / 60
    lat_section = mesh_4th1 // 2
    min_lat_section = lat_section * 7.5 / 60
    max_lat_section = (lat_section + 1) * 7.5 / 60
    min_latitude = math.floor(min_lat_section / 60) + min_lat_section % 60 / 60
    max_latitude = math.floor(max_lat_section / 60) + max_lat_section % 60 / 60
    min_longitude = math.floor(min_lon_section / 60) + min_lon_section % 60 / 60
    max_longitude = math.floor(max_lon_section / 60) + max_lon_section % 60 / 60
    left_x = left_x + min_longitude
    left_y = left_y + min_latitude

    # 4分の1メッシュの場合
    if len(mesh_code) == 10:
        right_x = left_x + (max_longitude - min_longitude)
        right_y = left_y + (max_latitude - min_latitude)
        return _create_polygon(left_x, left_y, right_x, right_y)


def _create_polygon(
    left_x: float, left_y: float, right_x: float, right_y: float
) -> Polygon:
    """
    バウンディングボックスからポリゴンを作成して返す

    Parameters
    ----------
    left_x : float
        左のx座標
    left_y : float
        左のy座標
    right_x : float
        右のx座標
    right_y : float
        右のy座標

    Returns
    -------
    shapely.geometry.Polygon
        ポリゴン
    """
    coords = (
        (left_x, left_y),
        (right_x, left_y),
        (right_x, right_y),
        (left_x, right_y),
        (left_x, left_y),
    )
    return Polygon(coords)
