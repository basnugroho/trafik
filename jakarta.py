import urllib.request
import json
import pickle
import datetime as dt

def get_traffic():
    apiKey = ""
    bbox = "-6.281836,106.585229;-6.070211,107.071031"
    center = (-6.176034,106.828130)
    fname=str(dt.datetime.now())[:19].replace(":","-")
    base="https://traffic.ls.hereapi.com/traffic/6.2/flow.json"+\
    "?apiKey="+apiKey+\
    "&bbox="+bbox+\
    "&responseattributes=sh,fc"
    print(base)
    try:
        response = urllib.request.urlopen(base)
        data=json.load(response)
        # path_loc = os.path.abspath(os.path.join(__file__ ,"./cities/malang/"))
        with open("./pickles/jakarta/"+fname+".p", 'wb') as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
        print("Success "+fname)
    except:
        print("Failed "+fname)

if __name__=="__main__":
  get_traffic()
