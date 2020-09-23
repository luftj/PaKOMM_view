from flask import Flask, request
from flask_cors import CORS
import datetime
import json
from pyproj import CRS, Transformer

app = Flask(__name__)
CORS(app)

def xy_to_lonlat(x, y, utm_reference_point=[568303,5933799]):
    crs_geo = CRS.from_epsg(4326)
    crs_m = CRS.from_epsg(32632)
    proj_inv = Transformer.from_crs(crs_m, crs_geo)

    new_point_utm = (utm_reference_point[0] + x, utm_reference_point[1] + y)
    new_point_geo = proj_inv.transform(*new_point_utm) # returns lon, lat order

    return new_point_geo[::-1] # frontend expects lat, lon order

def add_feature(x,y, type_name):
    time = datetime.datetime.now().isoformat()
    coords = xy_to_lonlat(x,y)
    
    with open("data/features.json", encoding="utf-8") as file:
        json_data = json.load(file)

    max_id = json_data["features"][-1]["id"]
    new_feature = {
            "type": "Feature", 
            "id": max_id+1, 
            "geometry": {
                "type": "Point", 
                "coordinates": coords
            },
            "properties": {
                "type": type_name,
                "time": time
            }
    }
    json_data["features"].append(new_feature)

    with open("data/features.json", "w", encoding="utf-8") as file:
        json.dump(json_data, file)

@app.route('/send_data')
def send_data():
    x= float(request.args.get('pos_x').replace(",",".")) # fix float formatting
    y= float(request.args.get('pos_y').replace(",","."))
    t= request.args.get('type')
    print('success! got %s at (%f, %f)' % (t,x,y))
    add_feature(x,y,t)
    return 'success! got %s at (%f, %f)' % (t,x,y)

@app.route('/get_geojson')
def get_geojson():
    import json
    with open("data/features.json") as json_file:
        json_data = json.load(json_file)
    return json_data

@app.route('/test')
def test():
	return "test success"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
