# MRC_reader
Program for opening mrc files.
## Install
Tested with Python version 3.8.13

Create [Conda](https://docs.conda.io/en/latest/miniconda.html) environment:

``` 
conda create -n mrc_reader 
conda activate mrc_reader
pip install -r requirements.txt
```

## Build

Create standalone program using:
``` 
pyinstaller --onefile mrcread.py
```
