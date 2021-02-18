
attr='(c) <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors (c) <a href="http://cartodb.com/attributions">CartoDB</a>, CartoDB <a href ="http://cartodb.com/attributions">attributions</a>'
from selenium import webdriver
import time
import os

city="bandung"
pickle_files_loc = "/root/pickles/"+city+"/"
htmls_loc = "/root/htmls/"+city+"/"
pngs_loc = "/root/pngs/"+city+"/"
ulbr = [-7.058949,107.358087,-6.809475,107.852472]
center = (-6.934228,107.605280)
time_delta = 7
zoom_start = 12

cities = ["bandung", "malang", "jakarta", "singapore", "surabaya"]
ulbrs = [[-7.058949,107.358087,-6.809475,107.852472], 
        [-8.044023,112.510911,-7.909893,112.758103],
        [-6.281836,106.585229,-6.070211,107.071031],
        [1.240877,103.568692,1.473241,104.054494],
        [-7.353130,112.493300,-7.141971,112.979102]]
centers = [(-6.934228,107.605280),
            (-7.976964,112.633906),
            (-6.176034,106.828130),
            (1.357061,103.811593),
            (-7.246360,112.737753)]

webdriver_loc = '/Users/basnugroho/python-projects/chromedriver'
htmls_root_file = 'file:///Users/basnugroho/python-projects/htmls/'

def screenshot(html_file):
    base  = htmls_loc
    delay=1
    browser = webdriver.Chrome(webdriver_loc)
    browser.get(htmls_root_file+city+"/"+html_file)

    time.sleep(delay)
    browser.save_screenshot(pngs_loc+html_file.replace("html","png"))
    browser.quit()

i = 0
root_folder = ".."
for kota in cities:
    print("process screenshot: "+kota+"...")
    city = kota
    pickle_files_loc = root_folder+"/pickles/"+city+"/"
    htmls_loc = root_folder+"/htmls/"+city+"/"
    pngs_loc = root_folder+"/pngs/"+city+"/"
    ulbr = ulbrs[i]
    center = centers[i]

    i = 0
    files_num = len([name for name in os.listdir(htmls_loc)])
    for f in os.listdir(htmls_loc):
        screenshot(f)
        if os.path.exists(htmls_loc+"/"+f):
            # os.remove(htmls_loc+"/"+f)
            print(htmls_loc+"/"+f+" captured")
            i += 1
            print("progress done: "+str(i)+"/"+str(files_num))
        else:
            print(htmls_loc+"/"+f+" does not exist")


