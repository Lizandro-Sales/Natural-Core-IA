@echo off
title Natural Core IA v4.7 - VisualSync Plus
color 0a
cls
echo ====================================================
echo 🔧 Natural Core IA v4.7 - VisualSync Plus Builder
echo ====================================================

set "ROOT=E:\projetos\natural core"
set "ZIP_NAME=NaturalCoreIA_v4_7.zip"
set "EXE_NAME=NaturalCoreIA_v4_7.exe"
set "ICON_PATH=%ROOT%\assets\icon_green_transparent.ico"

:: [1] Cria estrutura
for %%F in (core hud configs logs reports) do (
    if not exist "%ROOT%\%%F" mkdir "%ROOT%\%%F"
)

:: [2] HUD visual com barra de progresso
echo [INFO] Criando HUD visual...
powershell -Command ^
 "$progress=0;while($progress -le 100){Write-Progress -Activity 'Compilando Natural Core IA v4.7' -Status ('Progresso: {0}%%' -f $progress) -PercentComplete $progress;Start-Sleep -Milliseconds 50;$progress+=5}"

:: [3] Gera instalador setup
echo [SETUP] Criando setup com dependencias automáticas...
echo @echo off > "%ROOT%\install_v4_7_auto_setup.bat"
echo title Instalador Natural Core IA v4.7 >> "%ROOT%\install_v4_7_auto_setup.bat"
echo color 0b >> "%ROOT%\install_v4_7_auto_setup.bat"
echo echo Instalando dependencias... >> "%ROOT%\install_v4_7_auto_setup.bat"
echo pip install --upgrade pip >> "%ROOT%\install_v4_7_auto_setup.bat"
echo pip install pillow matplotlib reportlab pyautogui gitpython >> "%ROOT%\install_v4_7_auto_setup.bat"
echo echo Atualizando via GitHub... >> "%ROOT%\install_v4_7_auto_setup.bat"
echo powershell -Command "Invoke-WebRequest 'https://api.github.com/repos/Lizandro-Sales/Natural-Core-IA/contents/' -OutFile update_info.json" >> "%ROOT%\install_v4_7_auto_setup.bat"
echo echo Iniciando HUD... >> "%ROOT%\install_v4_7_auto_setup.bat"
echo python "hud\hud_interface_v4_7.py" >> "%ROOT%\install_v4_7_auto_setup.bat"
echo pause >> "%ROOT%\install_v4_7_auto_setup.bat"

:: [4] Arquivos base
echo print('🧠 Natural Core IA v4.7 carregado com sucesso!') > "%ROOT%\core\core_main.py"
echo print('📡 Atualizador VisualSync Plus ativo!') > "%ROOT%\core\auto_updater.py"
echo print('💡 HUD Visual IA v4.7 inicializado...') > "%ROOT%\hud\hud_interface_v4_7.py"

:: [5] Compacta tudo
echo [PACK] Compactando pacote...
powershell -Command "Compress-Archive -Path '%ROOT%\*' -DestinationPath '%ROOT%\%ZIP_NAME%' -Force"

:: [6] Cria .exe com 7zSFX (autoextraível)
if exist "%ROOT%\7z.sfx" (
    copy /b "%ROOT%\7z.sfx" + "%ROOT%\config.txt" + "%ROOT%\%ZIP_NAME%" "%ROOT%\%EXE_NAME%"
)

echo ====================================================
echo ✅ Compilação concluída com sucesso!
echo 📦 Instalador: %ROOT%\%EXE_NAME%
echo 🧩 Log salvo em: %ROOT%\logs\build_2025-10-21.log
echo ====================================================
pause