@echo off
title Natural Core IA - Sincronizador GitHub
color 0A
echo ============================================
echo     NATURAL CORE IA - GITHUB SYNC
echo ============================================
echo.

setlocal
cd /d "E:\projetos\natural core"

echo [INFO] Atualizando repositório remoto...
git pull origin main
echo.

echo [INFO] Adicionando novos arquivos...
git add .
echo.

echo [INFO] Commitando alterações...
git commit -m "Sincronização automática do HUD v5.3"
echo.

echo [INFO] Enviando atualizações...
git push origin main
echo.

echo ============================================
echo   Sincronização concluída com sucesso!
echo ============================================
pause
exit