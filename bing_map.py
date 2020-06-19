# bing_map.py
# David Bomard 06/2020

from os import path, mkdir
from urllib import request
from math import ceil
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from TileServeur import DataServer
from TileSystem import LatLongToPixelXY, PixelXYToTileXY, TileXYToQuadKey, TileXYToPixelXY, PixelXYToLatLong, MapSize


class BingMap(QGraphicsScene):
    def __init__(self, coo_centre_lat_long, zoom, rect):
        """
        :param coo_centre_lat_long: coordonnées du point central de la carte
        :param zoom: niveau de zoom entre 1 et 23
        :param rect: Qrect : surface d'affichage de la vue.
        """
        super(BingMap, self).__init__()
        self.coordonnees = coo_centre_lat_long  # coordonnées du point central en degrés
        self.zoom = zoom  # valeur du zoom actuel. Varie 1 < zoom < 23
        self.data_type = 'aerial'  # définit le type de données affichées. Par défaut : images aériennes
        self.tile_serveur = DataServer(self.data_type)  # initialise le serveur de tuiles
        self.url = self.tile_serveur.get_image_url()  # url de base pour charger les tuiles
        self.surface_x = rect.width()  # dimension en x de la vue
        self.surface_y = rect.height()  # dimension en y de la vue
        self.dict_tiles = {}
        if not path.exists("cache/"):
            mkdir('cache/')
        self.update_view()

    def set_coordonnees(self, coo_lat_long):
        """
        Met à jour les coordonnées du point central de la carte
        :param coo_lat_long: tuple
        """
        self.coordonnees = coo_lat_long

    def get_coordonnees(self):
        return self.coordonnees

    def get_zoom(self):
        return self.zoom

    def set_zoom(self, new_zoom):
        if 1 <= new_zoom <= 23:
            self.zoom = new_zoom
            if not path.exists("cache/" + str(self.zoom) + '/'):
                mkdir('cache/' + str(self.zoom) + '/')
            for tile in self.dict_tiles:
                self.removeItem(self.dict_tiles.get(tile))
            self.dict_tiles.clear()
            self.surface_x = self.surface_y = MapSize(self.zoom)
            self.setSceneRect(0,0,self.surface_x, self.surface_y)

    """
    def update_surface(self, rect):
        self.surface_x = rect.width()
        self.surface_y = rect.height()
        center = self.get_pixel_center()
        self.setSceneRect(center[0] - (rect.width() >> 1), center[1] - (rect.height() >> 1), self.surface_x,
                          self.surface_y)
    """

    def move_center(self, delta_x, delta_y):
        coo_pixel_centre = self.get_pixel_center()
        coo_pixel_centre = (coo_pixel_centre[0] - delta_x, coo_pixel_centre[1] - delta_y)
        self.set_coordonnees(PixelXYToLatLong(coo_pixel_centre[0], coo_pixel_centre[1], self.zoom))
        self.update_view()

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
        # calcul des coordonnées en pixel du point central de la carte
        coo_pixel_centre = self.get_pixel_center()
        # calcul en pixel du point supérieur gauche
        coo_pixel_up_left = (coo_pixel_centre[0] - (self.surface_x >> 1),
                             coo_pixel_centre[1] - (self.surface_y >> 1))
        # calcul de la tuile du haut à gauche
        coo_tile_up_left = PixelXYToTileXY(coo_pixel_up_left[0],
                                           coo_pixel_up_left[1])

        # calcul en pixel du point inférieur droit
        coo_pixel_bottom_right = (coo_pixel_centre[0] + (self.surface_x >> 1),
                                  coo_pixel_centre[1] + (self.surface_y >> 1))
        # calcul de la tuile du bas à droite
        coo_tile_bottom_right = PixelXYToTileXY(coo_pixel_bottom_right[0],
                                                coo_pixel_bottom_right[1])

        # boucle pour remplir le dictionnaire de tuiles + ajout des tuiles à la scène
        for x in range(coo_tile_up_left[0], coo_tile_bottom_right[0] + 1):
            for y in range(coo_tile_up_left[1], coo_tile_bottom_right[1] + 1):
                if self.dict_tiles.get((x, y), None) == None:
                    quadkey = TileXYToQuadKey(x, y, self.zoom)
                    tile = self.load_tile(quadkey)
                    img_item = self.addPixmap(tile)
                    coo_pixel_xy = TileXYToPixelXY(x, y)
                    img_item.setPos(coo_pixel_xy[0], coo_pixel_xy[1])
                    self.dict_tiles[(x, y)] = img_item

    def load_tile(self, quadkey):
        """
        Charge une tuile depuis le cache sinon la télécharge depuis le serveur
        :param quadkey: quadkey de la tuile à charger
        :return: un QPixmap contenant la tuile
        """
        img = QPixmap()
        # La tuile est-elle déjà dans le cache ?
        if not img.load("cache/" + str(self.zoom) + '/' + str(quadkey) + ".png", "PNG"):
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
        image.save("cache/" + str(self.zoom) + '/' + str(quadkey) + '.png', "PNG")
        return image
