import requests
import json
import time

def get_json_from_bbox(min_lat, min_lon, max_lat, max_lon):
    url = f"https://opencellid.org/ajax/getCells.php?bbox={min_lon},{min_lat},{max_lon},{max_lat}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Assuming the response is in JSON format
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print("Error occurred while making the request:", e)
        return None

def save_data_to_geojson(json_data, filename):
    if json_data and 'features' in json_data and json_data['features']:
        with open(filename, 'a') as f:
            for feature in json_data['features']:
                geojson_feature = {
                    "type": "Feature",
                    "geometry": feature["geometry"],
                    "properties": feature["properties"]
                }
                f.write(json.dumps(geojson_feature) + '\n')

def main():
    min_lat, max_lat = 36.0, 42.0
    min_lon, max_lon = 26.0, 45.0
    lat_step, lon_step = 0.012, 0.008
    data_filename = "data.json"
    total_features = 0
    
    total_steps = int((max_lat - min_lat) / lat_step) * int((max_lon - min_lon) / lon_step)
    current_step = 0
    
    for lat in range(int(min_lat * 1000), int(max_lat * 1000), int(lat_step * 1000)):
        for lon in range(int(min_lon * 1000), int(max_lon * 1000), int(lon_step * 1000)):
            min_lat_val = lat / 1000
            max_lat_val = min_lat_val + lat_step
            min_lon_val = lon / 1000
            max_lon_val = min_lon_val + lon_step
            
            json_data = get_json_from_bbox(min_lat_val, min_lon_val, max_lat_val, max_lon_val)
            if json_data:
                save_data_to_geojson(json_data, data_filename)
                total_features += len(json_data['features'])
            else:
                print(f"No JSON data for {min_lat_val},{min_lon_val},{max_lat_val},{max_lon_val}")
            
            current_step += 1
            progress_percentage = (current_step / total_steps) * 100
            print(f"Progress: {current_step}/{total_steps} ({progress_percentage:.2f}%) - Total Features: {total_features}")
            
            time.sleep(1)  # Add a small delay to avoid overwhelming the server

    print("Data retrieval and saving completed!")

if __name__ == "__main__":
    main()
