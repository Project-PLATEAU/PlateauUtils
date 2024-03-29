import abc
import glob
import numpy as np
import os


class NumpyTileParser(metaclass=abc.ABCMeta):
    def __init__(self, path: str = ""):
        self.path = path

    @abc.abstractmethod
    def parse(self):
        raise NotImplementedError("parse method is not implemented")

    def _parse_tile(self):
        """タイルをパースするメソッド"""
        tile_list = self.__make_tile_list()
        lons = []  # 経度
        lats = []  # 緯度
        dems = []  # 標高
        classifications = []  # 属性値
        # それぞれのタイルをパース
        for tile in tile_list:
            t = np.load(tile)
            lons.append(t["lons"])
            lats.append(t["lats"])
            dems.append(t["dem"])
            classifications.append(t["classification"])
        # np.arrayに変換
        np_lons, np_lats, np_dems, np_classifications = (
            np.concatenate(lons),
            np.concatenate(lats),
            np.concatenate(dems),
            np.concatenate(classifications),
        )
        # nanを除去
        np_lons = np_lons[~np.isnan(np_dems)]
        np_lats = np_lats[~np.isnan(np_dems)]
        np_classifications = np_classifications[~np.isnan(np_dems)]
        np_dems = np_dems[~np.isnan(np_dems)]
        return np_lons, np_lats, np_dems, np_classifications

    def __make_tile_list(self):
        """タイルのリストを作成するメソッド"""
        return glob.glob(os.path.join(self.path, "**", "*.npz"), recursive=True)
