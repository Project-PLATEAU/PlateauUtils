from itertools import product
from plateauutils.abc.polygon_to_list import PolygonToList
from plateauutils.tile_list.geo_to_tile import (
    point_to_tile,
    tile_to_polygon,
)
from shapely.geometry import Polygon


class PolygonToTileList(PolygonToList):
    """Polygonからタイルのリストを返すクラス

    Parameters
    ----------
    polygon : shapely.geometry.Point
        対象となるポリゴン
    zoom : int
        ズームレベル
    ext : str, optional
        タイルの拡張子, by default ".mvt"
    """

    def __init__(self, polygon: Polygon, zoom: int, ext: str = ".mvt"):
        super().__init__(polygon)
        self.zoom = zoom
        self.ext = ext
        self.split()

    def split(self):
        """対象となるポリゴンを分割してタイルのリストを作成する"""
        start_tile = point_to_tile(self.start_pos, self.zoom)
        end_tile = point_to_tile(self.end_pos, self.zoom)
        _, start_x, start_y = start_tile.split("/")
        start_x = int(start_x)
        start_y = int(start_y.split(".")[0])
        _, end_x, end_y = end_tile.split("/")
        end_x = int(end_x)
        end_y = int(end_y.split(".")[0])
        self.targets = _tile_list_range(
            start_x, start_y, end_x, end_y, self.zoom, self.ext
        )

    def output(self) -> list:
        """タイルのリストを出力する

        Returns
        -------
        list
            タイルのリスト
        """
        output_list = []
        for i in self.targets:
            polygon = tile_to_polygon(i)
            # ポリゴンが交差しているかどうかを判定
            if self.polygon.intersects(polygon):
                output_list.append(i)
        return sorted(output_list)


def _tile_list_range(
    start_x: int, start_y: int, end_x: int, end_y: int, zoom: int, ext: str
) -> list:
    """タイルのリストを作成する

    Parameters
    ----------
    start_x : int
        開始x座標
    start_y : int
        開始y座標
    end_x : int
        終了x座標
    end_y : int
        終了y座標
    zoom : int
        ズームレベル
    ext : str
        タイルの拡張子

    Returns
    -------
    list
        タイルのリスト
    """
    matrix = []
    matrix.append(range(zoom, zoom + 1))
    matrix.append(range(start_x, end_x + 1))
    # y軸は上下逆(コンピュータ座標に合わせる)
    matrix.append(range(end_y, start_y + 1))
    combinations = product(*matrix)
    tile_base = ["/".join(map(str, i)) for i in combinations]
    return [i + ext for i in tile_base]
