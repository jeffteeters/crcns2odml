# crcns2odml

This repository contains tools to convert metadata for data sets stored in CRCNS.org
to the odML format.  The tools include:

* convertSvobda2json.m
  A MATLAB script to convert matlab files stored using the Svoboda lab
  format to JSON format.

* json2odml.py
  A Python program to convert files in json format to odML.  Each conversion
  requires a map file, which specifies the map between contents in the json
  file and the location (sections and properties) in the odML file.  An example
  map file is "ksjson2odml.yaml" in the svoboda/alm-1/json directory.
  Running the command without arguments displays the usage information.

* fetch_datacite.py
  A Python program to fetch the DataCite metadata descriptions for CRCNS.org
  data sets which are registered at DataCite.  The retrieved metadata files
  can be converted to odML format using the odmlimportdatacite command
  which is part of the odML tools which are available at: https://github.com/G-Node/odmltools
 
  Usage information about odmlimportdatacite is displayed using the --help option.

 