@echo off 
title Instalador Natural Core IA 
color 0b 
echo Instalando dependencias Python... 
pip install --upgrade pip 
pip install pillow matplotlib reportlab pyautogui gitpython 
echo Sincronizando com GitHub... 
"E:\Git\bin\git.exe" add . 
"E:\Git\bin\git.exe" commit -m "Atualizacao automatica v4.6" 
"E:\Git\bin\git.exe" push origin main 
echo Iniciando HUD... 
python "hud\hud_interface_v4_6.py" 
pause 
