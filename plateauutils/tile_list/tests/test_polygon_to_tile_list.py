from plateauutils.tile_list.polygon_to_tile_list import (
    PolygonToTileList,
    _tile_list_range,
)
from shapely import from_wkt


def test_tile_list_range():
    assert _tile_list_range(0, 0, 0, 0, 0, ".mvt") == ["0/0/0.mvt"]
    assert sorted(_tile_list_range(58211, 25807, 58213, 25806, 16, ".mvt")) == sorted(
        [
            "16/58211/25807.mvt",
            "16/58211/25806.mvt",
            "16/58212/25807.mvt",
            "16/58212/25806.mvt",
            "16/58213/25807.mvt",
            "16/58213/25806.mvt",
        ]
    )


def test_polygon_to_tile_list():
    polygon = from_wkt(
        "POLYGON ((138.886414 35.719758, 139.465942 35.739825, 138.713379 35.250105, 138.886414 35.719758))"
    )
    zoom = 9
    tile_list = PolygonToTileList(polygon, zoom)
    assert sorted(tile_list.output()) == sorted(
        [
            "9/453/201.mvt",
            "9/454/201.mvt",
            "9/453/202.mvt",
        ]
    )

    polygon = from_wkt(
        "POLYGON ((139.759505 35.686546, 139.759462 35.685361, 139.769461 35.685326, 139.769526 35.678093, 139.759934 35.678111, 139.759912 35.676437, 139.771736 35.676524, 139.771564 35.686337, 139.759505 35.686546))"
    )
    zoom = 16
    tile_list = PolygonToTileList(polygon, zoom)
    assert sorted(tile_list.output()) == sorted(
        [
            "16/58210/25805.mvt",
            "16/58211/25805.mvt",
            "16/58212/25805.mvt",
            "16/58212/25806.mvt",
            "16/58210/25807.mvt",
            "16/58211/25807.mvt",
            "16/58212/25807.mvt",
        ]
    )
