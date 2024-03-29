# coding: utf-8

import click
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from shapely.geometry import Point
from plateauutils.mesh_geocorder.geo_to_mesh import (
    point_to_meshcode as _point_to_meshcode,
    meshcode_to_polygon as _meshcode_to_polygon,
    MeshException,
    MeshCodeException,
)
from plateauutils.tile_list.geo_to_tile import (
    point_to_tile as _point_to_tile,
    tile_to_polygon as _tile_to_polygon,
    TileRangeException,
)


@click.group()
def cli():
    pass


@cli.group()
def mesh_geocorder():
    """Mesh geocorder commands"""
    pass


@mesh_geocorder.command()
@click.argument("longitude", required=True, type=float)
@click.argument("latitude", required=True, type=float)
@click.argument("mesh", required=False, type=str, default="2")
def point_to_meshcode(longitude, latitude, mesh):
    """Convert a point to a meshcode"""
    point = Point(longitude, latitude)
    try:
        meshcode = _point_to_meshcode(point, mesh)
        click.echo(meshcode)
    except MeshException as e:
        click.echo("Error: {}".format(e))


@mesh_geocorder.command()
@click.argument("meshcode", required=True, type=str)
def meshcode_to_polygon(meshcode):
    """Convert a meshcode to a polygon"""
    try:
        polygon = _meshcode_to_polygon(meshcode)
        click.echo(polygon.wkt)
    except MeshCodeException as e:
        click.echo("Error: {}".format(e))


@cli.group()
def tile_list():
    """Tile list commands"""
    pass


@tile_list.command()
@click.argument("longitude", required=True, type=float)
@click.argument("latitude", required=True, type=float)
@click.argument("zoom", required=True, type=int)
@click.argument("ext", required=False, type=str, default=".mvt")
def point_to_tile(longitude, latitude, zoom, ext):
    """Convert a point to a tile"""
    point = Point(longitude, latitude)
    tile = _point_to_tile(point, zoom, ext)
    click.echo(tile)


@tile_list.command()
@click.argument("tile_path", required=True, type=str)
def tile_to_polygon(tile_path):
    """Convert a tile to a polygon"""
    try:
        polygon = _tile_to_polygon(tile_path)
        click.echo(polygon.wkt)
    except TileRangeException as e:
        click.echo("Error: {}".format(e))


def main():
    cli()


if __name__ == "__main__":
    main()
