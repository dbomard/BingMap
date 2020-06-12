import requests


class DataServer:
    def __init__(self, data_type):
        super().__init__()
        self.imageUrl = None
        self.imageUrlSubdomains = None
        self.imageHeight = None
        self.imageWidth = None
        self.resourceSets = None
        self.resources = None
        self.zoomMax = None
        self.zommMin = None
        self.__key = 'AsXU8jBLhuJYXAJS5F-f_5BoOfhOI2gcHdDq7N8tI7c5zwkfzxbos8comYa1pOqs'
        self.init(data_type)

    def init(self, data_type):
        response = requests.get(
            "https://dev.virtualearth.net/REST/v1/Imagery/Metadata/" + data_type + "?key=" + self.__key)
        metadata = response.json()
        for attr_name, attr_value in metadata.items():
            setattr(self, attr_name, attr_value)
        for attr_name, attr_value in self.resourceSets[0].items():
            setattr(self, attr_name, attr_value)
        for attr_name, attr_value in self.resources[0].items():
            setattr(self, attr_name, attr_value)

    def get_image_url(self):
        """
        retourne l'url de l'image sans le quadkey
        :param coordonnees: tuple(latitude, longitude)
        :param zoom: entier niveau de zoom
        :return: str représentant l'url de l'image
        """
        # pixel_xy = TileSystem.LatLongToPixelXY(coordonnees[0], coordonnees[1], zoom)
        # tile_xy = TileSystem.PixelXYToTileXY(pixel_xy[0], pixel_xy[1])
        # quad_key = TileSystem.TileXYToQuadKey(tile_xy[0], tile_xy[1], zoom)

        url = self.imageUrl.replace('{subdomain}', self.imageUrlSubdomains[0])
        # url = url.replace('{quadkey}', quad_key)
        return url


"""
test_serv = DataServer('aerial')
print(test_serv.get_image_url((48.858333, 2.294444), 15))
"""
