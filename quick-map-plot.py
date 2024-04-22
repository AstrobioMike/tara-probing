#!/usr/bin/env python

import pandas as pd
import folium
import argparse

parser = argparse.ArgumentParser(description = "Ad hoc map maker.")

# Add argument for the XML file
parser.add_argument("-i", "--input-table", help = "Path to the input table made by the parsing-biosample-xml.py script.")

# Add optional argument for the output file
parser.add_argument("-o", "--output-html-file", help = "Output html file name (default: sampling-map.tsv)", default = "sampling-map.tsv")

# Parse arguments
args = parser.parse_args()

# Load the data
data = pd.read_csv(args.input_table, sep='\t')

# Subset the data to keep only one row for each unique 'sampling_station' value
# data = data.drop_duplicates(subset='sampling_station')

# Create a map centered around the mean of latitudes and longitudes
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2, tiles = 'cartodb positron', max_bouns = True)

# Add markers for each location
for idx, row in data.iterrows():
    popup_content = f"Station: {row['sampling_station']}<br><br>Date sampled: {row['sampling_date']}<br><br>Depth: {row['depth_meters']}<br><br>Depth indicator: {row['depth_indicator']}"
    folium.Marker(location=[row['latitude'], row['longitude']], popup=popup_content).add_to(m)

# Save the map to an HTML file
m.save(args.output_html_file)
