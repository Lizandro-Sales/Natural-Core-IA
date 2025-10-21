@echo off 
title Instalador Natural Core IA v4.7 
color 0b 
echo Instalando dependencias... 
pip install --upgrade pip 
pip install pillow matplotlib reportlab pyautogui gitpython 
echo Atualizando via GitHub... 
powershell -Command "Invoke-WebRequest 'https://api.github.com/repos/Lizandro-Sales/Natural-Core-IA/contents/' -OutFile update_info.json" 
echo Iniciando HUD... 
python "hud\hud_interface_v4_7.py" 
pause 
