# -*- coding: utf-8 -*-
__author__ = 'P. Saint-Amand'
__appname__ = 'Volcanoes'
__version__ = 'V 0.0.1'

# Standard Python Modules
import logging
import os
from pathlib import Path
from typing import Any

# External Python Modules
import folium
import pandas as pd

# Personal Python Modules
import utils
from constants import *

def get_logger(logger_name:str=None, console_loglevel:int=LOGLEVEL_SUCCESS, file_loglevel:int=LOGLEVEL_DISABLE, logfile:Path=None) -> utils.ColorLogger:
    if not logfile and file_loglevel != LOGLEVEL_DISABLE:
        logfile = os.path.join(LOG_DIR,__appname__+".log")
    if not logger_name:
        logger_name, _ = os.path.splitext(os.path.basename(__file__))

    
    logging.addLevelName(LOGLEVEL_SUCCESS, 'SUCCESS')
    log_options = utils.ColorLoggerOptions(logfile_name=logfile, console_logging_level=console_loglevel, logfile_logging_level=file_loglevel)
    logger = utils.ColorLogger(name=__appname__, options=log_options)
    # save_logger_options(log_options)
    return logger

def init():
    """ Clear Screen, display banner & start the logger. """
    CONSOLE.clear_screen()
    if BANNER:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=banner_lst, appversion=__version__, creator="Designed by " + __author__))
    global logger
    logger = get_logger(logger_name=__appname__, console_loglevel=LOGLEVEL_CONSOLE, file_loglevel=LOGLEVEL_FILE)
    logger.debug("Debug Mode Activated")

def load_csv(filename, delimiter:str) -> pd.DataFrame:
    try:
        logger.debug(f"Loading file '{filename}'")
        content = pd.read_csv(filename, encoding="utf-8", encoding_errors="ignore", delimiter=delimiter, low_memory=False)
    except Exception as e:
        logger.error(f"Fail to load CSV file '{filename}':")
        logger.error("ERROR", f"{str(e)}")
    else:
        (nb_rows, nb_columns) = content.shape
        logger.log(LOGLEVEL_SUCCESS, f"CSV file Successfully loaded '{filename}'")
        logger.info(f"File contains {nb_columns} columns and {nb_rows} lines")
    return content

def map_build(df:pd.DataFrame) -> folium.Map:
    logger.debug(f"Building Map...")

    avg_lat = df["Latitude"].mean()
    avg_lon = df["Longitude"].mean()
    volcano_statuses = sorted(df.Status.unique())
    volcano_types = sorted(df.Type.unique())

    map = folium.Map(location=[avg_lat ,avg_lon],zoom_start=3, tiles="Stamen Terrain")
    
    # Note on some Google search parameters:
    #   q=<query>
    #   &tbm=isch (search fior images)
    iframe_html = """
    <strong>Volcano name</strong>: <a href="https://www.google.com/search?q=%%22%s volcano%%22&tbm=isch" target="_blank">%s</a><br>
    <strong>Height</strong>: %s m<br>
    <strong>Type</strong>: %s<br>
    <strong>Status</strong>: %s<br>
    """
    for name in volcano_types:
        logger.debug(f"Processing layer '{name}'")
        fg = folium.FeatureGroup(name=name)
        for idx, volcano in df.loc[df.Type == name].iterrows():
            iframe = folium.IFrame(html=iframe_html % (volcano["Volcano Name"], volcano["Volcano Name"], volcano["Elevation (m)"], volcano.Type, volcano.Status), width=250, height=100)
            color_index = volcano_statuses.index(volcano.Status) % len(MAP_COLORS)
            fg.add_child(folium.Marker(location=[volcano.Latitude ,volcano.Longitude], popup=folium.Popup(iframe), icon=folium.Icon(color=MAP_COLORS[color_index],icon="fire")))        
        map.add_child(fg)

    map.add_child(folium.LayerControl())
    return map
    
def map_save(map:folium.Map, outfile:Path) -> None:
    try:
        logger.debug(f"Saving map to '{outfile}'")
        map.save(outfile)
    except Exception as e:
        logger.error(f"Fail to save map as HTML file'{outfile}':")
        logger.error("ERROR", f"{str(e)}")
    else:
        logger.log(LOGLEVEL_SUCCESS, f"Map successfully saved as HTML file '{outfile}'")

if __name__ == "__main__":
    init()
    df = load_csv(filename=DATA_FILE, delimiter=CSV_DELIMITER)
    map = map_build(df)
    map_save(map, OUT_FILE)