@echo off
title ⚙ Natural Core IA - Build VisualSync v4.8+
color 0A
cls

echo ===========================================================
echo     🚀 INICIANDO COMPILACAO NATURAL CORE IA v4.8+
echo ===========================================================

:: CONFIGURAÇÕES BASE
setlocal enabledelayedexpansion
set "ROOT=E:\projetos\natural core"
set "ZIP_NAME=NaturalCoreIA.zip"
set "EXE_NAME=NaturalCoreIA.exe"
set "GIT_DIR=%ROOT%"
set "PYTHON=C:\Python312\python.exe"

:: LIMPA TEMPORÁRIOS
echo.
echo [INFO] Limpando temporários...
del /Q "%ROOT%\temp" >nul 2>&1

:: GERA O ZIP
echo.
echo [INFO] Compactando arquivos em "%ZIP_NAME%"...
"E:\7-Zip\7z.exe" a -tzip "%ROOT%\%ZIP_NAME%" "%ROOT%\core" "%ROOT%\assets" "%ROOT%\configs" "%ROOT%\hud" "%ROOT%\logs" -mx9

:: GERA O EXECUTÁVEL SFX
if exist "%ROOT%\7zS.sfx" (
    echo [INFO] Gerando instalador autoextraível "%EXE_NAME%"...
    copy /b "%ROOT%\7zS.sfx" + "%ROOT%\config.txt" + "%ROOT%\%ZIP_NAME%" "%ROOT%\%EXE_NAME%" >nul
    echo [OK] Instalador gerado com sucesso: "%EXE_NAME%"
) else (
    echo [ERRO] O arquivo 7zS.sfx nao foi encontrado em "%ROOT%".
)

:: LOG LOCAL
set "DATESTAMP=%date:~6,4%-%date:~3,2%-%date:~0,2%"
set "LOGFILE=%ROOT%\logs\build_%DATESTAMP%.log"
echo Build executado em %DATESTAMP% > "%LOGFILE%"

:: --- SINCRONIZAÇÃO AUTOMÁTICA COM GITHUB ---
echo.
echo ===========================================================
echo [GIT] Sincronizando com GitHub...
echo ===========================================================

cd "%GIT_DIR%"
git add .
git commit -m "Build automatica [%DATESTAMP%]"
git pull --no-edit origin main
git push -u origin main

if %errorlevel%==0 (
    echo [OK] Projeto sincronizado com sucesso com o GitHub.
) else (
    echo [ERRO] Falha durante o push para o GitHub.
)

echo ===========================================================
echo [FIM] Build finalizada com sucesso.
echo ===========================================================
pause
exit