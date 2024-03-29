import numpy as np
import pandas as pd
from plateauutils.abc.numpy_tile_parser import NumpyTileParser


class FloodToXyz(NumpyTileParser):
    """洪水浸水域をxyzに変換するクラス

    Parameters
    ----------
    path : str
        npzファイルのベースパス
    """

    def __init__(self, path: str = ""):
        super().__init__(path)

    def parse(self):
        """洪水浸水域をxyzに変換するメソッド"""
        lons, lats, dems, classifications = self._parse_tile()
        # IRGB値を作成
        i_values = np.ones_like(dems, dtype=np.int32) * 1
        r_values = np.ones_like(dems, dtype=np.int32) * 0
        g_values = np.ones_like(dems, dtype=np.int32) * 191
        b_values = np.ones_like(dems, dtype=np.int32) * 255
        # xyzファイルを作成, 並びはlatitude, longitude, altitude, i, r, g, b, classification
        df = pd.DataFrame(
            {
                "lat": lats,
                "lon": lons,
                "dem": dems,
                "i": i_values,
                "r": r_values,
                "g": g_values,
                "b": b_values,
                "classification": classifications,
            }
        )
        return df.to_csv(index=False, header=True, sep=" ")
