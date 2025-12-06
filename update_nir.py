import json

def get_centroid_lon(polygon):
    """Calculates the approximate longitude centroid of a polygon to determine its position."""
    # Polygon structure in GeoJSON is usually [ [ [x,y], [x,y]... ] ]
    # We take the first ring [0]
    total_lon = 0
    count = 0
    for point in polygon[0]:
        total_lon += point[0]
        count += 1
    return total_lon / count if count > 0 else 0

def get_centroid_lat(polygon):
    """Calculates approximate latitude."""
    total_lat = 0
    count = 0
    for point in polygon[0]:
        total_lat += point[1]
        count += 1
    return total_lat / count if count > 0 else 0

def process_geojson(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    new_nir_polygons = []
    
    # 1. Prepare Lists for the updated coordinates of the old regions
    updated_ph06_coords = [] # Western Visayas (minus Negros Occ)
    updated_ph07_coords = [] # Central Visayas (minus Negros Or & Siquijor)

    # 2. Iterate through features to find PH06 and PH07
    for feature in data['features']:
        
        # --- PROCESS WESTERN VISAYAS (PH06) ---
        if feature['properties']['id'] == 'PH06':
            print("Processing Western Visayas...")
            # PH06 contains Panay (West) and Negros Occidental (East)
            # Dividing line is roughly Longitude 122.75
            
            for polygon in feature['geometry']['coordinates']:
                lon = get_centroid_lon(polygon)
                
                if lon > 122.75:
                    # This is Negros Occidental -> Move to NIR
                    new_nir_polygons.append(polygon)
                else:
                    # This is Panay/Guimaras -> Keep in PH06
                    updated_ph06_coords.append(polygon)
            
            # Update PH06 geometry in place
            feature['geometry']['coordinates'] = updated_ph06_coords

        # --- PROCESS CENTRAL VISAYAS (PH07) ---
        elif feature['properties']['id'] == 'PH07':
            print("Processing Central Visayas...")
            # PH07 contains Negros Oriental (West), Siquijor (South-West), Cebu/Bohol (East)
            # Dividing line for Negros Oriental is roughly Longitude < 123.45
            # Siquijor is typically Lat < 9.35 and Lon < 123.7
            
            for polygon in feature['geometry']['coordinates']:
                lon = get_centroid_lon(polygon)
                lat = get_centroid_lat(polygon)

                is_negros_or = lon < 123.45 and lat > 9.0
                is_siquijor = lat < 9.35 and lon < 123.7

                if is_negros_or or is_siquijor:
                    # Move to NIR
                    new_nir_polygons.append(polygon)
                else:
                    # Keep Cebu/Bohol in PH07
                    updated_ph07_coords.append(polygon)

            # Update PH07 geometry in place
            feature['geometry']['coordinates'] = updated_ph07_coords

    # 3. Create the New NIR Feature
    if new_nir_polygons:
        print(f"Creating NIR with {len(new_nir_polygons)} polygons found.")
        nir_feature = {
            "type": "Feature",
            "properties": {
                "source": "Generated from split of PH06/PH07",
                "id": "PH18",
                "name": "Negros Island Region"
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": new_nir_polygons
            },
            "id": 18 # You may need to ensure this ID doesn't conflict with others
        }
        data['features'].append(nir_feature)
    else:
        print("Error: Could not isolate Negros polygons. Check input coordinate system.")

    # 4. Save the file
    output_filename = 'ph_updated_nir.json'
    with open(output_filename, 'w') as f:
        json.dump(data, f)
    
    print(f"Success! File saved as {output_filename}")

# Run the function
# Ensure 'ph.json' is in the same folder as this script
try:
    process_geojson('ph.json')
except FileNotFoundError:
    print("Please make sure your file is named 'ph.json' and is in the same folder.")