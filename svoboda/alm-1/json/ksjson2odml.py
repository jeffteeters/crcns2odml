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

map_file = "ks2odml_map.yaml"
# json_name = "data_structure_ANM221977_20140115.json"
json_name = "meta_data_ANM221977_20140115.json"
# test_file = "test_yaml_file.yaml"

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
	prop = odml.Property(name=name,
						  definition=definition,
						  values=values)
	section.append(prop)


def get_json_value(ksjson, json_path):
	# return value in object ksjson at json_path
	path_parts = json_path.split('/')
	obj = ksjson
	for i in range(len(path_parts) - 1):
		obj = obj[path_parts[i]]
	key = path_parts[-1]
	if key not in obj:
		print("path %s not found in json" % json_path)
		import pdb; pdb.set_trace()
	value = obj[key]
	return value


def add_odml_properties(root, json_name, ymap):
	ksjson = load_ksjson(json_name)
	property_info = ymap['odml_properties']
	for info in property_info:
		json_path = info["json_path"]
		odml_path = info["odml_path"]
		odml_info = info["odml_info"]
		print("\nadd property--")
		print("json_path=%s" % json_path)
		print("odml_path=%s" % odml_path)
		print("odml_info=%s" % odml_info)
		value = get_json_value(ksjson, json_path)
		property_path = odml_path.split('/')
		section = get_parent_section(root, property_path)
		property_name = property_path[-1]
		save_property(section, property_name, value, odml_info)
	base_name = json_name[0:-5]
	odml.save(root, base_name, "xml")


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


def load_yaml():
	global map_file
	with open(map_file, 'r') as stream:
		ymap = yaml.safe_load(stream)
	print("loaded map is:")
	pp.pprint(ymap)
	return ymap

def main():
	global json_name
	ymap = load_yaml()
	root = make_odml_root()
	create_odml_sections(root, ymap)
	add_odml_properties(root, json_name, ymap)

if __name__ == "__main__":
	main()

