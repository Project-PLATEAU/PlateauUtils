import abc
from os.path import exists, join
import numpy as np
import requests
from shapely.geometry import Polygon
from tqdm import tqdm


class PlateauParser(metaclass=abc.ABCMeta):
    def __init__(self, polygon: Polygon = None):
        self.targets = self._target_list(polygon)
        self.polygon = polygon

    @abc.abstractmethod
    def parse(self, target_path: str = ""):
        raise NotImplementedError("parse method is not implemented")

    @abc.abstractmethod
    def download_and_parse(self, url: str = "", target_dir: str = ""):
        raise NotImplementedError("download_and_parse method is not implemented")

    @abc.abstractmethod
    def _target_list(self, polygon: Polygon = None) -> list:
        raise NotImplementedError("_target_list method is not implemented")

    def _download(self, url: str = "", target_dir: str = "") -> str:
        # ダウンロードパスが無ければエラー
        if not exists(target_dir):
            raise FileNotFoundError(f"{target_dir} does not exist.")
        # ファイル名を取得
        filename = url.split("/")[-1]
        # 保存先パスを作成
        saved_path = join(target_dir, filename)
        # 保存パスにファイルが存在すれば、そのパスを返す
        if exists(saved_path):
            return saved_path
        # 進捗を表示するため、ストリームでダウンロード
        response = requests.get(url, stream=True)
        # レスポンスが200ならダウンロード
        if response.status_code == 200:
            # ファイルサイズを取得
            total_size = int(response.headers.get("content-length", 0))
            # 1 Kibibyte
            block_size = 1024
            # 進捗表示
            t = tqdm(total=total_size, unit="iB", unit_scale=True)
            with open(saved_path, "wb") as f:
                for data in response.iter_content(block_size):
                    # 進捗を更新
                    t.update(len(data))
                    # ファイルに書き込み
                    f.write(data)
            # 進捗表示を閉じる
            t.close()
            # サイズを確認、問題があればエラー
            if total_size != 0 and t.n != total_size:
                raise ConnectionError("ERROR, something went wrong")
        else:
            raise ConnectionError(f"Cannot download {url}")
        return saved_path
