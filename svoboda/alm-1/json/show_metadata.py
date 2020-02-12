import json
import pprint
# pp = pprint.PrettyPrinter(indent=4)
pp = pprint.PrettyPrinter(indent=4, width=120, depth=None, stream=None, compact=True)

# display metadata in json files
import glob, os
for file in glob.glob("meta_data*.json"):
	ds_file = file.replace("meta_data", "data_structure");
	print(file)
	assert os.path.isfile(ds_file), "could not file file %s" % ds_file
	print(ds_file)
	# now load the files, convert to json
	fp = open(file,mode='r');
	contents = fp.read();
	fp.close()
	meta = json.loads(contents);
	meta_pp = pp.pformat(meta);
	# data structures file
	fp = open(ds_file,mode='r');
	contents = fp.read();
	fp.close()
	ds_meta = json.loads(contents);
	ds_meta_pp = pp.pformat(ds_meta);

	# write contents to file
	file_base = file.replace("meta_data_", "");
	file_base = file_base.replace(".json", "");
	output_file = "pprint_" + file_base + ".txt";
	with open(output_file, 'w') as fp:
		fp.write("metadata for %s\n---------\n\n" % file_base)
		fp.write(" from %s\n" % file)
		fp.write(meta_pp);
		fp.write("--------------------------------\n\n from %s\n\n" % ds_file);
		fp.write(ds_meta_pp);	
