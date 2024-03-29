from plateauutils.mesh_geocorder.polygon_to_meshcode_list import PolygonToMeshCodeList
from shapely import from_wkt


def test_polygon_to_list():
    polygon = from_wkt(
        "POLYGON ((136.312866 34.930979, 136.345825 35.670685, 137.416992 35.661759, 136.312866 34.930979))%"
    )
    polygon_to_list = PolygonToMeshCodeList(polygon, "1")
    assert polygon_to_list.output() == sorted(["5236", "5336", "5337"])
    polygon = from_wkt(
        "POLYGON ((136.457062 35.610418, 136.568298 35.60651, 136.561432 35.472414, 136.459122 35.470736, 136.456375 35.431582, 136.662369 35.429904, 136.663742 35.635535, 136.459122 35.640557, 136.457062 35.610418))"
    )
    polygon_to_list = PolygonToMeshCodeList(polygon, "2")
    assert polygon_to_list.output() == sorted(
        ["533633", "533634", "533635", "533624", "533625", "533613", "533614", "533615"]
    )
    polygon = from_wkt(
        "POLYGON ((136.558943 35.569656, 136.554565 35.554365, 136.528301 35.554365, 136.530619 35.563303, 136.558943 35.569656))"
    )
    polygon_to_list = PolygonToMeshCodeList(polygon, "3")
    assert polygon_to_list.output() == sorted(
        [
            "53362462",
            "53362463",
            "53362464",
            "53362472",
            "53362473",
            "53362474",
            "53362484",
            "53362483",
        ]
    )
    polygon = from_wkt(
        "POLYGON ((136.543257 35.564001, 136.54109 35.561959, 136.544931 35.560492, 136.543257 35.564001))"
    )
    polygon_to_list = PolygonToMeshCodeList(polygon, "2/1")
    assert polygon_to_list.output() == sorted(
        ["533624731", "533624732", "533624733", "533624734"]
    )
    polygon_to_list = PolygonToMeshCodeList(polygon, "4/1")
    assert polygon_to_list.output() == sorted(
        ["5336247314", "5336247323", "5336247332", "5336247341"]
    )
    polygon = from_wkt(
        "POLYGON ((130.41249721501615 33.224722548534864, 130.41249721501615 33.348, 130.59 33.348, 130.59 33.224722548534864, 130.41249721501615 33.224722548534864))"
    )
    polygon_to_list = PolygonToMeshCodeList(polygon, "3")
    assert "49307460" in polygon_to_list.output()
