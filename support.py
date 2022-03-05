from os import walk
import pygame


def importFolder(path):
    surfaceList = []

    for _, __, imgFile in walk(path):
        for img in imgFile:
            fullPath = path + "/" + img
            imageSurface = pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurface)

    return surfaceList
