@echo off
chcp 65001 >nul
python "%~dp0reemplazar_caracteres.py" %1
