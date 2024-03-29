import abc
import math
import numpy as np
import os
from plateauutils.abc.numpy_tile_parser import NumpyTileParser
import sys


class FloodToPng(NumpyTileParser):
    """洪水浸水域をpngに変換するクラス

    Parameters
    ----------
    path : str
        npzファイルのベースパス
    """

    def __init__(self, path: str = ""):
        super().__init__(path)

    def parse(self, output_dir: str = ""):
        """洪水浸水域をpngに変換するメソッド

        Parameters
        ----------
        output_dir : str
            pngの出力先
        """
        # lontitude, latitude, classificationsを取得
        lons, lats, _, classifications = self._parse_tile()
        # ズームレベル8から15までのpngを作成
        for zoom in range(8, 16):
            # storeを作成
            store = Store(zoom)
            # storeのaddメソッドをベクトル化
            vfunc = np.vectorize(store.add)
            # storeにlontitude, latitude, classificationsを追加
            vfunc(lons, lats, classifications)
            # pngを書き出す
            writer = PngWriter(output_dir, zoom)
            writer.setStore(store)
            writer.write()


class Store(object):
    """タイルの座標及び属性を保持するクラス"""

    def __init__(self, zoom):
        self.zoom = zoom
        self.storage = dict()

    def add(self, x, y, classification):
        """タイルの座標及び属性を格納するメソッド"""
        longitude, latitude = x, y
        # 座標からタイルの座標とタイル内の座標を取得
        x, y, pos_x, pos_y = self._coordinate_to_position(longitude, latitude)
        # storageに格納
        self._insert(x, y, pos_x, pos_y, classification)

    def _insert(self, x, y, pos_x, pos_y, classification):
        # keyがstorageに存在する場合はその値を取得
        key = (x, y)
        if key in self.storage.keys():
            array = self.storage[key]
        else:
            # 存在しない場合は256*256の配列を作成
            array = np.zeros((256, 256), dtype=np.int32)
            self.storage[key] = array
        # 属性を格納
        current = array[pos_x][pos_y]
        if current < classification:
            array[pos_x][pos_y] = classification
            self.storage[key] = array

    def _coordinate_to_position(self, longitude, latitude):
        """座標からタイルの座標とタイル内の座標を取得するメソッド"""
        # 座標からタイルのベースとなる座標を取得
        real_x = self._longitude_to_tile_with_decimal(longitude)
        real_y = self._latitude_to_tile_with_decimal(latitude)
        # タイル座標を取得
        x = math.floor(real_x)
        y = math.floor(real_y)
        # タイル内の座標を取得
        pos_x = math.floor((real_x - x) * 256)
        pos_y = math.floor((real_y - y) * 256)
        return x, y, pos_x, pos_y

    def _longitude_to_tile_with_decimal(self, longitude):
        # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
        return (longitude + 180) / 360 * math.pow(2, self.zoom)

    def _latitude_to_tile_with_decimal(self, latitude):
        # https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python
        return (
            (
                1
                - math.log(
                    math.tan(latitude * math.pi / 180)
                    + 1 / math.cos(latitude * math.pi / 180)
                )
                / math.pi
            )
            / 2
            * math.pow(2, self.zoom)
        )


class Writer(metaclass=abc.ABCMeta):
    """storeの内容を書き出す基底クラス

    出力する形式に応じて _write メソッドを実装する

    Parameters
    ----------
    directory : str
        出力先ディレクトリ
    zoom : int
        ズームレベル
    """

    def __init__(self, directory, zoom):
        self.directory = directory
        self.zoom = zoom

    def setStore(self, store):
        """storeをセットするメソッド"""
        self.store = store

    def write(self):
        """storeの内容を書き出すメソッド"""
        # storeの内容をタイルごとに書き出す
        for key in self.store.storage.keys():
            x = key[0]
            y = key[1]
            value = self.store.storage[key]
            # ディレクトリが無ければ作成する
            target_dir = os.path.join(self.directory, f"{self.zoom}/{x}")
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            # 書き出し
            self._write(x, y, value)

    @abc.abstractmethod
    def _write(self, x, y, value):
        raise NotImplementedError("_parse method is not implemented")


class PngWriter(Writer):
    def __init__(self, directory, zoom):
        super().__init__(directory, zoom)

    def _write(self, x, y, value):
        # Pillowをインポート、失敗したら終了
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("can't import PIL / Pillow, shutdown program")
            sys.exit(-1)
        # 属性をpngに変換
        dt = np.dtype(
            {
                "names": ["r", "g", "b", "a"],
                "formats": [np.uint8, np.uint8, np.uint8, np.uint8],
            }
        )
        converted1 = np.array(
            [tuple(self._classification_to_png(v)) for v in value.reshape(value.size)],
            dtype=dt,
        )
        converted2 = converted1.reshape(value.shape)
        filename = f"{self.directory}/{self.zoom}/{x}/{y}.png"
        width = 256
        img = Image.new("RGBA", (width, width), (128, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for i in range(0, width):
            for j in range(0, width):
                p = converted2[i][j]
                draw.point([(i, j)], (int(p[0]), int(p[1]), int(p[2]), int(p[3])))
        img.save(filename)

    def _classification_to_png(self, classification):
        # 属性をPNGのRGBに変換するメソッド
        # 内容が入っていなかったら透明色
        if classification == 0:
            return (0xFF, 0xFF, 0xFF, 0x00)
        # 属性に応じて色を変更
        if classification == 6:
            # 220 122 220
            return (0xDC, 0x7A, 0xDC, 0xFF)
        if classification == 5:
            # 242 133 201
            return (0xF2, 0x85, 0xC9, 0xFF)
        if classification == 4:
            # 255 145 145
            return (0xFF, 0x91, 0x91, 0xFF)
        if classification == 3:
            # 255 183 183
            return (0xFF, 0xB7, 0xB7, 0xFF)
        if classification == 2:
            # 255 216 192
            return (0xFF, 0xD8, 0xC0, 0xFF)
        if classification == 1:
            # 247 245 169
            return (0xF7, 0xF5, 0xA9, 0xFF)
        # 例外は透明色
        # 255 255 255
        return (0xFF, 0xFF, 0xFF, 0x00)
