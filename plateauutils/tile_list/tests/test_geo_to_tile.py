import pytest
from shapely.geometry import Polygon, Point


def test_point_to_tile():
    from plateauutils.tile_list.geo_to_tile import point_to_tile

    point = Point(139.767125, 35.681236)
    zoom = 16
    tile_path = point_to_tile(point, zoom)
    assert tile_path == "16/58211/25806.mvt"

    zoom = 0
    tile_path = point_to_tile(point, zoom)
    assert tile_path == "0/0/0.mvt"


def test_tile_to_polygon():
    from plateauutils.tile_list.geo_to_tile import tile_to_polygon

    tile_path = "16/58211/25806.mvt"
    polygon = tile_to_polygon(tile_path)
    assert (
        polygon.wkt
        == "POLYGON ((139.7625732421875 35.68407153314097, 139.76806640625 35.68407153314097, 139.76806640625 35.679609609368576, 139.7625732421875 35.679609609368576, 139.7625732421875 35.68407153314097))"
    )

    tile_path = "0/0/0.mvt"
    polygon = tile_to_polygon(tile_path)
    assert (
        polygon.wkt
        == "POLYGON ((-180 85.0511287798066, 180 85.0511287798066, 180 -85.0511287798066, -180 -85.0511287798066, -180 85.0511287798066))"
    )


def test_invalid_tile_to_polygon():
    from plateauutils.tile_list.geo_to_tile import tile_to_polygon, TileRangeException

    tile_path = "-1/0/0.mvt"
    with pytest.raises(TileRangeException) as e:
        tile_to_polygon(tile_path)
    assert str(e.value) == "Tile range must be positive integer"

    tile_path = "1/2/0.mvt"
    with pytest.raises(TileRangeException) as e:
        tile_to_polygon(tile_path)
    assert str(e.value) == "Tile range must be less than 2"
