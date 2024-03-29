import abc
from shapely.geometry import Polygon, Point


class PolygonToList(metaclass=abc.ABCMeta):
    """Polygonからリストを返すクラスの抽象クラス

    Parameters
    ----------
    polygon : shapely.geometry.Polygon
        対象となるポリゴン
    """

    def __init__(self, polygon: Polygon):
        self.polygon = polygon
        self.bounds = self.polygon.bounds
        self.start_pos = Point(self.bounds[0], self.bounds[1])
        self.end_pos = Point(self.bounds[2], self.bounds[3])
        self.targets = []

    @abc.abstractmethod
    def split(self):
        """対象となるポリゴンを分割してリストを作成する"""
        raise NotImplementedError("split method is not implemented")

    @abc.abstractmethod
    def output(self) -> list:
        """リストを出力する

        Returns
        -------
        list
            リスト
        """
        raise NotImplementedError("output method is not implemented")
