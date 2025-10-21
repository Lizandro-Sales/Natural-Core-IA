@echo off
title Natural Core IA v4.6 - Instalador Automático
color 0a

echo [INFO] Preparando ambiente Natural Core IA v4.6...
cd /d "E:\projetos\natural core\"

REM === CRIA AS PASTAS PRINCIPAIS ===
mkdir core
mkdir hud
mkdir configs
mkdir logs
mkdir reports

REM === CRIA OS ARQUIVOS PADRÕES ===
echo { "auto_update": true, "hud_theme": "dark", "sync_interval": 24 } > "configs\config.json"

echo @echo off > install_v4_6_auto_setup.bat
echo title Instalador Natural Core IA >> install_v4_6_auto_setup.bat
echo color 0b >> install_v4_6_auto_setup.bat
echo echo Instalando dependencias Python... >> install_v4_6_auto_setup.bat
echo pip install --upgrade pip >> install_v4_6_auto_setup.bat
echo pip install pillow matplotlib reportlab pyautogui gitpython >> install_v4_6_auto_setup.bat
echo echo Sincronizando com GitHub... >> install_v4_6_auto_setup.bat
echo "E:\Git\bin\git.exe" add . >> install_v4_6_auto_setup.bat
echo "E:\Git\bin\git.exe" commit -m "Atualizacao automatica v4.6" >> install_v4_6_auto_setup.bat
echo "E:\Git\bin\git.exe" push origin main >> install_v4_6_auto_setup.bat
echo echo Iniciando HUD... >> install_v4_6_auto_setup.bat
echo python "hud\hud_interface_v4_6.py" >> install_v4_6_auto_setup.bat
echo pause >> install_v4_6_auto_setup.bat

REM === CRIA OS ARQUIVOS BASE DO CORE E HUD ===
echo print("🔧 Core IA v4.6 inicializado com sucesso!") > "core\core_main.py"
echo print("🧠 IA de diagnóstico ativa e sincronizada.") > "core\auto_diagnostic.py"
echo print("📊 HUD Visual IA v4.6 iniciado...") > "hud\hud_interface_v4_6.py"

REM === CRIA O ZIP AUTOEXECUTÁVEL ===
cd ..
powershell -Command "Compress-Archive -Path 'E:\projetos\natural core\*' -DestinationPath 'E:\projetos\natural_core_IA_v4_6_installer.zip' -Force"

echo.
echo ✅ Instalador gerado com sucesso em: E:\projetos\natural_core_IA_v4_6_installer.zip
pause