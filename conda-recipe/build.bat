@echo off
setlocal enabledelayedexpansion
set PY_VER=%PY_MAJOR%.%PY_MINOR%

:: Install from local wheels
@REM %PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels svgpathtools==1.6.1
%PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels varnaapi
@REM %PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels matplotlib==3.9.0
@REM %PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels tzdata
@REM %PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels PyQt6 PyQt6-sip PyQt6-Qt6
$PYTHON% -m pip install mariadb
$PYTHON% -m pip install snowflake-id
$PYTHON% -m pip install pysam

:: Install the package
%PYTHON% -m pip install . --no-deps --ignore-installed -vv

:: Rename the original script
rename "%PREFIX%\Scripts\dt-gui.exe" .dt-gui-real.exe

:: Create a launcher script wrapper (dt-gui.bat)
(
echo @echo off
echo set QT_QPA_PLATFORM_PLUGIN_PATH=%PREFIX%\Library\plugins\platforms
echo "%PREFIX%\Scripts\.dt-gui-real.exe" %%*
) > "%PREFIX%\Scripts\dt-gui.bat"
