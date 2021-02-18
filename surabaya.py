import urllib.request
import json
import pickle
import datetime as dt

def get_traffic():
    apiKey = ""
    bbox = "-7.353130,112.493300;-7.141971,112.979102"
    center = (-7.246360,112.737753)
    fname=str(dt.datetime.now())[:19].replace(":","-")
    base="https://traffic.ls.hereapi.com/traffic/6.2/flow.json"+\
    "?apiKey="+apiKey+\
    "&bbox="+bbox+\
    "&responseattributes=sh,fc"
    print(base)
    try:
        response = urllib.request.urlopen(base)
        data=json.load(response)
        with open("./pickles/surabaya/"+fname+".p", 'wb') as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
        print("Success "+fname)
    except:
        print("Failed "+fname)

if __name__=="__main__":
  get_traffic()
