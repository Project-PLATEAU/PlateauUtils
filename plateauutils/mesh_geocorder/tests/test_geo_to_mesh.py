import pytest
from shapely.geometry import Point


def test_invalid_mesh():
    """メッシュコードが不正な場合のテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import MeshException, _validate_mesh

    with pytest.raises(MeshException) as e:
        _validate_mesh("5")
    assert str(e.value) == "Mesh must be one of 1, 2, 2/1, 3, 4/1"


def test_point_to_mesh():
    """緯度経度をメッシュコードに変換するテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import point_to_meshcode

    point = Point(139.71475, 35.70078)
    mesh_code = point_to_meshcode(point, "1")
    assert mesh_code == "5339"

    mesh_code = point_to_meshcode(point, "2")
    assert mesh_code == "533945"

    mesh_code = point_to_meshcode(point, "3")
    assert mesh_code == "53394547"

    mesh_code = point_to_meshcode(point, "2/1")
    assert mesh_code == "533945471"

    mesh_code = point_to_meshcode(point, "4/1")
    assert mesh_code == "5339454711"


def test_invalid_mesh_code_to_polygon():
    """メッシュコードが不正な場合のテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import (
        MeshCodeException,
        meshcode_to_polygon,
    )

    with pytest.raises(MeshCodeException) as e:
        meshcode_to_polygon("0")
    assert str(e.value) == "Mesh code must be 4 or more digits"

    with pytest.raises(MeshCodeException) as e:
        meshcode_to_polygon("53394547141")
    assert str(e.value) == "Mesh code must be 10 or less digits"

    with pytest.raises(MeshCodeException) as e:
        meshcode_to_polygon("533945475")
    assert str(e.value) == "2nd mesh must be 1 to 4"

    with pytest.raises(MeshCodeException) as e:
        meshcode_to_polygon("5339454715")
    assert str(e.value) == "4th mesh must be 1 to 4"

    with pytest.raises(MeshCodeException) as e:
        meshcode_to_polygon("55394")
    assert str(e.value) == "Mesh code must be 4, 6, 8, 9 or 10 digits"


def test_meshcode_to_polygon():
    """メッシュコードからポリゴンを生成するテスト"""
    from plateauutils.mesh_geocorder.geo_to_mesh import meshcode_to_polygon

    mesh_code = "5339"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139 35.333333333333336, 140 35.333333333333336, 140 36, 139 36, 139 35.333333333333336))"
    )

    mesh_code = "533900"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139 35.333333333333336, 139.125 35.333333333333336, 139.125 35.41666666666667, 139 35.41666666666667, 139 35.333333333333336))"
    )

    mesh_code = "533945"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.625 35.66666666666667, 139.75 35.66666666666667, 139.75 35.75000000000001, 139.625 35.75000000000001, 139.625 35.66666666666667))"
    )

    mesh_code = "53394500"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.625 35.66666666666667, 139.6375 35.66666666666667, 139.6375 35.675000000000004, 139.625 35.675000000000004, 139.625 35.66666666666667))"
    )

    mesh_code = "53394547"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.7125 35.7, 139.725 35.7, 139.725 35.708333333333336, 139.7125 35.708333333333336, 139.7125 35.7))"
    )

    mesh_code = "533945471"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.7125 35.7, 139.71875 35.7, 139.71875 35.70416666666667, 139.7125 35.70416666666667, 139.7125 35.7))"
    )

    mesh_code = "533945472"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.71875 35.7, 139.725 35.7, 139.725 35.70416666666667, 139.71875 35.70416666666667, 139.71875 35.7))"
    )

    mesh_code = "533945473"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.7125 35.70416666666667, 139.71875 35.70416666666667, 139.71875 35.70833333333334, 139.7125 35.70833333333334, 139.7125 35.70416666666667))"
    )

    mesh_code = "533945474"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.71875 35.70416666666667, 139.725 35.70416666666667, 139.725 35.70833333333334, 139.71875 35.70833333333334, 139.71875 35.70416666666667))"
    )

    mesh_code = "5339454711"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.7125 35.7, 139.71562500000002 35.7, 139.71562500000002 35.702083333333334, 139.7125 35.702083333333334, 139.7125 35.7))"
    )

    mesh_code = "5339454712"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.71562500000002 35.7, 139.71875000000003 35.7, 139.71875000000003 35.702083333333334, 139.71562500000002 35.702083333333334, 139.71562500000002 35.7))"
    )

    mesh_code = "5339454713"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.7125 35.702083333333334, 139.71562500000002 35.702083333333334, 139.71562500000002 35.704166666666666, 139.7125 35.704166666666666, 139.7125 35.702083333333334))"
    )

    mesh_code = "5339454714"
    polygon = meshcode_to_polygon(mesh_code)
    assert (
        polygon.wkt
        == "POLYGON ((139.71562500000002 35.702083333333334, 139.71875000000003 35.702083333333334, 139.71875000000003 35.704166666666666, 139.71562500000002 35.704166666666666, 139.71562500000002 35.702083333333334))"
    )
