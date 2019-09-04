@echo off
::--iter 20000
set PYTHONPATH=%PYTHONPATH%;.
where wtee.exe > nul
if %ERRORLEVEL% EQU 0 (
echo ***
echo *** Saving log to out\logs\train.log
echo ***
%FASTER_RCNN_HOME%\tools\train_net.py --solver .\models\zf_solver.prototxt --imdb gbr_train --cfg .\models\gbr_rcnn.yml 2>&1 | wtee out\logs\train.log
) else (
echo ***
echo *** Logging to console
echo ***
%FASTER_RCNN_HOME%\tools\train_net.py --solver .\models\zf_solver.prototxt --imdb gbr_train --cfg .\models\gbr_rcnn.yml
)
