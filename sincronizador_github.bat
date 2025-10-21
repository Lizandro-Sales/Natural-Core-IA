@echo off
title Natural Core IA - Sincronizador GitHub
color 0A
echo ============================================
echo        NATURAL CORE IA - GITHUB SYNC
echo ============================================
echo.

cd /d "E:\projetos\natural core"
if %errorlevel% neq 0 (
    echo [ERRO] Caminho do projeto nao encontrado!
    pause
    exit /b
)

echo [INFO] Atualizando repositório remoto...
git pull origin main
if %errorlevel% neq 0 echo [AVISO] Nenhuma atualização remota. & echo.

echo [INFO] Adicionando novos arquivos...
git add -A
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao adicionar arquivos!
    pause
    exit /b
)
echo.

echo [INFO] Commitando alterações...
git commit -m "Sincronização automática do HUD v5.3"
if %errorlevel% neq 0 (
    echo [AVISO] Nenhuma alteração nova para commit.
) else (
    echo [OK] Commit criado com sucesso.
)
echo.

echo [INFO] Enviando atualizações para o GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao enviar alterações!
) else (
    echo [SUCESSO] Sincronização concluída com sucesso!
)
echo ============================================
pause
exit