# FITS image viewer
An application that converts FITS format data often used in astronomical data analysis into images.
## Execution Environments
- Python3.7
- wxPython
- astropy
- numpy
- absl
- Sequence
- beautifulsoup4
- selenium

## Setup

### 1. Make config.ini file in current directory
```config.ini
[FitsImageViewer]
FITS_DIR = ${FITS_DATA_LOCATION}
FITS_FILE_NAME = ${FITS_FILE_NAME}
DIST_DIR = dist/
OUTPUT_FILE_NAME = fits.jpg

[SCRAGING]
URL = http://xxxx
REGISTER_ID = abc@gmail.com
```

### 2. Change virtual Python execution environment
```
$ conda activate python37
```

# Run
```
$ pythonw app.py
```