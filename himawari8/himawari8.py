#!/usr/bin/env python

import os
import requests
from PIL import Image
from tqdm import tqdm

IMAGE = 'D531106'
HIMAWARI = 'himawari8.nict.go.jp'
BASE_URL = 'http://%s/img/%s' % (HIMAWARI, IMAGE)

def GetLastImageDate(n_trials = 10):
    
    """
    Parameters
        - n_trials: Number of retries on requests
        
    Return: 
        the date of the last satellite photo
    """
    
    session = requests.Session()
    for i in range(n_trials):
        try:
            response = session.get('%s/latest.json' % (BASE_URL))
            if response.status_code != 200:
                continue
            date = response.json().get('date')
            session.close()
            return date
        except:
            continue
    session.close()
    raise Exception('Failed to connect to server: Connection timed out.')

def FormatDate(date):
    
    """
    Parameters
        - date: date to be formatted (yyyy-mm-dd hh:mm:ss)
        
    Return:
        the date formated (yyyy/mm/dd/hhmmss)
    """
    
    date = date.replace('-', '/')
    date = date.replace(' ', '/')
    date = date.replace(':', '')
    return date

def GetTile(url, n_trials = 10):
    
    """
    Parameters
        - url: Url of image
        - n_trials: Number of retries on requests 
        
    Return: 
        the tile of image taken from planet Earth of the Japanese satellite Himawari 8
    """
    
    session = requests.Session()
    for i in range(n_trials):
        try:
            response = session.get(url, stream=True)
            if response.status_code != 200:
                continue
            session.close()
            return Image.open(response.raw)
        except:
            continue
    session.close()
    raise Exception('Failed to connect to server: Connection timed out.')

def GetUrlTile(tile_number, date, h, v):

    """
    Parameters
        - tile_number: Number of tiles
        - date: Date of image (yyyy-mm-dd hh:mm:ss)
        - h: Colunm position of tile
        - v: row position of tile
        
    Return:
        the url of tile of photo of himawari satelite image 
    """
    
    return '%s/%dd/550/%s_%d_%d.png' % (BASE_URL, tile_number, FormatDate(date), h, v)

def GetImageEarth(img_path = "", img_name = 'himawari.png', scale = 550, tile_number = 4, save_img = False, n_trials = 10, show_progress = True):
    
    """
    Parameters
        - img_path: Path where the image will be saved
        - img_name: Name of the image if it is saved
        - scale: Scale of tiles
        - tile_number: Number of tiles: 2, 4, 8, 16, 20
        - save_img: Save image option
        - n_trials: Number of retries on requests
    
    Return:
        the last image taken from planet Earth of the Japanese satellite Himawari 8
    """
    
    if not tile_number in {2, 4, 8, 16, 20}:
        raise Exception("The tile_number value '{}' is outside valid values".format(tile_number))
        return
    
    HORIZONTAL = tuple(range(0, tile_number))
    VERTICAL = tuple(range(0, tile_number))
    path = '%s%s' % (img_path, img_name)    
    date = GetLastImageDate(n_trials)
    image = Image.new('RGB', tuple(scale * len(n) for n in (HORIZONTAL, VERTICAL)))

    for x, h in enumerate(tqdm(iterable = HORIZONTAL, disable = not show_progress)):
        for y, v in enumerate(VERTICAL):
            url = GetUrlTile(tile_number, date, h, v)
            tile = GetTile(url, n_trials)
            image.paste(tile.resize((scale, scale), Image.BILINEAR), tuple(n * scale for n in (x, y)))
    
    if save_img:
        image.save(path)

    return image
