import os
from plateauutils.parser.mvt_tile_parser import MvtTileParser
from shapely import from_wkt
import tempfile


def test_mvt_tile_parser_z15():
    test_polygon = from_wkt(
        "POLYGON ((130.525689 33.323966, 130.522728 33.314069, 130.511441 33.308653, 130.501013 33.30937, 130.492516 33.318516, 130.493717 33.325831, 130.504618 33.332249, 130.512857 33.332213, 130.525689 33.323966))"
    )
    parser = MvtTileParser(test_polygon, 15)
    with tempfile.TemporaryDirectory() as tmpdir:
        result = parser.download_and_parse(
            "https://file.smellman.org/test_mvt_list.zip", tmpdir
        )
        assert len(result) == 13
        assert result[0] == os.path.join(
            tmpdir, "test_mvt_list/luse/15/28261/13163.mvt"
        )
        assert result[12] == os.path.join(
            tmpdir, "test_mvt_list/luse/15/28264/13165.mvt"
        )


def test_mvt_tile_parser_z14():
    test_polygon = from_wkt(
        "POLYGON ((130.525689 33.323966, 130.522728 33.314069, 130.511441 33.308653, 130.501013 33.30937, 130.492516 33.318516, 130.493717 33.325831, 130.504618 33.332249, 130.512857 33.332213, 130.525689 33.323966))"
    )
    parser = MvtTileParser(test_polygon, 14)
    with tempfile.TemporaryDirectory() as tmpdir:
        result = parser.download_and_parse(
            "https://file.smellman.org/test_mvt_list.zip", tmpdir
        )
        assert len(result) == 6
        assert result[0] == os.path.join(tmpdir, "test_mvt_list/luse/14/14130/6581.mvt")
        assert result[5] == os.path.join(tmpdir, "test_mvt_list/luse/14/14132/6582.mvt")
