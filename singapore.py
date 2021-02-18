import urllib.request
import json
import pickle
import datetime as dt

def get_traffic():
    apiKey = ""
    bbox = "1.240877,103.568692;1.473241,104.054494"
    center = (1.357061,103.811593)
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
        with open("./pickles/singapore/"+fname+".p", 'wb') as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
        print("Success "+fname)
    except:
        print("Failed "+fname)

if __name__=="__main__":
  get_traffic()
