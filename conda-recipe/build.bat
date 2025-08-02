@echo off
setlocal enabledelayedexpansion
set PY_VER=%PY_MAJOR%.%PY_MINOR%

:: Install from local wheels
%PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels varnaapi
@REM %PYTHON% -m pip install --no-index --find-links=%SRC_DIR%\conda-recipe\wheels PyQt6 PyQt6-sip PyQt6-Qt6

%PYTHON% -m pip --no-index --find-links=%SRC_DIR%\conda-recipe\wheels pyqt6
%PYTHON% -m pip --no-index --find-links=%SRC_DIR%\conda-recipe\wheels pyqt6-sip
%PYTHON% -m pip --no-index --find-links=%SRC_DIR%\conda-recipe\wheels pyqt6-qt6

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
