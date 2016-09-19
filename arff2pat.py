#!/usr/bin/env python

import click
import numpy as np
from sklearn.cross_validation import train_test_split

PAT_FILE_CONTENT = """SNNS pattern definition file V3.2
generated at Mon Apr 25 15:58:23 1994

No. of patterns : {data_length}
No. of input units : {inputs}
No. of output units : {outputs}
{data}
"""

@click.command()
@click.option('--arff', prompt='ARFF file', help='The input ARFF file')
@click.option('--pat', prompt='Output pat file', help='The output PAT file')
@click.option('--testsize', prompt='Test set size [0.0,1.0]', help='The size of the test set as a float [0.0,1.0]')
def convert(arff, pat, testsize):
	""" Converts arff file to pat file for moving data between weka and javanns """
	## process arff file contents
	with open(arff) as infile:
		attributes = [] ## we assume the last attribute is alwys the class
		data_found = False
		data = []

		line_num = 0
		for line in infile:
			line_num+=1
			if data_found:
				data.append(line.strip())
				continue
			if line.upper().startswith("@ATTRIBUTE"):
				attr = {}
				if     'real' in line \
					or 'REAL' in line \
					or 'numeric' in line \
					or 'NUMERIC' in line:
					
					values = line.split(' ')
					attr['name'] = values[1].strip()
					attr['type'] = values[2].strip().upper()
				elif '{' in line:
					## need to encode
					line = line.strip()
					categories = line[line.index('{')+1:-1]
					categories = categories.split(',')
					attr['name'] = line.split(' ')[1]
					attr['type'] = 'CATEGORICAL'
					attr['values'] = []
					i = 0
					for category in categories:
						attr['values'].append({ 'code': str(i), 'orig': category.strip() })
						i+=1	
				attributes.append(attr)
			if line.upper().startswith("@DATA"):
				data_found = True
				continue


	encoded_data = []
	## encode data
	for d in data:
		fields = d.split(',')
		for i in range(0, len(fields)):
			if attributes[i]['type'] == 'CATEGORICAL':
				for code in attributes[i]['values']:
					if fields[i].strip() == code['orig']: 
						fields[i] = code['code']
		encoded_data.append(fields)

	testsize = float(testsize)
	number_attributes = len(attributes)
	inputs = number_attributes - 1
	outputs = len(attributes[number_attributes-1]['values'])
	
	if testsize	> 0.0:
		arr = np.array(encoded_data)
		X, y = (arr[:,:-1], arr[:,-1])
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testsize)
		## further split your train into validation
		X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, \
																test_size=testsize)
		
		
		train = np.append(X_train, y_train.reshape(len(y_train),1),1)
		valid = np.append(X_valid, y_valid.reshape(len(y_valid),1),1)
		test = np.append(X_test, y_test.reshape(len(y_test),1),1)

		train_len = len(train)
		train = [" ".join(row) for row in train]
		train = "\n".join(train)

		valid_len = len(valid)
		valid = [" ".join(row) for row in valid]
		valid = "\n".join(valid)

		test_len = len(test)
		test = [" ".join(row) for row in test]
		test = "\n".join(test)
				
		train_file = pat.replace('.pat', '.train.pat')
		with open(train_file,'w') as outfile:
			outfile.write(PAT_FILE_CONTENT.format(data_length=train_len, \
                        inputs=inputs,outputs=outputs,data=train))
		print("\n\nFile output to: %s (%d cases)" % (train_file, train_len))

		valid_file = pat.replace('.pat', '.valid.pat')
		with open(valid_file,'w') as outfile:
			outfile.write(PAT_FILE_CONTENT.format(data_length=valid_len, \
                        inputs=inputs,outputs=outputs,data=valid))
		print("\n\nFile output to: %s (%d cases)" % (valid_file, valid_len))

		test_file = pat.replace('.pat', '.test.pat')
		with open(test_file, 'w') as outfile:
			outfile.write(PAT_FILE_CONTENT.format(data_length=test_len, \
                        inputs=inputs,outputs=outputs,data=test))
		print("\n\nFile output to: %s (%d cases)" % (test_file, test_len))

	else:
		data_length = len(encoded_data)
		with open(pat, 'w') as outfile:
			encoded_data = "\n".join(encoded_data)
			outfile.write(PAT_FILE_CONTENT.format(data_length=data_length, \
						inputs=inputs,outputs=outputs,data=encoded_data))

		print("\n\nFile output to: %s" % pat)
	print("\nAttribute encoding")
	class_variable_index = number_attributes - 1
	for attribute in attributes:
		print(attribute['name'])
		if attribute['type'] == 'CATEGORICAL':
			for value in attribute['values']:
					print("\t%s -> %s" % (value['orig'], value['code']))

if __name__ == '__main__':
    convert()
