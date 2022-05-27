from csv import reader
from os import walk

import pygame


def import_csv_layout(path):
    eath_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            eath_map.append(list(row))
        return eath_map

def import_csv_main(path):
    everything = []
    with open(path) as maincsv:
        csv = reader(maincsv, delimiter=';')
        for row in csv:
            everything.append(list(row))

    types, pathsCSV, pathsgraphics = [], [], []

    for listcsv in everything:
            types.append(str(listcsv[0]))
            pathsCSV.append(str(listcsv[1]))
            pathsgraphics.append(str(listcsv[2]))

    return types, pathsCSV, pathsgraphics


def import_folder(path, name):
    name += '.png'
    for _, __, img_files in walk(path, name):
        for image in img_files:
            full_path = path + '/' + name
            image_surf = pygame.image.load(full_path).convert_alpha()

    return image_surf



