#!/bin/bash
set -euxo pipefail

# Install from local wheels
#$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels svgpathtools==1.6.1
#$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels varnaapi
#$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels matplotlib==3.9.0
#$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels tzdata
#$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels PyQt6 PyQt6-sip PyQt6-Qt6

$PYTHON -m pip install --no-deps --ignore-installed \
    mariadb==1.1.10 \
    typing-extensions==4.12.1 \
    fsspec==2024.5.0 \
    pysam==0.23.0 \
    deprecated==1.2.14 \
    pygments==2.18.0 \
    matplotlib-venn==1.1.1 \
    platformdirs==4.2.2 \
    prompt-toolkit==3.0.47 \
    bcrypt==4.2.0 \
    snowflake-id==1.0.2 \
    stack_data==0.6.3 \
    rich==14.0.0 \
    sqlalchemy==2.0.36 \
    pure_eval==0.2.3 \
    cycler==0.12.1 \
    pluggy==1.6.0 \
    executing==2.0.1 \
    pycparser==2.22 \
    wrapt==1.16.0 \
    matplotlib-inline==0.1.7 \
    kiwisolver==1.4.5 \
    filelock==3.14.0 \
    mdurl==0.1.2 \
    markdown-it-py==3.0.0 \
    packaging==24.0 \
    asttokens==2.4.1 \
    sympy==1.12.1 \
    drawsvg==2.4.0 \
    PyQt6 \
    PyQt6-sip \
    PyQt6-Qt6 \
    tzdata \
    matplotlib==3.9.0 \
    varnaapi \
    svgpathtools==1.6.1


# Install the package using pip
$PYTHON -m pip install . --no-deps --ignore-installed -vv

# Rename the original executable installed by setup.py
mv "$PREFIX/bin/dt-gui" "$PREFIX/bin/.dt-gui-real"

PY_VER=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

cat > "$PREFIX/bin/dt-gui" <<EOF
#!/bin/bash

PLUGIN_CANDIDATES=(
  "\$CONDA_PREFIX/lib/python$PY_VER/site-packages/PyQt6/Qt6/plugins/platforms"
  "\$CONDA_PREFIX/lib/python$PY_VER/site-packages/PyQt6/Qt/plugins/platforms"
  "\$CONDA_PREFIX/Library/lib/python$PY_VER/site-packages/PyQt6/Qt6/plugins/platforms"
  "\$CONDA_PREFIX/Library/plugins/platforms"
)

for path in "\${PLUGIN_CANDIDATES[@]}"; do
  if [ -d "\$path" ]; then
    export QT_QPA_PLATFORM_PLUGIN_PATH="\$path"
    break
  fi
done

exec "\$CONDA_PREFIX/bin/.dt-gui-real" "\$@"
EOF

chmod +x "$PREFIX/bin/dt-gui"
