# bing_map.py
# David Bomard 06/2020

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from TileServeur import DataServer
from TileSystem import LatLongToPixelXY, PixelXYToTileXY, TileXYToQuadKey, QuadKeyToTileXY, TileXYToPixelXY
from urllib import request
from PyQt5.QtGui import QPixmap


class BingMap(QGraphicsScene):
    def __init__(self, coo_centre_lat_long, zoom):
        super(BingMap, self).__init__()
        self.coordonnees = coo_centre_lat_long  # coordonnées du point central
        self.zoom = zoom  # valeur du zoom actuel. Varie 1 < zoom < 23
        self.data_type = 'aerial'  # définit le type de données affichées. Par défaut : images aériennes
        self.tile_serveur = DataServer(self.data_type)  # initialise le serveur de tuiles
        self.url = self.tile_serveur.get_image_url()  # url de base pour charger les tuiles

        self.ui_init()

    def set_coordonnees(self, coo_lat_long):
        self.coordonnees = coo_lat_long

    def ui_init(self):
        # conversion des coordonnées du centre en quadkey
        coo_pixel_xy = LatLongToPixelXY(self.coordonnees[0], self.coordonnees[1], self.zoom)
        coo_tile_xy = PixelXYToTileXY(coo_pixel_xy[0], coo_pixel_xy[1])
        quadkey = TileXYToQuadKey(coo_tile_xy[0], coo_tile_xy[1., self.zoom], self.zoom)
        tile = self.load_tile(quadkey)
        img_item = QGraphicsPixmapItem(tile)
        # calcul des coordonnées de la tuile centrale:
        coo_tile_xy = QuadKeyToTileXY(quadkey)
        coo_pixel_xy = TileXYToPixelXY(coo_tile_xy[0], coo_tile_xy[1])
        img_item.setPos(coo_pixel_xy[0], coo_pixel_xy[1])
        self.addPixmap(img_item)

    def load_tile(self, quadkey):
        img = QPixmap()
        # La tuile est-elle déjà dans le cache ?
        if not img.load("..cache/" + str(self.zoom) + '/' + str(quadkey) + ".png", "PNG"):
            # sinon télécharger depuis le serveur
            img = self.download_tile(quadkey)
        return img

    def download_tile(self, quadkey):
        # téléchargement de la tuile
        image = QPixmap()
        image.loadFromData(request.urlopen(self.url.replace('{quadkey}', quadkey)).read())
        # enregistrement dans le dossier correspondant au niveau de zoom
        image.save("..cache/" + str(self.zoom) + '/' + str(quadkey) + '.png', "PNG")
        return image

