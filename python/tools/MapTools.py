import os
from os import listdir
from os.path import isfile, join
import json

import folium


def load_markers(dir_name):
    """ Load markers from a dir, then returns dict 

        Keyword arguments:
            dir_name -- (string) relative path to directory with marker files
                ** path = f"./{dirName}/"
    """

    result = {}
    path = f"./{dir_name}/"

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
                ** path = f"./{dir_name}/"
    """

    result = []
    path = f"./{dir_name}/"

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for f_name in onlyfiles:
        with open(f"{path}{f_name}") as json_file:
            data = json.load(json_file)
        result.append(data)
    return result


def add_areas(areas, names, styles, m):
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

    for i in range(len(areas)):
        folium.GeoJson(
            areas[i],
            name=names[i],
            style_function=lambda x: styles[i]
        ).add_to(m)


def add_markers_to_map(markers_dict, group, shop=False):
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
            shop -- (bool) flag, workaround solution
    """

    h3_s = "<h3 style='text-align:center;'>"
    h3_e = "</h3>"
    pa_s = "<p style='text-align:center;'><a href='"
    pa_e = "' target='_blank'>~ Wiki ~</a></p>"
    pa_e_alt = "' target='_blank'>~ WWW ~</a></p>"
    img_s = "<img style='border-radius:0.3rem;max-width:35vw;' src='"
    p_shop_s = "<p style='text-align:center;font-size:larger;'>"
    p_shop_e = "</p>"

    for item in markers_dict.keys():
        el = markers_dict[item]
        if (el['marker_color'] == False) or (el['marker_icon_prefix'] == False):
            marker = folium.Marker(
                location=el['loc'],
                popup=f"{h3_s}{el['name_code']}{h3_e}{pa_s}{el['wiki_link']}{pa_e}{img_s}{el['img_url']}'",
                icon=folium.Icon(icon=el['marker_icon']),
            )
        else:
            marker = folium.Marker(
                location=el['loc'],
                popup=f"{h3_s}{el['name_code']}{h3_e}{pa_s}{el['wiki_link']}{pa_e}{img_s}{el['img_url']}'",
                icon=folium.Icon(
                    color=el['marker_color'], icon=el['marker_icon'], prefix=el['marker_icon_prefix']),
            )

        if (el['wiki_link'] == 'None'):
            marker = folium.Marker(
                location=el['loc'],
                popup=f"{h3_s}{el['name_code']}{h3_e}{img_s}{el['img_url']}'",
                icon=folium.Icon(
                    color=el['marker_color'], icon=el['marker_icon'], prefix=el['marker_icon_prefix']),
            )
        if (shop):
            marker = folium.Marker(
                location=el['loc'],
                popup=f"{h3_s}{el['name_code']}{h3_e}{p_shop_s}{el['text']}{p_shop_e}{pa_s}{el['site_link']}{pa_e_alt}{img_s}{el['img_url']}'",
                icon=folium.Icon(
                    color=el['marker_color'], icon=el['marker_icon'], prefix=el['marker_icon_prefix']),
            )

        group.add_child(marker)
