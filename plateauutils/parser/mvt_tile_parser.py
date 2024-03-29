import glob
import os
from plateauutils.abc.plateau_parser import PlateauParser
from plateauutils.tile_list.polygon_to_tile_list import PolygonToTileList
from shapely.geometry import Polygon
import shutil
import zipfile


class MvtTileParser(PlateauParser):
    """MVTタイルをパースするクラス

    Parameters
    ----------
    polygon : shapely.geometry.Polygon
        対象となるポリゴン
    zoom : int
        対象とするズームレベル
    """

    def __init__(self, polygon: Polygon = None, zoom: int = 15):
        self.zoom = zoom
        super().__init__(polygon)

    def parse(self, target_path: str = "") -> list:
        """MVTタイルをパースして、リストを返すメソッド

        Parameters
        ----------
        target_path : str
            MVTタイル(zip)のパス

        Returns
        -------
        list
            タイルのパスのリスト
        """
        # ファイルが存在しないならエラー
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"target_path: {target_path} is not found")
        # zipファイルにターゲットのパスが存在するか確認
        hit_targets = []
        with zipfile.ZipFile(target_path) as zip_file:
            for name in zip_file.namelist():
                for target in self.targets:
                    path = os.path.join("luse", target)
                    if name.find(path) >= 0:
                        hit_targets.append(target)
        if len(hit_targets) == 0:
            raise ValueError(f"target_path: {target_path} is not target")
        # zipファイルを解凍する
        unarchived_dir = target_path.replace(".zip", "")
        shutil.unpack_archive(target_path, unarchived_dir)
        # 返り値を作成
        return_list = []
        # 解凍したファイルをパースする
        for target in hit_targets:
            # ファイルパスを作成
            target_file_path = os.path.join(unarchived_dir, "luse", target)
            for file_path in glob.glob(target_file_path):
                return_list.append(file_path)
        return sorted(return_list)

    def download_and_parse(self, url: str = "", target_dir: str = "") -> list:
        """MVTタイルをダウンロードして、タイルのリストを返すメソッド

        Parameters
        ----------
        url : str
            MVTタイル(zip)のURL
        target_dir : str
            ファイルを展開する先のパス

        Returns
        -------
        list
            タイルのパスのリスト
        """
        saved_path = self._download(url, target_dir)
        return self.parse(saved_path)

    def _target_list(self, polygon: Polygon = None) -> list:
        # PolygonがNoneならエラー
        if polygon is None:
            raise ValueError("polygon is None")
        # Polygonからタイルのリストを作成
        tile_list = PolygonToTileList(polygon, self.zoom)
        return tile_list.output()
