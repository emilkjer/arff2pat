#!/usr/bin/env python

"""
Converts ARFF (weka) files into .pat (javanns) files

Each nominal attribute and class label is mapped to a N-width binary string
  where N is the number of possible values for that attribute/class label.
Numeric attributes are used as input directly.
Numerical class labels are scaled to [0,1]

Usage:
chmod u+x arff2pat.py
./arff2pat.py

Without command line arguments, it will prompt you for inputs
Otherwise, see ./arff2pat.py --help for information

Refer to https://github.com/maree-s3596596/arff2pat/blob/master/README.md for
more information

"""

import click
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler

PAT_FILE_CONTENT = """SNNS pattern definition file V3.2
generated at Mon Apr 25 15:58:23 1994

No. of patterns : {data_length}
No. of input units : {inputs}
No. of output units : {outputs}
{data}
"""

NUMERIC_ATTRIBUTE_TYPES = ['real','REAL','numeric','NUMERIC']

def encode_nominal(num_values, flag_index):
    code = ['0'] * num_values  # init
    code[flag_index] = '1'
    return " ".join(code)

@click.command()
@click.option('--arff', prompt='ARFF file', help='The input ARFF file')
@click.option('--pat', prompt='Output pat file', help='The output PAT file')
@click.option('--testsize', prompt='Test set size float between 0.0,1.0',
              help='The size of the test set as float between 0.0,1.0',
              default=0.33)
@click.option('--validationsize',
              prompt='Validation set size (between 0.0,1.0)',
              help='The size of the validation set as float between 0.0,1.0',
              default=0.33)
def convert(arff, pat, testsize,validationsize):
    """
    Converts arff file to pat file for moving data
    between weka and javanns
    """

    testsize = float(testsize)
    validationsize = float(validationsize)
    outputs = 0  # number of output attributes (n-width)
    attributes = []  # we assume the last output-n-attributes is alwys the class
    data_found = False
    data = []
    rows_with_missing_data = 0

    # process arff file contents
    with open(arff) as infile:

        line_num = 0
        for line in infile:
            line_num += 1
            # ignore comments
            if line.strip().startswith('%'):
                continue
            # if we're in the data section
            if data_found:
                # ignore lines with missing values
                if '?' in line:
                    rows_with_missing_data += 1
                else:
                    data.append(line.strip())
                continue
            # if we're dealing with an attribute definition
            if line.upper().startswith("@ATTRIBUTE"):
                attr = {}
                # if its numeric we can just use the values straight
                # (we will deal with scaling numeric class later on)
                if any(t in line for t in NUMERIC_ATTRIBUTE_TYPES):
                    values = line.split()
                    attr['name'] = values[1].strip()
                    attr['type'] = values[2].strip().upper()
                    attr['values'] = [{}]
                    outputs = 1
                # else if the line contains { it is nominal so we need to encode
                # into an N-length string binary form
                elif '{' in line:
                    line = line.strip()
                    categories = line[line.index('{')+1:-1]
                    categories = categories.split(',')
                    attr['name'] = line.split(' ')[1]
                    attr['type'] = 'NOMINAL'
                    attr['values'] = []
                    i = 0
                    for category in categories:
                        attr['values'].append({ 'code': i,
                                                'orig': category.strip() })
                        i += 1
                    outputs = i
                    for dic in attr['values']:
                        dic['code'] = encode_nominal(outputs, dic['code'])
                attributes.append(attr)

            # if we've found the data section, set data_found flag
            if line.upper().startswith("@DATA"):
                data_found = True
                continue

    # encode the data
    encoded_data = []
    inputs = sum([len(attr['values']) for attr in attributes]) - outputs

    ## encode data
    for d in data:
        fields = d.split(',')
        for i in range(0, len(fields)):
            if attributes[i]['type'] == 'NOMINAL':
                for code in attributes[i]['values']:
                    if fields[i] == code['orig']:
                        fields[i] = code['code']

        encoded_data.append(fields)

    # if class variable is numeric, scale [0,1]
    if attributes[-1]['type'] != 'NOMINAL':
        encoded_data_np = np.array(encoded_data)
        class_vars = encoded_data_np[:,-1]
        min_max_scaler = MinMaxScaler()
        scaled_class_vars = min_max_scaler.fit_transform(class_vars.reshape(-1,1))
        encoded_data_np[:,-1] = scaled_class_vars.reshape(len(class_vars))
        encoded_data = encoded_data_np.tolist()

    if testsize > 0.0:

        do_validation_split = (validationsize > 0.0)

        arr = np.array(encoded_data)
        X, y = (arr[:,:-1], arr[:,-1])
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=testsize)
        # further split your train into validation if required
        if do_validation_split:
            X_train, X_valid, y_train, y_valid = \
                train_test_split(X_train, y_train,
                                test_size=validationsize)

        train = np.append(X_train, y_train.reshape(len(y_train),1),1)
        if do_validation_split:
            valid = np.append(X_valid, y_valid.reshape(len(y_valid),1),1)
        test = np.append(X_test, y_test.reshape(len(y_test),1),1)

        train_len = len(train)
        train = [" ".join(row) for row in train]
        train = "\n".join(train)

        if do_validation_split:
            valid_len = len(valid)
            valid = [" ".join(row) for row in valid]
            valid = "\n".join(valid)

        test_len = len(test)
        test = [" ".join(row) for row in test]
        test = "\n".join(test)

        train_file = pat.replace('.pat', '-train.pat')
        with open(train_file,'w') as outfile:
            outfile.write(PAT_FILE_CONTENT.format(data_length=train_len,
                                                  inputs=inputs,
                                                  outputs=outputs,
                                                  data=train))
        print("\n\nFile output to: %s (%d cases)" % (train_file, train_len))

        if do_validation_split:
            valid_file = pat.replace('.pat', '-valid.pat')
            with open(valid_file,'w') as outfile:
                outfile.write(PAT_FILE_CONTENT.format(data_length=valid_len,
                                                      inputs=inputs,
                                                      outputs=outputs,
                                                      data=valid))
            print("\n\nFile output to: %s (%d cases)" % (valid_file, valid_len))

        test_file = pat.replace('.pat', '-test.pat')
        with open(test_file, 'w') as outfile:
            outfile.write(PAT_FILE_CONTENT.format(data_length=test_len,
                                                  inputs=inputs,
                                                  outputs=outputs,
                                                  data=test))
        print("\n\nFile output to: %s (%d cases)" % (test_file, test_len))

    else: # no splitting required
        data_length = len(encoded_data)
        with open(pat, 'w') as outfile:
            encoded_data = "\n".join(encoded_data)
            outfile.write(PAT_FILE_CONTENT.format(data_length=data_length,
                                                  inputs=inputs,
                                                  outputs=outputs,
                                                  data=encoded_data))

        print("\n\nFile output to: %s" % pat)

    print("\nDiscarded %d cases with missing data" % rows_with_missing_data)
    print("\nNumber of inputs: %d" % inputs)
    print("\nNumber of outputs: %d" % outputs)
    print("\nAttribute encoding (the last listed is the class label)")

    for attribute in attributes:
        print(attribute['name'])
        if attribute['type'] == 'NOMINAL':
            for value in attribute['values']:
                    print("\t%s -> %s" % (value['orig'], value['code']))
        else:
            print("\t%s" % attribute['type'])

if __name__ == '__main__':
    convert()
