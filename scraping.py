import requests
import json

# Define the ranges of numbers
start_range_x = 180.0
end_range_x = -180.0
start_range_y = 85.0
end_range_y = -85.0

# Step size for iteration
step = 0.00000001

# Generate URLs and fetch/save data
for x in range(start_range_x,end_range_x + 0.00000001,0.00000001):
    for y in range(start_range_y,end_range_y + 0.00000001,0.00000001):
        
        url=f"https://maps.awi.de/services/projects/fram/litter_and_microplastic_distribution/wms/identify?layerTimeOptions=&maxAllowableOffset=&geometryPrecision=1&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&time=&returnGeometry=false&tolerance=10&mapExtent=-362.109375%2C-88.16750817509356%2C481.64062500000006%2C89.90823907909865&imageDisplay=1200%2C918%2C300&sr=EPSG%3A4326&layers=all%3A2&layerDefs=%7B%222%22%3A%22(lit_date%20%3E%3D%20%271960-01-01T00%3A00%3A00%27)%20AND%20(%20lit_date%20%3C%3D%20%272023-12-31T23%3A59%3A59%27)%22%7D&geometry={step * x:.17f}%2C{step * y:.17f}&geometryType=esriGeometryPoint&f=json"

        filename = f'{step * x:.17f}_{step * y:.17f}'
        
        print(f"Processing URL: {url}")
        
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.text
            with open(f'{filename}.txt', 'w') as txt_file:
                txt_file.write(data)
                
            try:
                json_data = response.json()
                with open(f'{filename}.json', 'w') as json_file:
                    json.dump(json_data, json_file, indent=4)
            except json.JSONDecodeError:
                print(f"JSON data not found in response for '{url}'. JSON file not created.")
        else:
            print(f"Ignoring invalid URL: '{url}'")

print("Data fetched and saved (ignoring invalid URLs).")
