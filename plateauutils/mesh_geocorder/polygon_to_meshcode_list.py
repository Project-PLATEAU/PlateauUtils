from itertools import product
from plateauutils.abc.polygon_to_list import PolygonToList
from plateauutils.mesh_geocorder.geo_to_mesh import (
    point_to_meshcode,
    meshcode_to_polygon,
)


class PolygonToMeshCodeList(PolygonToList):
    """Polygonからメッシュコードのリストを返すクラス

    Parameters
    ----------
    polygon : shapely.geometry.Polygon
        対象となるポリゴン
    mesh : str
        メッシュコードの粒度
    """

    def __init__(self, polygon, mesh="2"):
        super().__init__(polygon)
        self.mesh = mesh
        self.split()

    def split(self):
        """対象となるポリゴンを分割してメッシュコードのリストを作成する"""
        start_mesh = int(point_to_meshcode(self.start_pos, self.mesh))
        end_mesh = int(point_to_meshcode(self.end_pos, self.mesh))
        # メッシュを一旦3次メッシュの単位までにする
        if self.mesh == "2/1":
            start_mesh = int(start_mesh / 10)
            end_mesh = int(end_mesh / 10)
        elif self.mesh == "4/1":
            start_mesh = int(start_mesh / 100)
            end_mesh = int(end_mesh / 100)
        self.targets = _meshcode_range(start_mesh, end_mesh)
        # メッシュを元の粒度に戻す
        if self.mesh == "2/1":
            new_targets = []
            for i in self.targets:
                new_targets.append(i + "1")
                new_targets.append(i + "2")
                new_targets.append(i + "3")
                new_targets.append(i + "4")
            self.targets = new_targets
        elif self.mesh == "4/1":
            new_targets = []
            for i in self.targets:
                new_targets.append(i + "11")
                new_targets.append(i + "12")
                new_targets.append(i + "13")
                new_targets.append(i + "14")
                new_targets.append(i + "21")
                new_targets.append(i + "22")
                new_targets.append(i + "23")
                new_targets.append(i + "24")
                new_targets.append(i + "31")
                new_targets.append(i + "32")
                new_targets.append(i + "33")
                new_targets.append(i + "34")
                new_targets.append(i + "41")
                new_targets.append(i + "42")
                new_targets.append(i + "43")
                new_targets.append(i + "44")
            self.targets = new_targets

    def output(self) -> list:
        """メッシュコードのリストを出力する

        Returns
        -------
        list
            メッシュコードのリスト
        """
        output_list = []
        for i in self.targets:
            polygon = meshcode_to_polygon(i)
            # ポリゴンが交差しているかどうかを判定
            if self.polygon.intersects(polygon):
                output_list.append(i)
        return sorted(output_list)


def _meshcode_range(start_mesh: int, end_mesh: int) -> list:
    """メッシュコードの範囲を返す

    Parameters
    ----------
    start_mesh : int
        開始メッシュコード
    end_mesh : int
        終了メッシュコード

    Returns
    -------
    list
        メッシュコードのリスト
    """
    # start_pos = str(start_mesh)
    # end_pos = str(end_mesh)
    # print(start_pos, end_pos)
    # matrix = []
    # # 開始メッシュコードと終了メッシュコードの各桁の範囲をリストに格納
    # for i in range(len(start_pos)):
    #     if int(start_pos[i]) < int(end_pos[i]):
    #         matrix.append(range(int(start_pos[i]), int(end_pos[i]) + 1))
    #     else:
    #         matrix.append(range(0, 10))
    # # 全ての組み合わせを生成
    # combinations = product(*matrix)
    # # 各組み合わせを文字列として結合
    # return ["".join(map(str, combo)) for combo in combinations]
    combinations = range(start_mesh, end_mesh + 1)
    return [str(combo) for combo in combinations]
