#!/bin/bash

# Install from local wheels
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels svgpathtools==1.6.1
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels varnaapi
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels matplotlib==3.9.0
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels tzdata
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels pyqt6
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels pyqt6-sip

# Install the package using pip
$PYTHON -m pip install . --no-deps --ignore-installed -vv
