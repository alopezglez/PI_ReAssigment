@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Sistema de Procesamiento de Facturas

REM Cambiar al directorio del script (resuelve problema de rutas UNC)
cd /d "%~dp0"

echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo ▓▓▓                                                                         ▓▓▓
echo ▓▓▓                   SCRIPT DE AJUSTE DE REGISTROS PI                      ▓▓▓
echo ▓▓▓                                 v1.3                                    ▓▓▓
echo ▓▓▓                                                                         ▓▓▓
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo.
echo   📁 Estructura de carpetas:
echo      • originales/  → Archivos TXT sin procesar
echo      • archivos/    → Archivos procesados listos para ajustar
echo      • resultados/  → Archivos finales con tickets de compensación
echo      • scripts/     → Scripts Python (ocultos)
echo.
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo.

REM Verificar si Python está instalado
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        echo ▓▓▓                                                                         ▓▓▓
        echo ▓▓▓           ERROR: Python no está instalado o no está en el PATH          ▓▓▓
        echo ▓▓▓                                                                         ▓▓▓
        echo ▓▓▓   Por favor, instala Python desde: https://www.python.org/downloads/    ▓▓▓
        echo ▓▓▓                                                                         ▓▓▓
        echo ▓▓▓ IMPORTANTE: Durante la instalación marca la opción "Add Python to PATH" ▓▓▓
        echo ▓▓▓                                                                         ▓▓▓
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

echo 📦 Verificando dependencias de Python...
echo.

REM Verificar si pandas está instalado
%PYTHON_CMD% -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo    ⚠️  pandas no encontrado, instalando...
    %PYTHON_CMD% -m pip install pandas >nul 2>&1
    if errorlevel 1 (
        echo    ❌ Error al instalar pandas
        %PYTHON_CMD% -m pip install pandas
    ) else (
        echo    ✅ pandas instalado
    )
) else (
    echo    ✅ pandas encontrado
)

REM Verificar si openpyxl está instalado
%PYTHON_CMD% -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo    ⚠️  openpyxl no encontrado, instalando...
    %PYTHON_CMD% -m pip install openpyxl >nul 2>&1
    if errorlevel 1 (
        echo    ❌ Error al instalar openpyxl
        %PYTHON_CMD% -m pip install openpyxl
    ) else (
        echo    ✅ openpyxl instalado
    )
) else (
    echo    ✅ openpyxl encontrado
)

REM Verificar si xlrd está instalado
%PYTHON_CMD% -c "import xlrd" >nul 2>&1
if errorlevel 1 (
    echo    ⚠️  xlrd no encontrado, instalando...
    %PYTHON_CMD% -m pip install xlrd >nul 2>&1
    if errorlevel 1 (
        echo    ❌ Error al instalar xlrd
        %PYTHON_CMD% -m pip install xlrd
    ) else (
        echo    ✅ xlrd instalado
    )
) else (
    echo    ✅ xlrd encontrado
)

echo.
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo.
echo 🚀 Todas las dependencias están listas
echo.
echo 📝 Iniciando script de limpieza de caracteres...
echo    (Después podrás ejecutar el ajuste de facturas)
echo.
echo ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
echo.

REM Ejecutar el script de reemplazo de caracteres (que luego preguntará por ajustar_facturas)
%PYTHON_CMD% "%~dp0scripts\reemplazar_caracteres.py"

REM Mantener ventana abierta si hay error
if errorlevel 1 (
    echo.
    echo ❌ El script terminó con errores
    pause
)

exit /b 0
