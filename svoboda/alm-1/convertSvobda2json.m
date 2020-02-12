function [] = convertSvobda2json()
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
global obj meta_data
data_dir = 'data_structure_ANM221977';
meta_dir = 'meta_data_files';
out_dir = 'json';
% Check to make sure that both folders actually exist.
if ~isdir(data_dir)
  error('Error: The following folder does not exist:\n%s', data_dir);
end
if ~isdir(meta_dir)
  error('Error: The following folder does not exist:\n%s', meta_dir);
end
% Get a list of all files in the data_dir with the desired file name pattern.
filePattern = fullfile(data_dir, '*.mat');
theFiles = dir(filePattern);
for k = 1 : length(theFiles)
  baseFileName = theFiles(k).name;
  fullFileName = fullfile(data_dir, baseFileName);
  fprintf(1, 'Now reading %s\n', fullFileName);
  fprintf(1, 'baseFileName is %s\n', baseFileName);
  meta_name = strrep(baseFileName,'data_structure','meta_data');
  full_meta_name = fullfile(meta_dir, meta_name);
  fprintf(1, 'full_meta_name = %s\n', full_meta_name);
  if ~isfile(full_meta_name)
      error('Could not file %s\n', full_meta_name);
  end
  % Now it's verified that both data and meta data files exist,
  % convert to json and save in json directory
  % convert data_structure file
  load(fullFileName);
  clearEventSeriesHash_values();
  obj2 = jsonencode(obj);
  json_path = fullfile('json', strrep(baseFileName, '.mat', '.json'));
  fileID = fopen(json_path,'w');
  fprintf(fileID,"%s", obj2);
  fclose(fileID);
  % convert meta_data file
  load(full_meta_name);
  meta2 = jsonencode(meta_data);
  json_path = fullfile('json', strrep(meta_name, '.mat', '.json'));
  fileID = fopen(json_path,'w');
  fprintf(fileID,"%s", meta2);
  fclose(fileID);
end
end

