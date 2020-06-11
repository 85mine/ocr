# OCR Sample
Detects and Recognizes text in an image or pdf

Tested on macOS

## Prerequisites

### poetry
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
## brew
* tesserocr
* poppler



## Installation

```
poetry install
```


## Running

* How to use
```
poetry run python tessaractocr/run.py --help`
```

Usage: 

```
run.py [OPTIONS]

Options:
  --input TEXT   Input file (only support PNG/JPEG/PDF)
  --output TEXT  Output text file
  --verbose      Verbose mode - output detailed logs
  --help         Show this message and exit.
```

* Example
```
poetry run python tessaractocr/run.py --input=samples/test.pdf --output=output.text --verbose
```

## Format coding style
```
poetry run yapf -i -vv tessaractocr/run.py

poetry run isort -ac tessaractocr/run.py
```

