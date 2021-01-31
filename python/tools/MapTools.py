import os
from os import listdir
from os.path import isfile, join
import json
from pprint import pprint as pp

import folium


def fix_markers(dir_name):
    onlyfiles = [f for f in listdir(
        dir_name) if isfile(join(dir_name, f))]

    allAttrs = ['name_id', 'loc', 'name_code', 'img_url', 'wiki_link',
                'site_link', 'text', 'marker_color', 'marker_icon', 'marker_icon_prefix']

    for f_name in onlyfiles:
        with open(f"{dir_name}{f_name}") as json_file:
            data = json.load(json_file)
        for attr in allAttrs:
            if (attr not in data.keys()):
                data[attr] = ''
        with open(f"{dir_name}{f_name}", "w") as jsonFile:
            json.dump(data, jsonFile)


def load_markers(dir_name):
    """ Load markers from a dir, then returns dict 

        Keyword arguments:
            dir_name -- (string) relative path to directory with marker files
                ** path = f"{dirName}"
    """

    result = {}
    path = f"{dir_name}"

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f_name in onlyfiles:
        with open(f"{path}{f_name}") as json_file:
            data = json.load(json_file)
        result[f_name.split('.')[0]] = data
    return result


def load_areas(dir_name):
    """ Load geoJSON data from a dir, then returns list

        Keyword arguments:
            dir_name -- (string) relative path to directory with geoJSON files
                ** path = f"{dir_name}"
    """

    result = []
    path = f"{dir_name}"

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f_name in onlyfiles:
        with open(f"{path}{f_name}") as json_file:
            data = json.load(json_file)
        result.append(data)
    return result


def add_areas_to_map(areas, names, styles, m):
    """ Add areas to map

        Keyword arguments:
            areas -- (list) list of areas (area - dict with geoJSON data)
            names -- (list) list of areas names (name - string)
            styles -- (list) list of dicts with styles
                ** fillColor: hex color code
                ** color: hex color code
                ** opacity: float number
            m -- (obj) folium map object
    """
    def add_area_to_map(a, n, s, m):
        folium.GeoJson(
            a,
            name=n,
            style_function=lambda x: s,
        ).add_to(m)

    for i in range(len(areas)):
        add_area_to_map(areas[i], names[i], styles[i], m)


def add_markers_to_map(markers_dict, group):
    """ Add markers to map

        Keyword arguments:
            markers_dict -- (dict) dict with markers
                ** name_id: string
                ** loc: list [float, float]
                ** name_code: escaped unicode string, example: "\\u0413\\u0438\\u043f\\u0435\\u0440\\u0438\\u043e\\u043d"
                ** img_url: string
                ** wiki_link: string
                ** site_link: string
                ** text: escaped unicode string
                ** marker_color: string (check folium allowed colors)
                ** marker_icon: string (check folium allowed marker icons)
                ** marker_icon_prefix: string (check folium allowed marker icon prefixes)
            group -- folium subgroup object
    """

    for item in markers_dict.keys():
        el = markers_dict[item]

        wiki = f"<p style='text-align:center;'><a href='{el['wiki_link']}' target='_blank'>~ WIKI ~</a></p>" if (
            el['wiki_link'] != '' and el['wiki_link'] != 'None') else ''

        www = f"<p style='text-align:center;'><a href='{el['site_link']}' target='_blank'>~ WWW ~</a></p>" if (
            el['site_link'] != '') else ''

        text = f"<p style='text-align:center;font-size:larger;'>{el['text']}</p>" if (
            el['site_link'] != '') else ''

        template = f"<h3 style='text-align:center;'>{el['name_code']}</h3>{text}{wiki}{www}<p style='text-align:center;'><img style='border-radius:0.3rem;max-width:35vw;' src='{el['img_url']}'>"

        marker = folium.Marker(
            location=el['loc'],
            popup=template,
            icon=folium.Icon(
                color=el['marker_color'], icon=el['marker_icon'], prefix=el['marker_icon_prefix'])
        )

        group.add_child(marker)
