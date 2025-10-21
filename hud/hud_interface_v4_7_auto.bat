@echo off
title Natural Core IA v4.7.2 - AutoHUD Launcher
color 0a
echo =====================================================
echo       🚀 INICIANDO HUD VISUAL IA v4.7.2 PLUS
echo =====================================================
echo.

cd /d "%~dp0"
echo [INFO] Verificando dependências do Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado no sistema.
    pause
    exit /b
)

echo [INFO] Iniciando HUD Visual IA...
python hud_interface_v4_7.py
echo.
echo =====================================================
echo [FIM] HUD encerrado. Pressione qualquer tecla para sair.
pause >nul