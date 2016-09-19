#!/usr/bin/python

PAT_FILE_CONTENT = """SNNS pattern definition file V3.2
generated at Mon Apr 25 15:58:23 1994

No. of patterns : {data_length}
No. of input units : {inputs}
No. of output units : {outputs}

{data}
"""

#@click.option('--train', help='Size of train split')
#@click.option('--test', help='Size of test split')
#@click.option('--validate', help='Size of validate split')
#@click.option('--split', help='Split data true/false')

import click

@click.command()
@click.option('--arff', help='The input ARFF file')
@click.option('--pat', help='The output PAT file')
def convert(arff, pat, target, train, test, validate, split):
	""" Converts arff file to pat file for moving data between weka and javanns """

	## process arff file contents
	with open(arff) as infile:
		attributes = [] ## we assume the last attribute is alwys the class
		data_found = False
		data = []

		for line in infile:
			if data_found:
				data.append(line.strip())
				continue
			if line.startswith("@ATTRIBUTE"):
				attr = {}
				if 'real' in line or 'REAL' in line or 'numeric' in line or 'NUMERIC':
					values = line.split(' ')
					attr['name'] = values[1].strip()
					attr['type'] = values[2].strip().upper()
				elif '{' in line:
					## need to encode
					line = line.strip()
					categories = line[line.index('{'):-1]
					categories = categories.split(',')
					attr['name'] = line.split(' ')[1]
					attr['type'] = 'CATEGORICAL'
					attr['values'] = []
					i = 0
					for category in categories:
						attr['values'].append({ 'code': i, 'orig': category.strip() })
						i+=1	
				attributes.append(attr)
			if line.startswith("@DATA"):
				data_found = True
				continue

	encoded_data = []
	## encode data
	for d in data:
		fields = data.split(',')
		for i in range(0, len(fields)):
			if attributes[i]['type'] == 'CATEGORICAL':
				for code in attributes[i]['values']:
					if fields[i].strip() == code['orig']: fields[i] = code['code']
		encoded_data.append(" ".join(fields))	

	
	data_length = len(encoded_data)
	inputs = len(attributes) - 1
	outputs = len(attributes[-1]['values'])
	with open(pat, 'w') as outfile:
		encoded_data = "\n".join(encoded_data)
		outfile.write(PAT_FILE_CONTENT.format(data_length=data_length, inputs=inputs,outputs=outputs,data=encoded_data))
