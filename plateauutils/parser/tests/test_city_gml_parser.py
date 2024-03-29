from plateauutils.parser.city_gml_parser import CityGMLParser
from shapely import from_wkt
import tempfile


def test_citygml_parser_v2():
    target_polygon = from_wkt(
        "POLYGON ((130.41249721501615 33.224722548534864, 130.41249721501615 33.22506264293093, 130.41621606802997 33.22506264293093, 130.41621606802997 33.224722548534864, 130.41249721501615 33.224722548534864))"
    )
    parser = CityGMLParser(target_polygon)
    with tempfile.TemporaryDirectory() as tmpdir:
        result = parser.download_and_parse(
            "https://file.smellman.org/test_citygml_v2.zip", tmpdir
        )
        assert len(result) == 3
        assert result[0]["gid"] == "bldg_383f1804-aa34-4634-949f-f769e09fa92d"
        assert result[0]["center"] == [130.41263587199947, 33.22489181671553]
        assert result[0]["min_height"] == 3.805999994277954
        assert result[0]["measured_height"] == 9.3
        assert result[0]["building_structure_type"] == "非木造"
        assert result[0]["usage"] == "運輸倉庫施設"


def test_citygml_parser_v1_4():
    target_polygon = from_wkt(
        "POLYGON ((130.41249721501615 33.224722548534864, 130.41249721501615 33.22506264293093, 130.41621606802997 33.22506264293093, 130.41621606802997 33.224722548534864, 130.41249721501615 33.224722548534864))"
    )
    parser = CityGMLParser(target_polygon)
    with tempfile.TemporaryDirectory() as tmpdir:
        result = parser.download_and_parse(
            "https://file.smellman.org/test_citygml_v1.4.zip", tmpdir
        )
        assert len(result) == 2
        assert result[0]["gid"] == "uuid_877DEA60-35D0-4FD9-8B02-852E39C75D81"
        assert result[0]["center"] == [130.41619367090038, 33.22492719812357]
        assert result[0]["min_height"] == 4.454999923706055
        assert result[0]["measured_height"] == 3.0
        assert result[0]["building_structure_type"] == "非木造"
        assert result[0]["usage"] == "共同住宅"
