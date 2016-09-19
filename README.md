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

```pip install click numpy scipy sklearn```

```chmod u+x arff2pat.py```

```./arff2pat.py``` or ```python arff2pat.py```

Enter the names of input arff file, output pat file and the float value of the test split (e.g. 0.33 is 33% of full set goes to test set).

```
./arff2pat.py --arff=weather.numeric.arff --pat=weather.numeric.pat --testsize=0.33
```

If test size is set to 0.0 it will only convert the supplied file directly to an equivalent pat file.

If test size is > 0.0, train, validation and test files will be generated.


## Edits

Edited to take into command line arguments (instead of hard coded paths)
