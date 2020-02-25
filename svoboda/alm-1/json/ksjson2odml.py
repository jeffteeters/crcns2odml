import odml
import glob, os
import datetime as dt
import sys
import yaml
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)



# script to convert json made from Svoboda lab Mat files to odML.
# uses map file "ks2odml_map.yaml" to specify map beteeen json and odml

default_map_file = "ks2odml_map.yaml"
# json_name = "data_structure_ANM221977_20140115.json"
default_input_file = "meta_data_ANM221977_20140115.json"

def make_odml_root():
	root = odml.Document(author='Jeff Teeters',
				version=0.1,
				date=dt.date(2020,2,10)
				);
	return root

def get_parent_section(root, property_path):
	# returns odML section to store property
	# root is root of odML object
	# property path is list of sections in path to property.  Name of 
	# property is the last component of the path
	section = root
	for i in range(len(property_path) - 1):
		child_sections = section.sections
		wanted_name = property_path[i]
		section_found = False
		for cs in child_sections:
			if cs.name == wanted_name:
				# found desired section
				section = cs
				section_found = True
				break
		if not section_found:
			# must create a new section
			print("Cound not find parent section for property: %s" % property_path)
			sys.exit("aborting")
			# section = odml.Section(name=wanted_name,
			# 			parent=section)
	return section

def create_odml_section(root, path, stype, definition):
	# create odML section
	# root is the odML root object
	path_parts = path.split('/')
	section = root
	section_found = True
	for i in range(len(path_parts) - 1):
		child_sections = section.sections
		wanted_name = path_parts[i]
		section_found = False
		for cs in child_sections:
			if cs.name == wanted_name:
				# found desired section
				section = cs
				section_found = True
				break
	if not section_found:
		print("Unable to find parent odML section for section %s" % path)
		sys.exit("aborting")
		# create a new section
	section = odml.Section(name=path_parts[-1], type=stype, definition=definition, 
						parent=section)


def save_property(section, name, values, odml_info):
	# save odml property in section section
	# odml_info is dictionary with keys:
	#  definition - definition
	definition = odml_info['definition']
	if 'dtype' in odml_info:
		dtype = odml_info["dtype"]
		if dtype[-6:] == "-tuple":
			# must convert values to form like: ["(1; 2)", "(3; 4)"]
			values = [ '(' + '; '.join(["%g" % x for x in v]) + ')'  for v in values]
	else:
		dtype = None
	try:
		prop = odml.Property(name=name,
						  definition=definition,
						  values=values,
						  dtype = dtype)
	except ValueError as e:
		print("unable to create property '%s'" % name)
		print("values=")
		pp.pprint(values)
		print("odML info=")
		pp.pprint(odml_info)
	else:
		section.append(prop)


def get_json_value(ksjson, json_path):
	# return value in object ksjson at json_path
	path_parts = json_path.split('/')
	obj = ksjson
	for i in range(len(path_parts) - 1):
		obj = obj[path_parts[i]]
	key = path_parts[-1]
	if key not in obj:
		# print("path %s not found in json" % json_path)
		value = None
	else:
		value = obj[key]
	return value


def add_odml_properties(root, json_name, ymap, output_directory):
	ksjson = load_ksjson(json_name)
	property_info = ymap['odml_properties']
	for info in property_info:
		json_path = info["json_path"]
		odml_path = info["odml_path"]
		odml_info = info["odml_info"]
		# print("\nadd property--")
		# print("json_path=%s" % json_path)
		# print("odml_path=%s" % odml_path)
		# print("odml_info=%s" % odml_info)
		value = get_json_value(ksjson, json_path)
		if value is None:
			# could not find this value in the json file, display a warning
			print("Warning: Could not find '%s' in JSON file.  Not including it in odML" % json_path)
			continue
		property_path = odml_path.split('/')
		section = get_parent_section(root, property_path)
		property_name = property_path[-1]
		save_property(section, property_name, value, odml_info)
	base_name = json_name[0:-5]
	if(output_directory is not None):
		output_path = os.path.join(output_directory, base_name)
	else:
		output_path = base_name
	odml.save(root, output_path, "xml")


def load_ksjson(json_name):
	# json_name = base_name + ".json"
	with open(json_name, 'r') as content_file:
		contents = content_file.read()
	ksjson = json.loads(contents)
	return ksjson

def create_odml_sections(root, ymap):
	# create the sections specified by the 'odML_sections' key
	sections_info = ymap['odml_sections']
	for si in sections_info:
		create_odml_section(root, si["path"], si["type"], si["definition"])


def load_yaml(map_file):
	with open(map_file, 'r') as stream:
		ymap = yaml.safe_load(stream)
	# print("loaded map is:")
	# pp.pprint(ymap)
	return ymap

def display_instructions():
	print("Usage:")
	print("%s <input_file> <map_file> [ <output_directory> ]" % sys.argv[0])
	print("Where:")
	print("<input_file> - json file containing metadata, or '-' for default file.")
	print("<map_file> - yaml file specifying map of data from json to odML, or '-' for default file.")
	print("<output_directory> - directory to store generated odML file.  Default is")
	print("    current directory.  File name will basename of <input_file> with extension '.xml'.")

def process_command_arguments():
	# return list of <input_file>, <map_file>, <output_directory>
	global default_input_file, default_map_file
	if(len(sys.argv) < 3 or len(sys.argv) > 4):
		display_instructions()
		sys.exit()
	input_file = sys.argv[1]
	if(input_file == '-'):
		input_file = default_input_file
		print("Using default input file: %s" % default_input_file)
	if not os.path.isfile(input_file):
		print("Input file %s not found." % input_file)
		sys.exit("Aborting")
	if not input_file.endswith(".json"):
		print("Input file '%s' must have extension .json" % input_file)
		sys.exit("Aborting.")
	map_file = sys.argv[2]
	if map_file == '-':
		map_file = default_map_file
		print("Using default map file: %s" % default_map_file)
	if not os.path.isfile(map_file):
		print("Map file %s not found." % map_file)
		sys.exit("Aborting.")
	if len(sys.argv) == 4:
		output_directory = sys.argv[3]
		if not os.path.isdir(output_directory):
			print("Output directory '%s' not found" % output_directory)
			sys.exit("Aborting.")
	else:
		output_directory = None  # use current directory
	return(input_file, map_file, output_directory)


def main():
	input_file, map_file, output_directory = process_command_arguments()
	ymap = load_yaml(map_file)
	root = make_odml_root()
	create_odml_sections(root, ymap)
	add_odml_properties(root, input_file, ymap, output_directory)

if __name__ == "__main__":
	main()

