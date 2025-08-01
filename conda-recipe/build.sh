#!/bin/bash
set -euxo pipefail

# Install from local wheels
$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels varnaapi
#$PYTHON -m pip install mariadb --no-index --find-links=$SRC_DIR/conda-recipe/wheels

if [[ "$(uname)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  #$PYTHON -m pip install --no-index --find-links=$SRC_DIR/conda-recipe/wheels PyQt6 PyQt6-sip PyQt6-Qt6
  #$PYTHON -m pip install $SRC_DIR/conda-recipe/wheels/mariadb-1.1.13.tar.gz
  #$PYTHON -m pip install snowflake-id --no-index --find-links=$SRC_DIR/conda-recipe/wheels
  #$PYTHON -m pip install pysam --no-index --find-links=$SRC_DIR/conda-recipe/wheels/pysam-0.23.3-cp39-cp39-macosx_11_0_arm64.whl
fi

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
