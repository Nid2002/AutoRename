@echo off
title AutoRename Phoenix - Build
color 0A

echo.
echo ============================================================
echo              AutoRename Phoenix v1.0.0
echo                   Build de Distribuicao
echo ============================================================
echo.

REM ------------------------------------------------------------
REM Limpando builds anteriores
REM ------------------------------------------------------------

echo [1/6] Limpando pastas...

if exist build (
    rmdir /S /Q build
)

if exist dist (
    rmdir /S /Q dist
)

if exist Release (
    rmdir /S /Q Release
)

echo.

REM ------------------------------------------------------------
REM Compilando
REM ------------------------------------------------------------

echo [2/6] Compilando executavel...
echo.

pyinstaller --clean AutoRename.spec

if errorlevel 1 (
    echo.
    echo ****************************************************
    echo ERRO: Falha durante a compilacao.
    echo ****************************************************
    pause
    exit /b 1
)

echo.

REM ------------------------------------------------------------
REM Criando Release
REM ------------------------------------------------------------

echo [3/6] Criando pasta Release...

mkdir Release

echo.

REM ------------------------------------------------------------
REM Copiando arquivos
REM ------------------------------------------------------------

echo [4/6] Copiando arquivos...

copy /Y dist\AutoRename.exe Release\
copy /Y config.ini Release\

if exist README.txt (
    copy /Y README.txt Release\
)

echo.

REM ------------------------------------------------------------
REM Criando estrutura
REM ------------------------------------------------------------

echo [5/6] Criando estrutura...

mkdir Release\Entrada
mkdir Release\Logs

echo.

REM ------------------------------------------------------------
REM Finalizado
REM ------------------------------------------------------------

echo [6/6] Build concluido.
echo.

echo ============================================================
echo               BUILD FINALIZADO COM SUCESSO!
echo ============================================================
echo.
echo Arquivos gerados em:
echo.
echo     Release\
echo.
echo Estrutura:
echo.
echo Release\
echo ├── AutoRename.exe
echo ├── config.ini
echo ├── README.txt
echo ├── Entrada\
echo └── Logs\
echo.

pause
