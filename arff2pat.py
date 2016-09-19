#!/usr/bin/env python

PAT_FILE_CONTENT = """SNNS pattern definition file V3.2
generated at Mon Apr 25 15:58:23 1994

No. of patterns : {data_length}
No. of input units : {inputs}
No. of output units : {outputs}

{data}
"""

import click

@click.command()
@click.option('--arff', prompt='ARFF file', help='The input ARFF file')
@click.option('--pat', prompt='Output pat file', help='The output PAT file')
def convert(arff, pat):
	""" Converts arff file to pat file for moving data between weka and javanns """
	## process arff file contents
	with open(arff) as infile:
		attributes = [] ## we assume the last attribute is alwys the class
		data_found = False
		data = []

		line_num = 0
		for line in infile:
			line_num+=1
			print(line_num)
			print(line)
			if data_found:
				print("Data found")
				data.append(line.strip())
				continue
			if line.upper().startswith("@ATTRIBUTE"):
				print("Attribute")
				attr = {}
				if     'real' in line \
					or 'REAL' in line \
					or 'numeric' in line \
					or 'NUMERIC' in line:
					
					values = line.split(' ')
					print("Values...")
					print(values)
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
						print("Category: %s" % category)
						attr['values'].append({ 'code': str(i), 'orig': category.strip() })
						i+=1	
				print(attr)
				attributes.append(attr)
			if line.upper().startswith("@DATA"):
				print("Data decorator found")
				data_found = True
				continue


	print(attributes)
	print(data)

	encoded_data = []
	## encode data
	for d in data:
		fields = d.split(',')
		for i in range(0, len(fields)):
			if attributes[i]['type'] == 'CATEGORICAL':
				for code in attributes[i]['values']:
					if fields[i].strip() == code['orig']: 
						fields[i] = code['code']
		encoded_data.append(" ".join(fields))	

	
	data_length = len(encoded_data)
	number_attributes = len(attributes)
	inputs = number_attributes - 1
	outputs = len(attributes[number_attributes-1]['values'])
	with open(pat, 'w') as outfile:
		encoded_data = "\n".join(encoded_data)
		outfile.write(PAT_FILE_CONTENT.format(data_length=data_length, \
						inputs=inputs,outputs=outputs,data=encoded_data))

if __name__ == '__main__':
    convert()
