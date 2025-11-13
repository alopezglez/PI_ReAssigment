@echo off
chcp 65001 >nul
title Ajuste de Facturas - Restaurante

echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo ▓▓▓                                                                         ▓▓▓
echo ▓▓▓                   SCRIPT DE AJUSTE DE REGISTROS PI                      ▓▓▓
echo ▓▓▓                                 v1.2                                    ▓▓▓
echo ▓▓▓                                                                         ▓▓▓
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo.

REM Verificar si Python está instalado
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo.
        echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        echo ▓▓▓           ERROR: Python no está instalado o no está en el PATH          ▓▓▓
        echo ▓▓▓                                                                         ▓▓▓
        echo ▓▓▓   Por favor, instala Python desde: https://www.python.org/downloads/    ▓▓▓
        echo ▓▓▓                                                                         ▓▓▓
        echo ▓▓▓ IMPORTANTE: Durante la instalación marca la opción "Add Python to PATH" ▓▓▓
        echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)

REM Instalar dependencias necesarias
echo 📦 Instalando/verificando dependencias (puede tardar un momento)...
echo.
%PYTHON_CMD% -m pip install --upgrade pandas openpyxl xlrd >nul 2>&1

if errorlevel 1 (
    echo.
    echo ⚠️  Intentando instalación visible...
    %PYTHON_CMD% -m pip install pandas openpyxl xlrd
    echo.
)

echo.
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░
echo.

REM Solicitar ruta del archivo Excel
:PEDIR_ARCHIVO
echo Por favor, introduce la ruta del archivo Excel:
echo (Puedes arrastrar el archivo aquí y presionar ENTER)
echo.
set /p "ARCHIVO_EXCEL="

REM Limpiar comillas si las hay
set "ARCHIVO_EXCEL=%ARCHIVO_EXCEL:"=%"

REM Verificar que el archivo existe
if not exist "%ARCHIVO_EXCEL%" (
    echo.
    echo ❌ ERROR: El archivo no existe: %ARCHIVO_EXCEL%
    echo.
    goto PEDIR_ARCHIVO
)

echo.
echo ✅ Archivo encontrado: %ARCHIVO_EXCEL%
echo.

REM Solicitar número de ticket inicial
:PEDIR_TICKET
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░
echo.
set /p "TICKET_INICIAL=¿Cuál será el número del PRIMER TICKET? (ej: 1000): "

REM Verificar que es un número
echo %TICKET_INICIAL%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Por favor, introduce un número válido
    echo.
    goto PEDIR_TICKET
)

REM Verificar que es mayor que 0
if %TICKET_INICIAL% LEQ 0 (
    echo.
    echo ❌ ERROR: El número debe ser mayor que 0
    echo.
    goto PEDIR_TICKET
)

echo.
echo ✅ Número de ticket inicial: %TICKET_INICIAL%
echo.
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░
echo.
echo 🚀 Iniciando proceso...
echo.

REM Ejecutar el script de Python pasando los parámetros
%PYTHON_CMD% "%~dp0ajustar_facturas.py" "%ARCHIVO_EXCEL%" "%TICKET_INICIAL%"

REM Mantener ventana abierta si hay error
if errorlevel 1 (
    echo.
    echo ❌ El script terminó con errores
    pause
) else (
    echo.
    pause
)
