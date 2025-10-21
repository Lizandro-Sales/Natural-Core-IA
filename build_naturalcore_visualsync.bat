@echo off
title 🌿 Natural Core IA - Build VisualSync v4.3
color 0A
cls
echo ===========================================================
echo       🌱 INICIANDO COMPILACAO NATURAL CORE IA v4.3
echo ===========================================================
echo.

:: ==== Diretórios base ====
setlocal enabledelayedexpansion
set "ROOT=E:\projetos\natural core"
set "ICON=%ROOT%\assets\icon_green_transparent.ico"
set "ZIP_NAME=NaturalCoreIA.zip"
set "EXE_NAME=NaturalCoreIA.exe"
set "LOG_DIR=%ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\build_!date:~6,4!-!date:~3,2!-!date:~0,2!.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: ==== Verifica 7-Zip ====
set "ZIP_EXE=E:\7-Zip\7z.exe"
if not exist "%ZIP_EXE%" (
    echo ❌ 7-Zip nao encontrado em "%ZIP_EXE%"
    echo Instale o 7-Zip ou atualize o caminho no script.
    pause
    exit /b
)

:: ==== Estrutura ====
echo 📁 Organizando estrutura...
if not exist "%ROOT%\assets" mkdir "%ROOT%\assets"
if not exist "%ROOT%\core" mkdir "%ROOT%\core"

:: ==== Limpeza ====
echo 🧹 Limpando arquivos temporarios...
del /Q "%ROOT%\temp\*" >nul 2>nul

:: ==== Compacta projeto ====
echo 📦 Compactando projeto em "%ZIP_NAME%" ...
"%ZIP_EXE%" a -tzip "%ROOT%\%ZIP_NAME%" "%ROOT%\core" "%ROOT%\assets" -mx9 >nul
echo ✅ Arquivo ZIP criado: "%ZIP_NAME%"

:: ==== Gera configuracao SFX ====
echo 🧠 Gerando instalador autoextraivel (%EXE_NAME%) ...
(
    echo ;!@Install@!UTF-8!
    echo Title="Natural Core IA - Setup"
    echo BeginPrompt="Deseja instalar o Natural Core IA?"
    echo RunProgram="setup.exe"
    echo Directory="NaturalCoreIA"
    echo GUIMode="2"
    echo ;!@InstallEnd@!
) > "%ROOT%\config.txt"

:: ==== Monta executavel ====
if exist "%ROOT%\7zS.sfx" (
    copy /b "%ROOT%\7zS.sfx" + "%ROOT%\config.txt" + "%ROOT%\%ZIP_NAME%" "%ROOT%\%EXE_NAME%" >nul
    echo ✅ Instalador gerado com sucesso!
) else (
    echo ❌ ERRO: O arquivo 7zS.sfx nao foi encontrado em "%ROOT%"
)

:: ==== Limpeza final ====
if exist "%ROOT%\config.txt" del "%ROOT%\config.txt"
echo 🧩 Limpando temporarios... concluido.

:: ==== Log ====
echo [%date% %time%] Build concluida >> "%LOG_FILE%"

echo ===========================================================
echo 💽 Instalador final: "%ROOT%\%EXE_NAME%"
echo 📦 Pacote ZIP: "%ROOT%\%ZIP_NAME%"
echo 🪶 Log salvo em: "%LOG_FILE%"
echo ===========================================================
echo.
pause
endlocal
exit /b