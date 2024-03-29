from pathlib import Path
from plateauutils.flood_converter.flood_to_xyz import FloodToXyz
from pyproj import CRS
from py3dtiles.convert import convert as _convert
import tempfile


class FloodTo3dtiles:
    """洪水浸水域を3dtilesに変換するクラス"""

    def __init__(self):
        pass

    def convert(
        self,
        path: str = "",
        output_dir: str = "",
    ):
        """洪水浸水域を3dtilesに変換するメソッド

        Parameters
        ----------
        path : str
            npzファイルのベースパス
        output_dir : str
            3dtilesの出力先
        """
        # xyzファイルを作成
        xyz = FloodToXyz(path).parse()
        tmp = tempfile.mktemp(suffix=".csv")
        # 一時ファイルにxyzを書き込み
        with open(tmp, "w") as f:
            f.write(xyz)
        # py3dtilesで変換, crsは固定
        _convert(
            tmp,
            outfolder=output_dir,
            crs_in=CRS.from_epsg(4326),
            crs_out=CRS.from_epsg(4978),
        )
        # 一時ファイルを削除
        Path(tmp).unlink()
