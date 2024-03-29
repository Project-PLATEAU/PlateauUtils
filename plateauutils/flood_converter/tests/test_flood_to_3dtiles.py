from plateauutils.flood_converter.flood_to_3dtiles import FloodTo3dtiles

from py3dtiles.tileset import number_of_points_in_tileset

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
    flood_to_3dtiles = FloodTo3dtiles()
    flood_to_3dtiles.convert(path=str(DATA_DIRECTORY), output_dir=str(tmp_dir))
    assert Path(tmp_dir, "tileset.json").exists()
    assert Path(tmp_dir, "r.pnts").exists()
    tileset_path = tmp_dir / "tileset.json"
    assert 62615 == number_of_points_in_tileset(tileset_path)
