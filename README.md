Arff2pat
========

Conversion of ARFF to PAT files read by JavaNNS.

This converter is a rough converter from .arff to .pat format.

By Emil Kjer


Data Mining software Weka by The Unifersity of Waikato
http://www.cs.waikato.ac.nz/ml/weka/


Neural Network simulator JavaNNS by Mathematich Naturwissenschaftliche Fakultat:
http://www.ra.cs.uni-tuebingen.de/downloads/JavaNNS/

## Usage

You'll need python on your system. To check, open a terminal and type ```python --version```

If you don't have python already installed, download [MiniConda](http://conda.pydata.org/miniconda.html) and install. 

Next you need to install the correct modules for python.

If you have conda, ```conda install click numpy scipy sklearn``` or otherwise, ```pip install click numpy scipy sklearn```

Either git clone or download this repositiory and from the directory you can run the following:

```chmod u+x arff2pat.py```

```./arff2pat.py``` or ```python arff2pat.py```

Enter the names of input arff file, output pat file and float values for the test split (e.g. 0.33 is 33% of full set goes to test set) and validation split.

```
./arff2pat.py --arff=weather.numeric.arff --pat=weather.numeric.pat --testsize=0.33 --validationsize=0.1
```

If test size is set to 0.0 it will only convert the supplied file directly to an equivalent pat file.

If test size is > 0.0, train, validation (if validation size > 0.0)  and test files will be generated.


## Edits / enhancements in this fork

* Edited to take in command line arguments (instead of hard coded paths etc.)
* Uses numpy and sklearn train_test_split to split the data (stratified)
