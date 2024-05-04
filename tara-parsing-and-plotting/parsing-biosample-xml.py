#!/usr/bin/env python

import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description = "This script parses a biosample XML file from NCBI and extracts specific data into a table.")

# Add argument for the XML file
parser.add_argument("-i", "--input-xml-file", help = "Path to the XML file")

# Add optional argument for the output file
parser.add_argument("-o", "--output-file", help = "Output tsv file name (default: biosample-data.tsv)", default = "biosample-data.tsv")

# Parse arguments
args = parser.parse_args()

# Path to your XML file
xml_file = args.input_xml_file

# initializing empty lists to hold wanted data
accessions = []
SRA_IDs = []
sample_names = []
sample_stations = []
latitudes = []
longitudes = []
marine_regions = []
local_scale_env_contexts = []
biomes = []
sampling_dates = []
depths = []
temperatures = []
chlorophyll_sensors = []
nitrate_sensors = []
oxygen_sensors = []
salinity_sensors = []
size_fraction_lower_thresholds = []
size_fraction_upper_thresholds = []
sample_material_labels = []
depth_indicators = []

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Iterate through each BioSample
for biosample in root.findall('BioSample'):

    accession = biosample.attrib.get('accession')
    marine_region = "NA"  # Default value
    local_scale_env_context = "NA"  # Default value
    sample_material_label = "NA"  # Default value
    depth_indicator = "NA"  # Default value

    # Extract Ids
    for ids_elem in biosample.findall('Ids'):
        for id_elem in ids_elem.findall('Id'):
            if id_elem.attrib.get('db') == "SRA":
                SRA_ID = id_elem.text

    # Extract Attributes
    for attr_elem in biosample.findall('Attributes/Attribute'):
        key = attr_elem.attrib.get('attribute_name')
        value = attr_elem.text

        if key == "sample name":
            sample_name = value
        elif key == "sampling station":
            sample_station = value
        elif key == "latitude start":
            latitude = value
        elif key == "longitude start":
            longitude = value
        elif key == "marine region":
            marine_region = value
        elif key == "environment (feature)":
            local_scale_env_context = value
        elif key == "environment (biome)":
            biome = value
        elif key == "event date/time start":
            initial_sampling_date = value
            try:
                initial_sampling_date_formatted = datetime.strptime(initial_sampling_date, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                initial_sampling_date_formatted = datetime.strptime(initial_sampling_date, "%Y-%m-%dT%H:%M")
            sampling_date = initial_sampling_date_formatted.strftime("%d-%b-%Y")
        elif key == "depth":
            depth = value
        elif key == "temperature":
            temperature = value
        elif key == "Chlorophyll Sensor":
            chlorophyll_sensor = value
        elif key == "nitrate sensor":
            nitrate_sensor = value
        elif key == "oxygen sensor":
            oxygen_sensor = value
        elif key == "Salinity Sensor":
            salinity_sensor = value
        elif key == "size fraction lower threshold":
            size_fraction_lower_threshold = value
        elif key == "size fraction upper threshold":
            size_fraction_upper_threshold = value
        elif key == "sample material label":
            sample_material_label = value
            depth_indicator = sample_material_label.split("_")[2]
        else:
            pass  # Ignore other attributes

    if depth_indicator == "NA":
        if local_scale_env_context == "deep chlorophyll maximum layer (ENVO:xxxxxxxx)":
            depth_indicator = "DCM"
        elif local_scale_env_context == "mesopelagic zone (ENVO:00000213)" or local_scale_env_context == "mesopelagic zone (ENVO:00000213) & marine oxygen minimum zone (ENVO:01000065)":
            depth_indicator = "MES"
        elif local_scale_env_context == "surface water layer (ENVO:00002042)":
            depth_indicator = "SRF"
        elif local_scale_env_context == "marine epipelagic mixed layer (ENVO:xxxxxxxxx)":
            depth_indicator = "MIX"
        else:
            depth_indicator = "NA"
    
    # appending extracted data to respective lists
    accessions.append(accession)
    SRA_IDs.append(SRA_ID)
    sample_names.append(sample_name)
    sample_stations.append(sample_station)
    latitudes.append(latitude)
    longitudes.append(longitude)
    marine_regions.append(marine_region)
    local_scale_env_contexts.append(local_scale_env_context)  # Append here
    biomes.append(biome)
    sampling_dates.append(sampling_date)
    depths.append(depth)
    temperatures.append(temperature)
    chlorophyll_sensors.append(chlorophyll_sensor)
    nitrate_sensors.append(nitrate_sensor)
    oxygen_sensors.append(oxygen_sensor)
    salinity_sensors.append(salinity_sensor)
    size_fraction_lower_thresholds.append(size_fraction_lower_threshold)
    size_fraction_upper_thresholds.append(size_fraction_upper_threshold)
    sample_material_labels.append(sample_material_label)
    depth_indicators.append(depth_indicator)

# making a DataFrame from the extracted data
data = {
    "accession": accessions,
    "SRA_id": SRA_IDs,
    "sample_name": sample_names,
    "sampling_station": sample_stations,
    "latitude": latitudes,
    "longitude": longitudes,
    "marine_region": marine_regions,
    "local_scale_env_context": local_scale_env_contexts,
    "biome": biomes,
    "sampling_date": sampling_dates,
    "depth_meters": depths,
    "temperature_celsius": temperatures,
    "chlorophyll_sensor": chlorophyll_sensors,
    "nitrate_sensor": nitrate_sensors,
    "oxygen_sensor": oxygen_sensors,
    "salinity_sensor": salinity_sensors,
    "lower_size_fraction_um": size_fraction_lower_thresholds,
    "upper_size_fraction_um": size_fraction_upper_thresholds,
    "sample_material_label": sample_material_labels,
    "depth_indicator": depth_indicators
}

df = pd.DataFrame(data)

df.to_csv(args.output_file, sep="\t", index=False)
