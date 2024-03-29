Plateau Utils
=============

This is a collection of utilities for the `Plateau <https://www.mlit.go.jp/plateau/>`_ project.

.. code:: bash

    pip install plateauutils

Tested with Python 3.9 and 3.10

CityGML parser
--------------

.. code:: python

    >>> from shapely.geometry import Point
    >>> from plateauutils.mesh_geocorder.geo_to_mesh import point_to_meshcode
    >>> point = Point(139.71475, 35.70078)
    >>> mesh_code = point_to_meshcode(point, "2/1")
    >>> mesh_code
    '533945471'
    >>> from shapely import from_wkt
    >>> from plateauutils.parser.city_gml_parser import CityGMLParser
    >>> target_polygon = from_wkt("POLYGON ((130.41249721501615 33.224722548534864, 130.41249721501615 33.22506264293093, 130.41621606802997 33.22506264293093, 130.41621606802997 33.224722548534864, 130.41249721501615 33.224722548534864))")
    >>> parser = CityGMLParser(target_polygon)
    >>> result = parser.download_and_parse("https://assets.cms.plateau.reearth.io/assets/d6/70821e-7f58-4f69-bc34-341875704e78/40203_kurume-shi_2020_citygml_3_op.zip", "/tmp")
    >>> result
    [{'gid': 'bldg_383f1804-aa34-4634-949f-f769e09fa92d', 'center': [130.41263587199947, 33.22489181671553], 'min_height': 3.805999994277954, 'measured_height': 9.3, 'building_structure_type': '非木造'}, {'gid': 'bldg_877dea60-35d0-4fd9-8b02-852e39c75d81', 'center': [130.41619367090038, 33.22492719812357], 'min_height': 4.454999923706055, 'measured_height': 3.0, 'building_structure_type': '非木造'},...]

URLs of CityGML zip files can be found at `G空間情報センター <https://www.geospatial.jp/ckan/dataset/plateau>`_.

MVT parser
----------

.. code:: python

    >>> from plateauutils.parser.mvt_tile_parser import MvtTileParser
    >>> target_polygon = from_wkt("POLYGON ((130.525689 33.323966, 130.522728 33.314069, 130.511441 33.308653, 130.501013 33.30937, 130.492516 33.318516, 130.493717 33.325831, 130.504618 33.332249, 130.512857 33.332213, 130.525689 33.323966))")
    >>> parser = MvtTileParser(target_polygon)
    >>> result = parser.download_and_parse("https://assets.cms.plateau.reearth.io/assets/43/53a0e1-cc14-4228-a5ef-19333a23596d/40203_kurume-shi_2020_3dtiles-mvt_3_op.zip", "/tmp")
    >>> result
    ['/tmp/40203_kurume-shi_2020_3dtiles-mvt_3_op/luse/15/28254/13174.mvt']

URLs of 3D Tiles/MVT zip files can be found at `G空間情報センター <https://www.geospatial.jp/ckan/dataset/plateau>`_.

Flood converter
---------------

.. code:: python

    >>> from plateauutils.flood_converter.flood_to_3dtiles import FloodTo3dtiles
    >>> f = FloodTo3dtiles()
    >>> f.convert('/tmp/floodmap_depth', '/tmp/depth_3dtiles')
    >>> from plateauutils.flood_converter.flood_to_png import FloodToPng
    >>> p = FloodToPng('/tmp/floodmap_depth')
    >>> p.parse('/tmp/depth_png')

How to develop
--------------

.. code:: bash

    python3.9 -m venv venv
    ./venv/bin/activate
    pip install -U pip
    pip install -r dev-requirements.txt
    pytest --cov=plateauutils --cov-report=html --cov-fail-under=90
