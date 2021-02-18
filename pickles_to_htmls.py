import pandas as pd
import numpy as np
import datetime as dt
import geopandas as gpd
from shapely.geometry import Point, LineString,Polygon
import matplotlib.pyplot as plt
import os
import folium
attr='(c) <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors (c) <a href="http://cartodb.com/attributions">CartoDB</a>, CartoDB <a href ="http://cartodb.com/attributions">attributions</a>'
import time
from pyproj import Proj, CRS,transform

#e4326=Proj(init='epsg:4326')
e4326=CRS('EPSG:4326')
#e3857=Proj(init='epsg:3857')
e3857=CRS('EPSG:3857')

class Projection:
    '''
    helper to project lat/lon values to map
    '''
    #e4326=Proj(init='epsg:4326')
    e4326=CRS('EPSG:4326')
    #e3857=Proj(init='epsg:3857')
    e3857=CRS('EPSG:3857')

    @staticmethod
    def wgsToXy(lon,lat):
        t1=transform(Projection.e4326,Projection.e3857, lon,lat)
        #t2=transform(Proj('epsg:4326'), Proj('epsg:3857'), lon,lat)
        return t1

    @staticmethod
    def pointToXy(point):
        xy=point.split(",")
        return Projection.wgsToXy(float(xy[0]),float(xy[1]))

city=""
pickle_files_loc = "/root/pickles/"+city+"/"
htmls_loc = "/root/htmls/"+city+"/"
pngs_loc = "/root/pngs/"+city+"/"
ulbr = [0,0,0,0]
center = (0,0)
time_delta = 7
zoom_start = 12

# define a function to get important information from HERE Maps API output
def get_resume(data):
    data=data['RWS'][0]
    rws=data['RW']
    fis=[x['FIS'][0]['FI'] for x in rws]
    fisis = [direction for subfis in fis for direction in subfis]
    JFS = [x['CF'][0]['JF'] for x in fisis]
    IDS = [str(x['TMC']['PC'])+x['TMC']['QD'] for x in fisis]
    LIS = [x['LI'] for x in rws]
    SHPS = [x['SHP'] for x in fisis]
    FCS = [np.mean([x['FC'] for x in y]) for y in SHPS]
    SHPS_string=["".join(list(np.array([x['value'] for x in shp]).flatten())) for shp in SHPS]
    df = pd.DataFrame({'JF':JFS,
                       #'SU':SUS,
                       'FC':FCS,'ID':IDS,'shape':SHPS_string})
    return df

# define a function to plot lines on folium and save it as HTML
def plot_folium(tes, fname, center, zoom_start, save=True):
    m=folium.Map(center, zoom_start=zoom_start,
                tiles="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_nolabels/{z}/{x}/{y}.png",
                #tiles = "https://{s}.basemaps.cartocdn.com/base-dark/{z}/{x}/{y}.png",
                 attr=attr)
    color={2:'#069E2D',0:'#034732',1:'#008148',3:'#F5BB00',4:'#FB5012'}
    style_function = lambda x: {
        'color' : color[x['properties']['group']],
        'weight' : 5/x['properties']['FC']
    }
    tes_=tes
    for wi in np.sort(tes['FC'].unique())[::-1]:
            for c in np.sort(tes['group'].unique()):
                the_df=tes_[(tes_['FC']==wi)&(tes_['group']==c)]
                if len(the_df)==0:
                    continue
                else:
                    folium.GeoJson(the_df, style_function=style_function).add_to(m)
    if save==True:
        m.save(fname)
    else:
        return m

def process_to_html(fname1, time_delta, pickles_loc, htmls_loc, center, zoom_start):
    time1 = dt.datetime.strptime(fname1.split(".")[0], "%Y-%m-%d %H-%M-%S") + dt.timedelta(hours=time_delta)
    data1 = pd.read_pickle(os.path.join(pickles_loc, fname1))
    res1 = get_resume(data1)
    res1['group'] = pd.cut(res1.JF, [-1, 1, 3, 4, 8, 11]).cat.codes
    tes = pd.merge(gdf_ok, res1[['ID', 'JF', 'group']], on="ID")
    plot_folium(tes, os.path.join(htmls_loc, str(time1).replace(":", "-") + ".html"), center, zoom_start)
    return tes

cities = ["bandung", "malang", "jakarta", "singapore", "surabaya", "yogyakarta"]
ulbrs = [[-7.058949,107.358087,-6.809475,107.852472], 
        [-8.044023,112.510911,-7.909893,112.758103],
        [-6.281836,106.585229,-6.070211,107.071031],
        [1.239993,103.563487,1.473044,104.054782],
        [-7.353130,112.493300,-7.141971,112.979102],
        [-7.859463,110.241654,-7.743984,110.487302]]
centers = [(-6.934228,107.605280),
            (-7.976964,112.633906),
            (-6.176034,106.828130),
            (1.357061,103.811593),
            (-7.246360,112.737753),
            (-7.801727,110.364478)]

root_folder = ".."
remove_pickles = True
i = 0
for kota in cities:
    print("process "+kota)
    city = kota
    pickle_files_loc = root_folder+"/pickles/"+city+"/"
    htmls_loc = root_folder+"/htmls/"+city+"/"
    pngs_loc = root_folder+"/pngs/"+city+"/"
    ulbr = ulbrs[i]
    center = centers[i]
    i += 1

    files = os.listdir(pickle_files_loc)

    pickle_count = 0
    begin_time = dt.datetime.now()
    for file in files:
        fname1 = file
        print(fname1)
        if(len(fname1)) > 19:
            time1 = dt.datetime.strptime(fname1.split(".")[0], "%Y-%m-%d %H-%M-%S") + dt.timedelta(hours=time_delta)  # +14 because I live in PST
            data1 = pd.read_pickle(os.path.join(pickle_files_loc, fname1))
            res1 = get_resume(data1)
            gdf = res1[['ID', 'shape', 'FC']].copy()
            gdf['geometry'] = gdf['shape'].apply(lambda s: LineString(map(lambda x: Point(eval(x)[::-1]),s.strip().split(" "))))
            gdf = gpd.GeoDataFrame(gdf)
            gdf.crs = {'init': 'epsg:4326'}
            gdf.head()
            res1['group'] = pd.cut(res1.JF, [-1, 1, 3, 4, 8, 11]).cat.codes
            u, l = ulbr[0], ulbr[1]
            b, r = ulbr[2], ulbr[3],
            x = [l, r, r, l]
            y = [b, b, u, u]
            bound = Polygon([[px, py] for px, py in zip(x, y)])
            bd = gpd.GeoDataFrame(pd.Series([bound]).reset_index().rename(columns={0: 'geometry'}))
            bd.crs = {'init': 'epsg:4326'}
            gdf_ok = gpd.sjoin(gdf, bd)
            process_to_html(fname1, time_delta, pickle_files_loc, htmls_loc, center, zoom_start)
            pickle_count += 1
            if os.path.exists(pickle_files_loc+fname1) and remove_pickles == True:
                os.remove(pickle_files_loc+fname1)
                print(pickle_files_loc+fname1+" deleted")
            else:
                print(pickle_files_loc+fname1+" does not exist")
    print(city+": "+str(dt.datetime.now() - begin_time))
    print(city+" done, "+str(pickle_count)+" files executed")