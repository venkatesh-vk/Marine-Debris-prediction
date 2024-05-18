import os
import json
import csv

# Specify the folder path containing JSON files
folder = 'jsondata'

# Create a list to store extracted data
data_list = []
t = 0
c = 0

# Iterate through folders
# Iterate through files in the folder
for filename in os.listdir(folder):
    t=0
    if filename.endswith('.json'):
        # Remove the ".json" extension from the filename
        filename_without_extension = os.path.splitext(filename)[0]

        # Extract longitude and latitude from the filename
        filename_parts = filename_without_extension.split('_')
        if len(filename_parts) == 2:
            longitude_str, latitude_str = filename_parts[0], filename_parts[1]

            # Convert strings to float values
            longitude = float(longitude_str)
            latitude = float(latitude_str)

            file_path = os.path.join(folder, filename)
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                for item in data.get("results", []):
                    attributes = item.get("attributes", {})
                    extracted_data = {
                        "longitude": longitude,
                        "latitude": latitude,
                        "layerName": attributes.get("layerName", ""),
                        "displayFieldName": attributes.get("displayFieldName", ""),
                        "value": attributes.get("value", ""),
                        "author": attributes.get("author", ""),
                        "year": attributes.get("year", ""),
                        "title": attributes.get("title", ""),
                        "doi": attributes.get("doi", ""),
                        "habitat": attributes.get("habitat", ""),
                        "unit": attributes.get("unit", ""),
                        "Plastic": attributes.get("Plastic", ""),
                        "Other": attributes.get("Other", ""),
                        "N/A": attributes.get("N/A", ""),
                        "shape": attributes.get("shape", ""),
                        "objectid": attributes.get("objectid", ""),
                        "gis_value": attributes.get("gis_value", ""),
                        "org_habitat": attributes.get("org_habitat", ""),
                        "analysis_method": attributes.get("analysis_method", ""),
                        "final_value": attributes.get("final_value", ""),
                        "no_litter": attributes.get("no_litter", ""),
                        "size": attributes.get("size", ""),
                        "sizes": attributes.get("sizes", ""),
                        "types": attributes.get("types", ""),
                        "pub_date": attributes.get("pub_date", ""),
                        "loc_perc": attributes.get("loc_perc", ""),
                        "lit_date": attributes.get("lit_date", ""),
                        "lit_year": attributes.get("lit_year", "")
                    }
                    data_list.append(extracted_data)
                    t += 1
                    print(t, " rows completed in JSON")

            # Write the extracted data to a CSV file
            with open('output5.csv', 'a', newline='') as csv_file:
                fieldnames = ["layerName", "displayFieldName", "value", "author", "year", "title", "doi", "habitat",
                              "unit",
                              "Plastic", "Other", "N/A", "shape", "objectid", "gis_value", "org_habitat",
                              "analysis_method",
                              "final_value", "no_litter", "size", "sizes", "types", "pub_date", "loc_perc",
                              "lit_date",
                              "lit_year", "longitude", "latitude"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                if c == 0:
                    writer.writeheader()
                writer.writerow(extracted_data)
                c += 1
                print(c, " rows completed in CSV")

print(f"CSV data saved to output.csv")
