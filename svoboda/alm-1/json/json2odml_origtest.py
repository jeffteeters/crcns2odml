import odml
import glob, os
import datetime as dt
import sys


# pp = pprint.PrettyPrinter(indent=4)
# pp = pprint.PrettyPrinter(indent=4, width=120, depth=None, stream=None, compact=True)

# display metadata in json files


def make_odml(file_base=None, meta=None, ds_meta=None):
	# make odml file from (dictionary) stored in meta and ds_meta
	MYodML = odml.Document(author='Jeff Teeters',
				version=0.1,
				date=dt.date.today(),
				# repository="http://crcns.org"  # meant to be repository of terms
				);
	sec1 = odml.Section(name="TheCrew",
				definition="Information on the crew",
				type="crew")
	MYodML.append(sec1)

	sec2 = odml.Section(name="Arthur Philip Dent",
				definition="Information on Arthur Dent",
				type="crew/person",
				parent=sec1)

	prop1 = odml.Property(name="Gender",
 				definition="Sex of the subject",
				values="male")

	MYodML['TheCrew']['Arthur Philip Dent'].append(prop1)

	prop2 = odml.Property(name="NameCrewMembers",
				definition="List of crew members names",
				values=["Arthur Philip Dent",
					"Teeters, Jeff",
 					"Zaphod Beeblebrox",
					"Tricia Marie McMillan",
					"Ford Prefect"],
				dtype=odml.DType.person)
	MYodML['TheCrew'].append(prop2)

	# site_location = [[2.5, -1.2, 0.577], [2.5, -1.2, 0.477], [2.5, -1.2, 0.377]];

	site_locations = odml.Property(name="siteLocations")
	# site_locations.dtype = "3-tuple"
	site_locations.dtype = "3-tuple"
	site_locations.values = ["(2.5; -1.2; 0.577)", "(2.5; -1.2; 0.477)", "(2.5; -1.2; 0.377)"];
	print("site_locations = %s\n" % site_locations.values )
	MYodML['TheCrew'].append(site_locations)

	site_locations2 = odml.Property(name="SiteLocations2",
                          definition="Locations of recording electrodes",
                          values=["(2.5; -1.2; 0.577)", "(2.5; -1.2; 0.477)", "(2.5; -1.2; 0.377)"],
                          dtype="3-tuple")
	MYodML['TheCrew'].append(site_locations2)

	print("site_locations after append = %s\n" % site_locations.values )
	print("direct access site_locations: %s\n" % MYodML['TheCrew'].properties['siteLocations'])
	# import pdb; pdb.set_trace()

	# prop2.append("Blind Passenger")

	save_to = 'myodml2'
	# odml.save(MyodML, save_to, "yaml")
	odml.save(MYodML, save_to, "xml")
	sys.exit("done saving sample odML file")

	# write contents to file

	# output_file = "pprint_" + file_base + ".txt";
	# with open(output_file, 'w') as fp:
	# 	fp.write("metadata for %s\n---------\n\n" % file_base)
	# 	fp.write(" from %s\n" % file)
	# 	fp.write(meta_pp);
	# 	fp.write("--------------------------------\n\n from %s\n\n" % ds_file);
	# 	fp.write(ds_meta_pp);
def process_files():
	for file in glob.glob("meta_data*.json"):
		ds_file = file.replace("meta_data", "data_structure");
		assert os.path.isfile(ds_file), "could not file file %s" % ds_file
		# now load the files, convert to json
		fp = open(file,mode='r');
		contents = fp.read();
		fp.close()
		meta = json.loads(contents);
		# data structures file
		fp = open(ds_file,mode='r');
		contents = fp.read();
		fp.close()
		ds_meta = json.loads(contents);
		file_base = file.replace("meta_data_", "");
		file_base = file_base.replace(".json", "");
		make_odml(file_base, meta, ds_meta);

def main():
	make_odml()

main()
