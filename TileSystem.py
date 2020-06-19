"""
Adaptation en Python d'après fichier microsoft initialement écrit en C# par Joe Schwartz
30/05/2020
David Bomard
"""

from math import cos, pi, sin, log, atan, exp

EARTH_RADIUS = 6378137
MIN_LATITUDE = -85.05112878
MAX_LATITUDE = 85.05112878
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180


def Clip(n, min_value, max_value):
    """
    clips a number to the specified minimum and maximum values
    :param n: the value to clip
    :param min_value: Minimum allowable value
    :param max_value: Maximum allowable value
    :return: The clipped value
    """
    return min(max(n, min_value), max_value)


def MapSize(level_of_detail):
    """
    Determines the map width and height (in pixels) at a specified level of detail.
    :param level_of_detail:Level of detail, from 1 (lowest detail) to 23 (highest detail)
    :return: The map width and height in pixels
    """
    return 256 << level_of_detail


def GroundResolution(latitude, level_of_detail):
    """
    Determines the ground resolution (in meters per pixel) at a specified
    latitude and level of detail
    :param latitude: Latitude (in degrees) at which to measure the
    ground resolution
    :param level_of_detail: Level of detail, from 1 (lowest detail)
    to 23 (highest detail)
    :return: The ground resolution, in meters per pixel
    """
    latitude = Clip(latitude, MIN_LATITUDE, MAX_LATITUDE)
    return cos(latitude * pi / 180) * 2 * pi * EARTH_RADIUS / MapSize(level_of_detail)


def LatLongToPixelXY(latitude, longitude, level_of_detail):
    """
    Converts a point from latitude/longitude WGS-84 coordinates (in degrees)
    into pixel XY coordinates at a specified level of detail
    :param latitude: Latitude of the point, in degrees
    :param longitude: Longitude of the point, in degrees
    :param level_of_detail:Level of detail, from 1 (lowest detail)
    to 23 (highest detail)
    :return: a tuple (the X coordinate in pixels, the Y coordinate in pixels)
    """
    latitude = Clip(latitude, MIN_LATITUDE, MAX_LATITUDE)
    longitude = Clip(longitude, MIN_LONGITUDE, MAX_LONGITUDE)

    x = (longitude + 180) / 360
    sin_latitude = sin(latitude * pi / 180)
    y = 0.5 - log((1 + sin_latitude) / (1 - sin_latitude)) / (4 * pi)

    map_size = MapSize(level_of_detail)
    pixel_x = int(Clip(x * map_size + 0.5, 0, map_size - 1))
    pixel_y = int(Clip(y * map_size + 0.5, 0, map_size - 1))

    return pixel_x, pixel_y


def PixelXYToLatLong(pixel_x, pixel_y, level_of_detail):
    """
    Converts a pixel from pixel XY coordinates at a specified level of detail
    into latitude/longitude WGS-84 coordinates (in degrees
    :param pixel_x: X coordinate of the point, in pixels
    :param pixel_y: Y coordinates of the point, in pixels
    :param level_of_detail: Level of detail, from 1 (lowest detail)
    to 23 (highest detail)
    :return: a tuple (latitude in degrees, longitude in degrees)
    """
    map_size = MapSize(level_of_detail)
    x = (Clip(pixel_x, 0, map_size - 1) / map_size) - 0.5
    y = 0.5 - (Clip(pixel_y, 0, map_size - 1) / map_size)

    latitude = 90 - 360 * atan(exp(-y * 2 * pi)) / pi
    longitude = 360 * x

    return latitude, longitude


def PixelXYToTileXY(pixel_x, pixel_y):
    """
    Converts pixel XY coordinates into tile XY coordinates of the tile containing
    the specified pixel
    :param pixel_x: Pixel X coordinate
    :param pixel_y: Pixel X coordinate
    :return: tuple (tile x coordinate, tile y coordinate
    """
    tile_x = int(pixel_x / 256)
    tile_y = int(pixel_y / 256)
    return tile_x, tile_y


def TileXYToPixelXY(tile_x, tile_y):
    """
    Converts tile XY coordinates into pixel XY coordinates of the upper-left pixel
    of the specified tile
    :param tile_x: Tile X coordinate
    :param tile_y: Tile Y coordinate
    :return: tuple (pixel x coordinate, pixel y coordinate)
    """
    pixel_x = tile_x * 256
    pixel_y = tile_y * 256
    return pixel_x, pixel_y


def TileXYToQuadKey(tile_x, tile_y, level_of_detail):
    """
    Converts tile XY coordinates into a QuadKey at a specified level of detail
    :param tile_x: Tile X coordinate
    :param tile_y: Tile Y coordinate
    :param level_of_detail: Level of detail, from 1 (lowest detail)
    to 23 (highest detail)
    :return: A string containing the QuadKey
    """
    quadkey = ''
    for i in range(level_of_detail, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (tile_x & mask) != 0:
            digit += 1
        if (tile_y & mask) != 0:
            digit += 2
        quadkey = quadkey + str(digit)
    return quadkey


def QuadKeyToTileXY(quad_key):
    """
    Converts a QuadKey into tile XY coordinates
    :param quad_key: QuadKey of the tile
    :return: tuple (tile X coordinate, tile Y coordinate, level of detail)
    """
    tile_x = 0
    tile_y = 0
    level_of_detail = len(quad_key)

    for i in range(level_of_detail, 0, -1):
        mask = 1 << (i - 1)
        switcher = quad_key[level_of_detail - i]
        if switcher == '0':
            break
        elif switcher == '1':
            tile_x |= mask
        elif switcher == '2':
            tile_y |= mask
        elif switcher == '3':
            tile_x |= mask
            tile_y |= mask
        else:
            raise ValueError('Invalid Quadkey digit sequence')
    return tile_x, tile_y, level_of_detail
