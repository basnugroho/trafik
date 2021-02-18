import os
import subprocess
import datetime as dt
import time

cities = ["bandung", "malang", "jakarta", "singapore", "surabaya", "yogyakarta"]

root_folder = ".."
i = 0
for kota in cities:
    city = kota
    htmls_loc = root_folder+"/htmls/"+city+"/"
    pngs_loc = root_folder+"/root/pngs/"+city+"/"
    print(htmls_loc)
    begin_time = dt.datetime.now()
    pickle_count = 0
    total_files = len([name for name in os.listdir(htmls_loc)])
    for f in os.listdir(htmls_loc):
        if os.path.exists(htmls_loc+f):
            input = city+"/"+f
            pngs_loc = "/Users/basnugroho/python-projects/pngs/"+city+"/"
            output = pngs_loc+f.replace("html","png")
            # print("input: "+input)
            # print("output: "+output)
            # os.system("python ./convert.py "+input+" "+output)
            subprocess.run(["./convert.py", input, output])
            pickle_count+=1
            time.sleep(0.1) 
            print(city+" processing: "+str(pickle_count)+"/"+str(total_files)+" files executed")
    print(city+" done, "+str(pickle_count)+" files executed")
            
