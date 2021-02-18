import pandas as pd
import numpy as np
import datetime as dt
import geopandas as gpd
from shapely.geometry import Point, LineString,MultiLineString,Polygon
from shapely import ops
import matplotlib.pyplot as plt
import os
import folium
attr='(c) <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors (c) <a href="http://cartodb.com/attributions">CartoDB</a>, CartoDB <a href ="http://cartodb.com/attributions">attributions</a>'
from selenium import webdriver
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import glob
import moviepy.editor as mpy
import time

cities = ["bandung", "malang", "jakarta", "singapore", "surabaya", "yogyakarta"]
month = "Februari"

daydict = {0:'s e n i n',
          1:'s e l a s a',
          2: 'r a b u',
          3:'k a m i s',
          4:'j u m a t', 5:'s a b t u', 6:'m i n g g u'}

def get_crop(infile):
    f = infile.split("\\")[-1]
    original = Image.open(pngs_loc+f)
    the_date = dt.datetime.strptime(f.split(".")[0], "%Y-%m-%d %H-%M-%S")
    
    # crop image
    width, height = original.size  
    left = width/9
    top = height/6
    right = 8*width/9
    bottom = 7 * height/8
    cropped_example = original.crop((left, top, right, bottom))
    draw = ImageDraw.Draw(cropped_example)
                                    
    # captions                                
    day=daydict[the_date.weekday()].upper()
    hour=str(the_date.hour).zfill(2)+":"+str(the_date.minute).zfill(2)
    bottomword=str(the_date.day)+" "+month+" "+str(the_date.year)
    
    # initialize position
    the_x=1050
    start_y=730
                                    
    # write hours                               
    font = ImageFont.truetype('./Montserrat/Montserrat-ExtraBold.ttf', size=60)
    # the x position is relative to the minute value
    (x, y) = (50+((cropped_example.size[0]-100)/28.5)*(the_date.hour+the_date.minute*1./60), start_y)
    color = 'rgb(255, 255, 255)' 
    draw.multiline_text((x, y), hour, fill=color, font=font, align="right")

    # write day
    day_x=50+((cropped_example.size[0]-150)/7)*(the_date.weekday())
    font = ImageFont.truetype('./Montserrat/Montserrat-Regular.ttf', size=30)
    # the x position is relative to the day value
    (x, y) = (day_x, start_y+60)
    color = 'rgb(255, 255, 255)'
    draw.text((x, y), day, fill=color, font=font)

    # write date
    font = ImageFont.truetype('./Montserrat/Montserrat-ExtraBold.ttf', size=25)
    (x, y) = (day_x, start_y+90)
    color = 'rgb(175, 171, 171)'
    draw.text((x, y), bottomword, fill=color, font=font)
                                    
    return cropped_example

i = 0
root_folder = ".."
for kota in cities:
    print("process crop: "+kota+"...")
    city = kota
    pickle_files_loc = root_folder+"/pickles/"+city+"/"
    htmls_loc = root_folder+"/htmls/"+city+"/"
    pngs_loc = root_folder+"/pngs/"+city+"/"

    fl = []
    for name in glob.glob(pngs_loc+'/*.png'):
        f = name[len(pngs_loc):]
        cropped_example=get_crop(f)
        cropped_example.save(pngs_loc+f,format="PNG")
        fl.append(f)
        fl.sort()

    # to gif
    gif_name = city
    fps = 3
    loc_fl = [pngs_loc+f for f in fl]

    # here I use fl to create the sequence
    clip = mpy.ImageSequenceClip(loc_fl, fps=fps)
    clip.write_gif('{}.gif'.format(gif_name), fps=fps)
    print(gif_name+" created")