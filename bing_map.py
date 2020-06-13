# bing_map.py
# David Bomard 06/2020

from os import path, mkdir
from urllib import request

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from TileServeur import DataServer
from TileSystem import LatLongToPixelXY, PixelXYToTileXY, TileXYToQuadKey, TileXYToPixelXY


class BingMap(QGraphicsScene):
    def __init__(self, coo_centre_lat_long, zoom, rect):
        """
        :param coo_centre_lat_long: coordonnées du point central de la carte
        :param zoom: niveau de zoom entre 1 et 23
        :param rect: Qrect : surface d'affichage de la vue.
        """
        super(BingMap, self).__init__()
        self.coordonnees = coo_centre_lat_long  # coordonnées du point central
        self.zoom = zoom  # valeur du zoom actuel. Varie 1 < zoom < 23
        self.data_type = 'aerial'  # définit le type de données affichées. Par défaut : images aériennes
        self.tile_serveur = DataServer(self.data_type)  # initialise le serveur de tuiles
        self.url = self.tile_serveur.get_image_url()  # url de base pour charger les tuiles
        self.surface_x = rect.width()  # dimension en x de la vue
        self.surface_y = rect.height()  # dimension en y de la vue
        self.cache_dir = 'cache/'

        self.update_view()

    def set_coordonnees(self, coo_lat_long):
        """
        Met à jour les coordonnées du point central de la carte
        :param coo_lat_long: tuple
        """
        self.coordonnees = coo_lat_long

    def get_pixel_center(self):
        """
        retourne les coordonnées en pixel du centre de la carte
        :return:
        """
        return LatLongToPixelXY(self.coordonnees[0], self.coordonnees[1], self.zoom)

    def update_view(self):
        """
        Mise à jour de la vue
        """
        # calcul de la tuile centrale
        coo_pixel_xy = LatLongToPixelXY(self.coordonnees[0], self.coordonnees[1], self.zoom)
        coo_tile_xy = PixelXYToTileXY(coo_pixel_xy[0], coo_pixel_xy[1])

        # calcul du nombre de tuiles nécessaires en x :
        nb_tiles_x = int(self.surface_x / 256 + 1)
        nb_tiles_y = int(self.surface_y / 256 + 1)

        # calcul de la tuile en haut à gauche
        top_tile_x = coo_tile_xy[0] - (nb_tiles_x >> 1)
        top_tile_y = coo_tile_xy[1] - (nb_tiles_y >> 1)

        # ajout des tuiles à la scène
        for x in range(nb_tiles_x):
            for y in range(nb_tiles_y):
                quadkey = TileXYToQuadKey(x + top_tile_x, y + top_tile_y, self.zoom)
                tile = self.load_tile(quadkey)
                img_item = QGraphicsPixmapItem(tile)
                coo_pixel_xy = TileXYToPixelXY(x + top_tile_x, y + top_tile_y)
                img_item.setPos(coo_pixel_xy[0], coo_pixel_xy[1])
                self.addItem(img_item)

    def load_tile(self, quadkey):
        """
        Charge une tuile depuis le cache sinon la télécharge depuis le serveur
        :param quadkey: quadkey de la tuile à charger
        :return: un QPixmap contenant la tuile
        """
        img = QPixmap()
        # La tuile est-elle déjà dans le cache ?
        if not img.load("cache/" + str(quadkey) + ".png", "PNG"):
            # sinon télécharger depuis le serveur
            img = self.download_tile(quadkey)
        return img

    def download_tile(self, quadkey):
        """
        Télécharge la tuile passée en paramètre depuis le serveur puis
        l'enregistre dans le cache dans un répertoire correspondant au zoom
        actuel de la carte
        :param quadkey: quadkey de la tuile à télécharger
        :return: QPixmap contenant l'image
        """
        # téléchargement de la tuile
        image = QPixmap()
        image.loadFromData(request.urlopen(self.url.replace('{quadkey}', quadkey)).read())
        # enregistrement dans le dossier correspondant au niveau de zoom
        if not path.exists("cache/"):
            mkdir('cache/')
        if not path.exists("cache/" + str(self.zoom) + '/'):
            mkdir('cache/' + str(self.zoom) + '/')
        image.save("cache/" + str(self.zoom) + '/' + str(quadkey) + '.png', "PNG")
        return image
