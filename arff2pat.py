#!/usr/bin/python


PAT_FILE_CONTENT = 
"""
SNNS pattern definition file V3.2
generated at Mon Apr 25 15:58:23 1994

No. of patterns : {data_length}
No. of input units : {inputs}
No. of output units : {outputs}

{data}
"""

import click

@click.command()
@click.option('--arff', help='The input ARFF file')
@click.option('--pat', help='The output PAT file')
@click.option('--target', help='The name of the class variable')
@click.option('--train', help='Size of train split')
@click.option('--test', help='Size of test split')
@click.option('--validate', help='Size of validate split')
@click.option('--split', help='Split data true/false')
def convert(arff, pat, target, train, test, validate, split):
	""" Converts arff file to pat file for moving data between weka and javanns """

	split_data_bool = (split == "true")
	split_sizes = {'train' : int(train), 'test' : int(test), 'validate' : int(validate)}

	with open(arff) as infile:
		attribute_count = 0
		output_count = 0
		data_found = False
		data = []

		
		for line in infile:
			if data_found:
				data.append(line.strip())
				continue
			if line.strip()[0] == '%':
				continue
			if len(line.strip()) == 0:
				continue
			if line.startswith("@ATTRIBUTE {target}".format(target=target)):
				## get number of output units
				line = line.strip()
				classes = line[line.index('{'):-1]
				classes = classes.split(',')
				output_count = len(classes)
			if line.startswith("@ATTRIBUTE"):
				if '{' in line:
					## need to encode
					line = line.strip()
					non_numerics = line[line.index('{'}:-1]
					non_numerics = non_numerics.split(',')
					
					
				attribute_count+=1
			if line.startswith("@DATA"):
				data_found = True
				continue

	with open(pat, 'w') as outfile:
		data = "\n".join(data)
		data = data.replace(","," ")
		data.replace("TRUE",1)
		data.replace("FALSE",0)
		data.replace('yes', 1)
		data.repalce('no', 0)
		outfile.write(file_content.format(data_length=data_length, inputs=inputs,outputs=outputs,data=data)

			
def parse_attributes(data_string_raw):
  #Clean the raw string for spaces
  data_string = data_string_raw.replace(' ', '')
  #Clean the raw string for newlines
  data_string = data_string.rstrip('\n')

  #The string can either be a real value or a touple
  if data_string.startswith('real') or data_string.startswith('numeric'):
    return data_string
  else:
    #Get the values in the string by splitting between {} and split by ,
    s_touple = data_string.split('{', 1)[1].split('}')[0]
    s_array = s_touple.split(',')
    return s_array


def shuffle_list(list_raw):
  import random
  list_shuffled = random.shuffle(list_raw, random.random)
  return list_raw

def split_data(data_list_raw, split_sizes):
  #To get train, test and validation data split it in defined sizes
  #Update, we need to stratisfy the data and will do that with Weka
  train_list = data_list_raw[:split_sizes['train']:]

  test_from = split_sizes['train']
  test_to = split_sizes['train']+split_sizes['test']
  test_list = data_list_raw[test_from:test_to]

  validate_from = test_to
  validate_to = test_to+split_sizes['validate']
  validate_list = data_list_raw[validate_from: validate_to]

  data_split_dict = {'train' : train_list,
                     'test' : test_list, 
                     'validate' : validate_list}
  return data_split_dict

def find_touple_index(value, array):
  #Get the index value in an array
  return array.index(value)

def return_binary_array(true_index, in_array):
  #Translate and convert to binary array
  bin_array = []
  for index, val in enumerate(in_array):
    if index != true_index:
      bin_array.append(0)
    else:
      bin_array.append(1)
  return bin_array

def find_and_return_bin_array(value, in_array):
  #Get a binary value based on a value in an array
  array_index = find_touple_index(value, in_array)
  return return_binary_array(array_index, in_array)


def translate_list_to_binary(data_list_raw, array_list):
  data_list_translated = []
  for data_cur in data_list_raw:
    data_list_cur = []
    bad_line = False
    for i, att in enumerate(array_list):
      val = data_cur[i]

      print "String: " + str(data_cur)
      if len(data_cur) ==0:
        print "blah"
        break
      elif len(data_cur[0]) == 0:
        print "bloh"
        break



      #make sure the value is not a question mark
      #REMARK this is a decision based on the data
      if val == '?':
        # data_list_cur.append(val)
        # The line is invalid and should be skipped
        bad_line = True

      elif att == 'real' or att == 'numeric':
        #Keep numeric values
        print val
        print att
        data_list_cur.append(float(val))

      else:
        #Convert attributes of arrays to binary values.
        #REMARK this can be done differently
        val_translated = find_and_return_bin_array(val, att)
        val_trans_clean = convert_list_to_string(val_translated)
        data_list_cur.append(val_trans_clean)
    #If something is wrong with the line, skip it...
    if bad_line:
      continue
    data_list_translated.append(data_list_cur)
  return data_list_translated




###################
##   EXECUTION   ##
###################

file_location = file_base_dir + arff_name_in + '.arff'
file_raw = read_file(file_location)
file_dict = substract_information_from_file(file_raw)
file_raw.close()

#Get the data and attributes as out
data_list = file_dict['list_data']
attributes_list = file_dict['list_attributes']

#Translate the data to binary values
data_list = translate_list_to_binary(data_list, attributes_list)

if split_data_bool:
  #Save the data for test, train and validation

  #shuffle the data
  shuffle_list(data_list)

  data_dict = split_data(data_list, split_sizes)
  #As an excample print the test data:
  #print data_dict['test']

  #### TRAIN FILE ####
  content_dict['data'] = data_dict['train']
  content_dict['no_of_patterns'] = split_sizes['train']
  out_name = '-train'
  save_file_to_pat(content_dict,
              file_base_dir_out, arff_name_in,
              out_name)

  #### TEST FILE ####
  content_dict['data'] = data_dict['test']
  content_dict['no_of_patterns'] = split_sizes['test']
  out_name = '-test'
  save_file_to_pat(content_dict,
              file_base_dir_out, arff_name_in,
              out_name)

  #### VALIDATE FILE ####
  content_dict['data'] = data_dict['validate']
  content_dict['no_of_patterns'] = split_sizes['validate']
  out_name = '-validate'  
  save_file_to_pat(content_dict,
              file_base_dir_out, arff_name_in,
              out_name)

#We need something down here
else:
  #save with normal parameters
  content_dict['no_of_patterns'] = len(data_list)
  content_dict['data'] = data_list
  out_name = ''
  save_file_to_pat(content_dict,
              file_base_dir_out, arff_name_in,
              out_name)
