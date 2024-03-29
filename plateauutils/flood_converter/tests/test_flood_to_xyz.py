from plateauutils.flood_converter.flood_to_png import FloodToPng

from pathlib import Path
from pytest import fixture
import shutil
from typing import Generator

DATA_DIRECTORY = Path(__file__).parent / "fixtures"


@fixture()
def tmp_dir() -> Generator[str, None, None]:
    yield Path("tmp/")
    shutil.rmtree("tmp/")


def test_convert(tmp_dir: str):
    flood_to_png = FloodToPng(str(DATA_DIRECTORY))
    flood_to_png.parse(output_dir=str(tmp_dir))
    assert Path(tmp_dir, "15/28264/13160.png").exists()
    assert Path(tmp_dir, "8/220/102.png").exists()
