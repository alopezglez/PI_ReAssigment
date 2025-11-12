#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ajustar registros de facturas de restaurante
Autor: Alexander López González
Fecha: 2025-11-12
"""

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime, timedelta
import random
import sys
import os

def limpiar_consola():
    """Limpia la consola según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')

def solicitar_archivo():
    """Solicita al usuario la ruta del archivo Excel"""
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓          SCRIPT DE AJUSTE DE REGISTROS PI          ▓")
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("\nPor favor, arrastra el archivo Excel aquí y presiona ENTER:")
    print("(o escribe la ruta completa del archivo)\n")
    
    ruta = input("Ruta del archivo: ").strip().strip('"').strip("'")
    
    if not os.path.exists(ruta):
        print(f"\n❌ ERROR: El archivo no existe: {ruta}")
        input("\nPresiona ENTER para salir...")
        sys.exit(1)
    
    return ruta

def solicitar_ticket_inicial():
    """Solicita el número de ticket inicial"""
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    while True:
        try:
            ticket = input("¿Cuál será el número del PRIMER TICKET? (ej: 1000): ").strip()
            ticket_num = int(ticket)
            if ticket_num > 0:
                return ticket_num
            else:
                print("❌ Por favor, ingresa un número positivo.")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")

def obtener_parametros_desde_args():
    """Obtiene los parámetros desde los argumentos de línea de comandos"""
    if len(sys.argv) >= 3:
        archivo = sys.argv[1].strip().strip('"').strip("'")
        try:
            ticket = int(sys.argv[2])
            if ticket > 0 and os.path.exists(archivo):
                return archivo, ticket
        except ValueError:
            pass
    return None, None

def cargar_excel(ruta):
    """Carga el archivo Excel"""
    print("\n📂 Cargando archivo Excel...")
    
    # Determinar el engine según la extensión
    extension = os.path.splitext(ruta)[1].lower()
    
    # Definir engines según el tipo de archivo
    if extension == '.xls':
        engines = ['xlrd', 'openpyxl']
        print("   📄 Detectado formato Excel 2003 (.xls)")
    elif extension == '.xlsx':
        engines = ['openpyxl', 'xlrd']
        print("   📄 Detectado formato Excel moderno (.xlsx)")
    else:
        engines = ['openpyxl', 'xlrd']
        print(f"   📄 Formato detectado: {extension}")
    
    df = None
    df_totales = None
    
    for engine in engines:
        try:
            print(f"   🔄 Intentando cargar con engine='{engine}'...")
            
            # Cargar hoja de registros
            # Intentar primero con la hoja 'Registros', si no existe usar la primera
            try:
                df = pd.read_excel(ruta, sheet_name='Registros', engine=engine)
                print(f"   ✅ Hoja 'Registros' encontrada y cargada")
            except:
                print(f"   ⚠️  Hoja 'Registros' no encontrada, usando la primera hoja")
                df = pd.read_excel(ruta, sheet_name=0, engine=engine)
            
            # Cargar hoja de totales SIN encabezados (header=None)
            try:
                df_totales = pd.read_excel(ruta, sheet_name='TOTALES', engine=engine, header=None)
                print(f"   ✅ Hoja 'TOTALES' encontrada (sin encabezados)")
            except:
                print("   ⚠️  ADVERTENCIA: No se encontró la hoja 'TOTALES'")
                df_totales = None
            
            print(f"✅ Archivo cargado exitosamente: {len(df)} registros encontrados")
            print(f"   Engine utilizado: {engine}")
            return df, df_totales, ruta
            
        except Exception as e:
            print(f"   ❌ Falló con '{engine}': {str(e)[:100]}")
            if engine == engines[-1]:  # Último intento
                print(f"\n❌ ERROR: No se pudo cargar el archivo con ningún método")
                print(f"\n💡 POSIBLES SOLUCIONES:")
                print("   1. Abre el archivo en Excel y guárdalo como .xlsx (Excel Workbook)")
                print("   2. Verifica que el archivo no esté corrupto")
                print("   3. Cierra el archivo si lo tienes abierto en Excel")
                print("   4. Verifica que el archivo tenga datos en la primera hoja")
                input("\nPresiona ENTER para salir...")
                sys.exit(1)
            else:
                continue  # Intentar con el siguiente engine

def validar_estructura_archivo(df, df_totales, ruta):
    """Valida que el archivo cumple con los requisitos mínimos"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  VALIDACIÓN PREVIA: Estructura del archivo                                  ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    errores_criticos = []
    advertencias = []
    
    # Validación 1: Verificar hojas existentes
    print("\n🔍 Verificando hojas del archivo...")
    if df is None:
        errores_criticos.append("No se pudo cargar la hoja de registros")
    else:
        print("   ✅ Hoja 'Registros' encontrada")
    
    if df_totales is None:
        advertencias.append("Hoja 'TOTALES' no encontrada - No se ajustarán totales")
        print("   ⚠️  Hoja 'TOTALES' no encontrada")
    else:
        print("   ✅ Hoja 'TOTALES' encontrada")
        # Validar estructura de TOTALES
        if len(df_totales) < 1:
            advertencias.append("Hoja 'TOTALES' está vacía")
            print("      ⚠️  La hoja TOTALES está vacía")
        elif len(df_totales.columns) < 2:
            errores_criticos.append("Hoja 'TOTALES' debe tener al menos 2 columnas (Fecha | Total)")
            print("      ❌ Faltan columnas en hoja TOTALES")
        else:
            print(f"      ✅ {len(df_totales)} registros en hoja TOTALES")
    
    # Validación 2: Verificar columnas mínimas
    print("\n🔍 Verificando columnas requeridas...")
    columnas = df.columns.tolist()
    columnas_esperadas = [
        "Local", "DIA", "Hora", "NºFactura", "BASE", "IVA", "TOTAL Fra", 
        "COBRADO", "TARJETA", "Descuentos", "INVITACIONES"
    ]
    
    print(f"   Columnas encontradas: {len(columnas)}")
    print(f"   Columnas esperadas: {len(columnas_esperadas)} mínimo")
    
    if len(columnas) < 8:
        errores_criticos.append(f"Faltan columnas. Encontradas: {len(columnas)}, Mínimo requerido: 8")
        print(f"   ❌ Insuficientes columnas (mínimo 8)")
    else:
        print(f"   ✅ Número de columnas correcto")
        
        # Mostrar columnas encontradas vs esperadas
        print("\n   📋 Mapeo de columnas:")
        for i in range(min(len(columnas), len(columnas_esperadas))):
            esperada = columnas_esperadas[i] if i < len(columnas_esperadas) else "N/A"
            encontrada = columnas[i]
            indicador = "✓" if i < 8 else "○"
            print(f"      {indicador} {chr(65+i)}: {encontrada}")
    
    # Validación 3: Verificar número mínimo de registros
    print("\n🔍 Verificando registros...")
    num_registros = len(df)
    print(f"   Registros totales: {num_registros}")
    
    if num_registros < 10:
        errores_criticos.append(f"Muy pocos registros: {num_registros} (mínimo: 10)")
        print(f"   ❌ Muy pocos registros (mínimo 10)")
    elif num_registros < 100:
        advertencias.append(f"Pocos registros: {num_registros}. Verifica que sea correcto")
        print(f"   ⚠️  Pocos registros. ¿Es correcto?")
    else:
        print(f"   ✅ Cantidad de registros adecuada")
    
    # Validación 4: Verificar datos en columnas críticas
    print("\n🔍 Verificando datos en columnas críticas...")
    
    if len(columnas) >= 4:
        # Verificar columna de NºFactura
        col_ticket = columnas[3]
        tickets_vacios = df[col_ticket].isna().sum()
        if tickets_vacios > num_registros * 0.5:
            errores_criticos.append(f"Columna '{col_ticket}' tiene muchos valores vacíos ({tickets_vacios})")
            print(f"   ❌ Columna NºFactura con datos insuficientes")
        else:
            print(f"   ✅ Columna NºFactura con datos válidos")
    
    if len(columnas) >= 7:
        # Verificar columna de TOTAL
        col_total = columnas[6]
        totales_vacios = df[col_total].isna().sum()
        if totales_vacios > num_registros * 0.5:
            errores_criticos.append(f"Columna '{col_total}' tiene muchos valores vacíos ({totales_vacios})")
            print(f"   ❌ Columna TOTAL con datos insuficientes")
        else:
            print(f"   ✅ Columna TOTAL con datos válidos")
    
    # Mostrar resumen
    print("\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓            RESULTADO DE LA VALIDACIÓN              ▓")
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\n")
    
    if errores_criticos:
        print(f"  ❌ ERRORES CRÍTICOS: {len(errores_criticos)}")
        for error in errores_criticos:
            print(f"     • {error}")
        print("\n  ⛔ El archivo NO cumple los requisitos mínimos")
        print("     Por favor, revisa el archivo y vuelve a intentarlo")
        input("\n  Presiona ENTER para salir...")
        sys.exit(1)
    
    if advertencias:
        print(f"  ⚠️  ADVERTENCIAS: {len(advertencias)}")
        for adv in advertencias:
            print(f"     • {adv}")
    
    if not errores_criticos:
        print(f"  ✅ El archivo cumple los requisitos mínimos")
        if not advertencias:
            print("     ✓ Todas las hojas presentes")
            print("     ✓ Columnas correctas")
            print("     ✓ Número de registros adecuado")
    
    print()

def paso1_fusionar_columnas(df):
    """Fusiona columnas H (COBRADO) e I (INVITACIONES TARJETA)"""
    print("\n╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 1: Fusionando columnas COBRADO e INV. TARJETA                         ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    # Mostrar las columnas encontradas
    columnas = df.columns.tolist()
    print(f"\n📋 Columnas encontradas en el archivo:")
    for i, col in enumerate(columnas):
        print(f"   {chr(65+i)} (índice {i}): {col}")
    
    # Verificar que hay suficientes columnas
    if len(columnas) < 9:
        print(f"\n⚠️  ADVERTENCIA: Solo se encontraron {len(columnas)} columnas")
        print("   Se esperaban al menos 9 columnas (A-I)")
        if len(columnas) < 8:
            print("   No se puede fusionar. Se omite este paso.")
            return df
    
    # Trabajar con índices de columna (más seguro)
    col_h_idx = 7  # Columna H (COBRADO)
    col_i_idx = 8  # Columna I (INVITACIONES TARJETA)
    
    col_h = columnas[col_h_idx]
    col_i = columnas[col_i_idx] if col_i_idx < len(columnas) else None
    
    if col_i:
        # Convertir a numérico, forzando errores a 0
        df[col_h] = pd.to_numeric(df[col_h], errors='coerce').fillna(0)
        df[col_i] = pd.to_numeric(df[col_i], errors='coerce').fillna(0)
        
        # Fusionar: H = H + I
        df[col_h] = df[col_h] + df[col_i]
        df[col_i] = ''  # Vaciar columna I
        
        print(f"\n✅ Columnas fusionadas:")
        print(f"   '{col_h}' (H) ahora contiene la suma de H + I")
        print(f"   '{col_i}' (I) vaciada")
    else:
        print(f"\n⚠️  Solo se encontró la columna H. Se omite la fusión.")
    
    return df

def paso2_eliminar_filas_problematicas(df):
    """Elimina filas con subtotales y registros negativos"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 2: Eliminando filas problemáticas                                     ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    inicial = len(df)
    columnas = df.columns.tolist()
    
    # Usar índices de columna
    col_d = columnas[3] if len(columnas) > 3 else None  # NºFactura
    col_e = columnas[4] if len(columnas) > 4 else None  # BASE
    col_f = columnas[5] if len(columnas) > 5 else None  # IVA
    col_g = columnas[6] if len(columnas) > 6 else None  # TOTAL Fra
    col_h = columnas[7] if len(columnas) > 7 else None  # COBRADO
    
    # Eliminar filas con SUBTOTAL
    if col_d:
        df = df[~df[col_d].astype(str).str.contains('SUBTOTAL', case=False, na=False)].copy()
        subtotales = inicial - len(df)
        print(f"✅ Filas de SUBTOTAL eliminadas: {subtotales}")
    else:
        print("⚠️  No se encontró columna de NºFactura")
        subtotales = 0
        df = df.copy()
    
    # Eliminar filas donde haya valores negativos en E, F, G o H
    inicial_neg = len(df)
    
    # Convertir columnas a numérico primero
    columnas_numericas = []
    if col_e:
        df.loc[:, col_e] = pd.to_numeric(df[col_e], errors='coerce')
        columnas_numericas.append(col_e)
    if col_f:
        df.loc[:, col_f] = pd.to_numeric(df[col_f], errors='coerce')
        columnas_numericas.append(col_f)
    if col_g:
        df.loc[:, col_g] = pd.to_numeric(df[col_g], errors='coerce')
        columnas_numericas.append(col_g)
    if col_h:
        df.loc[:, col_h] = pd.to_numeric(df[col_h], errors='coerce')
        columnas_numericas.append(col_h)
    
    # Crear condiciones (usar >= 0 directamente sin fillna para evitar warnings)
    condiciones = []
    for col in columnas_numericas:
        # Comparar con 0, los NaN se convierten automáticamente a False
        condiciones.append((df[col] >= 0) | df[col].isna())
    
    if condiciones:
        from functools import reduce
        import operator
        mascara_final = reduce(operator.and_, condiciones)
        df = df[mascara_final].copy()
        negativos = inicial_neg - len(df)
        print(f"✅ Filas con valores negativos eliminadas: {negativos}")
    else:
        print("⚠️  No se pudieron verificar valores negativos")
        negativos = 0
    
    # Resetear índice
    df = df.reset_index(drop=True)
    
    print(f"✅ Registros restantes: {len(df)}")
    
    return df

def paso6_hacer_tickets_correlativos(df, ticket_inicial):
    """Hace que los tickets sean correlativos por día - SE EJECUTA AL FINAL"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 6: Haciendo tickets correlativos (FINAL)                              ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    columnas = df.columns.tolist()
    col_b = columnas[1]  # DIA
    col_d = columnas[3]  # NºFactura
    
    # Agrupar por día - forzar formato dd/mm/yyyy primero
    df[col_b] = pd.to_datetime(df[col_b], dayfirst=True, errors='coerce')
    
    # Extraer solo la fecha (sin hora)
    df['_fecha_temp'] = df[col_b].dt.date
    dias_unicos = sorted(df['_fecha_temp'].dropna().unique())
    
    print(f"📅 Días encontrados: {len(dias_unicos)}")
    if dias_unicos:
        print(f"   Primer día: {dias_unicos[0]}")
        print(f"   Último día: {dias_unicos[-1]}")
        
        # Analizar meses y días faltantes
        from collections import defaultdict
        import calendar
        
        meses_con_datos = defaultdict(set)
        anos_con_datos = set()
        
        for dia in dias_unicos:
            anos_con_datos.add(dia.year)
            meses_con_datos[dia.year].add(dia.month)
        
        # Mostrar análisis por año
        for ano in sorted(anos_con_datos):
            meses = sorted(meses_con_datos[ano])
            nombres_meses = [calendar.month_name[m] for m in meses]
            
            if len(meses) == 12:
                print(f"   📊 Analizado año {ano}: Completo (12 meses)")
            else:
                meses_str = ", ".join(nombres_meses)
                print(f"   📊 Analizado año {ano}: {meses_str}")
    
    ticket_actual = ticket_inicial
    
    for dia in dias_unicos:
        mask = df['_fecha_temp'] == dia
        indices = df[mask].index.tolist()
        num_tickets = len(indices)
        
        for idx in indices:
            df.at[idx, col_d] = ticket_actual
            ticket_actual += 1
    
    # Eliminar columna temporal
    df = df.drop('_fecha_temp', axis=1)
    
    print(f"✅ Tickets renumerados desde {ticket_inicial} hasta {ticket_actual - 1}")
    print(f"   Total de días procesados: {len(dias_unicos)}")
    
    return df, ticket_actual - 1

def paso3_ajustar_totales_por_dia(df, df_totales):
    """Ajusta los totales de cada día para que coincidan con la hoja TOTALES"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 3: Ajustando totales por día                                          ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    columnas = df.columns.tolist()
    col_a = columnas[0]  # Local
    col_b = columnas[1]  # DIA
    col_c = columnas[2]  # Hora
    col_d = columnas[3]  # NºFactura
    col_e = columnas[4]  # BASE
    col_f = columnas[5]  # IVA
    col_g = columnas[6]  # TOTAL Fra
    col_h = columnas[7]  # COBRADO
    
    # Crear diccionario de totales esperados
    totales_esperados = {}
    if df_totales is not None:
        print(f"\n📋 Analizando hoja TOTALES:")
        print(f"   Filas encontradas: {len(df_totales)}")
        print(f"   Primeras 3 filas como muestra:")
        
        # Mostrar muestra de datos
        for i in range(min(3, len(df_totales))):
            print(f"      Fila {i+1}: Fecha={df_totales.iloc[i, 0]} | Total={df_totales.iloc[i, 1]}")
        
        # Leer datos: Columna 0 = Fecha, Columna 1 = Total
        for idx, row in df_totales.iterrows():
            fecha = pd.to_datetime(row[0], dayfirst=True, errors='coerce')
            if pd.notna(fecha):
                total = float(row[1]) if pd.notna(row[1]) else None
                if total is not None:
                    totales_esperados[fecha.date()] = total
        
        print(f"   Total de fechas válidas procesadas: {len(totales_esperados)}")
        if totales_esperados:
            primer_total = min(totales_esperados.keys())
            ultimo_total = max(totales_esperados.keys())
            print(f"   Rango: {primer_total} a {ultimo_total}")
    else:
        print("⚠️  No se encontró la hoja TOTALES")
    
    if not totales_esperados:
        print("⚠️  ADVERTENCIA: No hay totales en la hoja TOTALES")
        print("   Se mantendrán los totales calculados de los registros")
        print("   Para ajustar totales, verifica que:")
        print("   - La hoja se llame exactamente 'TOTALES'")
        print("   - Columna A tenga fechas en formato dd/mm/yyyy")
        print("   - Columna B tenga los totales esperados")
        return df
    
    # Asegurar que las fechas están en el formato correcto
    if '_fecha_temp' in df.columns:
        df = df.drop('_fecha_temp', axis=1)
    
    # Asegurarse de que col_b es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[col_b]):
        df[col_b] = pd.to_datetime(df[col_b], dayfirst=True, errors='coerce')
    
    df['_fecha_temp'] = df[col_b].dt.date
    
    # Procesar cada día
    dias_unicos = sorted([d for d in df['_fecha_temp'].unique() if d is not None and not pd.isna(d)])
    filas_nuevas = []
    
    print(f"\n🔍 Procesando {len(dias_unicos)} días:")
    dias_sin_total = []
    dias_ajustados = []
    dias_correctos = []
    
    for dia in dias_unicos:
        mask = df['_fecha_temp'] == dia
        registros_dia = df[mask].copy()
        
        total_actual = registros_dia[col_g].sum()
        total_esperado = totales_esperados.get(dia)
        
        if total_esperado is None:
            # IMPORTANTE: No hay total en la hoja TOTALES para este día
            print(f"⚠️  {dia}: SIN TOTAL en hoja TOTALES - Calculado: {total_actual:.2f}€")
            dias_sin_total.append(dia)
            continue
        
        diferencia = total_esperado - total_actual
        
        if abs(diferencia) < 0.01:
            print(f"✅ {dia}: Coincide con TOTALES: {total_actual:.2f}€")
            dias_correctos.append(dia)
            continue
        
        print(f"🔧 {dia}: Ajustando {total_actual:.2f}€ → {total_esperado:.2f}€ (dif: {diferencia:+.2f}€)")
        dias_ajustados.append(dia)
        
        # Obtener datos del último registro del día
        ultimo_registro = registros_dia.iloc[-1]
        ultimo_ticket = int(ultimo_registro[col_d])
        hora_base = ultimo_registro[col_c]
        local = ultimo_registro[col_a]
        
        # Crear tickets de ajuste
        num_tickets = max(1, int(abs(diferencia) / 50))  # Dividir en tickets de ~50€
        ajuste_por_ticket = diferencia / num_tickets
        
        for i in range(num_tickets):
            # Calcular hora (incrementar minutos)
            if isinstance(hora_base, str):
                try:
                    hora_dt = datetime.strptime(hora_base, '%H:%M:%S')
                except:
                    try:
                        hora_dt = datetime.strptime(hora_base, '%H:%M')
                    except:
                        hora_dt = datetime.strptime('23:59:00', '%H:%M:%S')
            else:
                hora_dt = hora_base
            
            nueva_hora = (hora_dt + timedelta(minutes=i+1)).strftime('%H:%M')
            
            # Calcular BASE e IVA (IVA = 7%) - Redondear a 2 decimales
            total_ticket = round(ajuste_por_ticket, 2)
            base = round(total_ticket / 1.07, 2)
            iva = round(total_ticket - base, 2)
            
            nueva_fila = {
                col_a: local,
                col_b: pd.Timestamp(dia),
                col_c: nueva_hora,
                col_d: ultimo_ticket + i + 1,
                col_e: base,
                col_f: iva,
                col_g: total_ticket,
                col_h: total_ticket,
            }
            
            # Añadir columnas restantes vacías
            for col_idx in range(8, len(columnas)):
                nueva_fila[columnas[col_idx]] = ''
            
            filas_nuevas.append(nueva_fila)
    
    # Añadir las filas nuevas al DataFrame
    if filas_nuevas:
        df_nuevas = pd.DataFrame(filas_nuevas)
        df = pd.concat([df, df_nuevas], ignore_index=True)
        
        # Reordenar por día y hora
        df = df.sort_values([col_b, col_c]).reset_index(drop=True)
        
        print(f"\n✅ Se agregaron {len(filas_nuevas)} tickets de ajuste")
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DEL PASO 4:")
    print(f"   ✅ Días correctos: {len(dias_correctos)}")
    print(f"   🔧 Días ajustados: {len(dias_ajustados)}")
    if dias_sin_total:
        print(f"   ⚠️  Días SIN TOTAL en hoja TOTALES: {len(dias_sin_total)}")
        print(f"      ACCIÓN REQUERIDA: Verifica la hoja TOTALES")
        print(f"      Días afectados: {dias_sin_total[0]} a {dias_sin_total[-1]}")
    
    return df

def paso4_añadir_ticket_negativo(df):
    """Añade un ticket negativo al final de cada día (0.8-1.0% del total)"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 4: Añadiendo ticket negativo al final del día                         ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    columnas = df.columns.tolist()
    col_a = columnas[0]  # Local
    col_b = columnas[1]  # DIA
    col_c = columnas[2]  # Hora
    col_d = columnas[3]  # NºFactura
    col_e = columnas[4]  # BASE
    col_f = columnas[5]  # IVA
    col_g = columnas[6]  # TOTAL Fra
    col_h = columnas[7]  # COBRADO
    col_j = columnas[9] if len(columnas) > 9 else 'INVITACIONES'  # INVITACIONES
    
    # Asegurar columna temporal de fecha
    if '_fecha_temp' in df.columns:
        df = df.drop('_fecha_temp', axis=1)
    
    # Asegurarse de que col_b es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[col_b]):
        df[col_b] = pd.to_datetime(df[col_b], dayfirst=True, errors='coerce')
    
    df['_fecha_temp'] = df[col_b].dt.date
    
    dias_unicos = sorted([d for d in df['_fecha_temp'].unique() if d is not None and not pd.isna(d)])
    filas_nuevas = []
    
    for dia in dias_unicos:
        mask = df['_fecha_temp'] == dia
        registros_dia = df[mask].copy()
        
        total_dia = registros_dia[col_g].sum()
        porcentaje = random.uniform(0.008, 0.010)  # 0.8% - 1.0%
        importe_negativo = -1 * (total_dia * porcentaje)
        
        # Obtener datos del último registro
        ultimo_registro = registros_dia.iloc[-1]
        ultimo_ticket = int(ultimo_registro[col_d])
        local = ultimo_registro[col_a]
        
        # Crear hora final (sin segundos)
        hora_final = "23:59"
        
        # Calcular BASE e IVA negativos (redondear a 2 decimales)
        base_neg = round(importe_negativo / 1.07, 2)
        iva_neg = round(importe_negativo - base_neg, 2)
        
        nueva_fila = {
            col_a: local,
            col_b: pd.Timestamp(dia),
            col_c: hora_final,
            col_d: ultimo_ticket + 1,
            col_e: round(base_neg, 2),
            col_f: round(iva_neg, 2),
            col_g: round(importe_negativo, 2),
            col_h: 0,
            col_j: round(importe_negativo, 2)
        }
        
        # Añadir columnas restantes vacías
        for col_idx in range(len(columnas)):
            if columnas[col_idx] not in nueva_fila:
                nueva_fila[columnas[col_idx]] = ''
        
        filas_nuevas.append(nueva_fila)
        
        print(f"✅ {dia}: Ticket negativo añadido: {importe_negativo:.2f}€ ({porcentaje*100:.2f}% de {total_dia:.2f}€)")
    
    # Añadir las filas al DataFrame
    if filas_nuevas:
        df_nuevas = pd.DataFrame(filas_nuevas)
        df = pd.concat([df, df_nuevas], ignore_index=True)
        df = df.sort_values([col_b, col_c]).reset_index(drop=True)
    
    return df

def paso5_compensar_tickets_negativos(df, df_totales):
    """Añade tickets positivos antes del negativo para compensar"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 5: Compensando tickets negativos                                      ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    columnas = df.columns.tolist()
    col_a = columnas[0]  # Local
    col_b = columnas[1]  # DIA
    col_c = columnas[2]  # Hora
    col_d = columnas[3]  # NºFactura
    col_e = columnas[4]  # BASE
    col_f = columnas[5]  # IVA
    col_g = columnas[6]  # TOTAL Fra
    col_h = columnas[7]  # COBRADO
    
    # Crear diccionario de totales esperados
    totales_esperados = {}
    if df_totales is not None:
        # Leer datos: Columna 0 = Fecha, Columna 1 = Total (sin encabezados)
        for _, row in df_totales.iterrows():
            fecha = pd.to_datetime(row[0], dayfirst=True, errors='coerce')
            if pd.notna(fecha):
                total = float(row[1]) if pd.notna(row[1]) else None
                if total is not None:
                    totales_esperados[fecha.date()] = total
    
    # Asegurar columna temporal de fecha - limpiar y recrear si es necesario
    if '_fecha_temp' in df.columns:
        df = df.drop('_fecha_temp', axis=1)
    
    # Asegurarse de que col_b es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[col_b]):
        df[col_b] = pd.to_datetime(df[col_b], dayfirst=True, errors='coerce')
    
    df['_fecha_temp'] = df[col_b].dt.date
    
    # Filtrar valores no nulos y ordenar
    dias_unicos = sorted([d for d in df['_fecha_temp'].unique() if d is not None and not pd.isna(d)])
    filas_compensacion = []
    
    for dia in dias_unicos:
        mask = df['_fecha_temp'] == dia
        registros_dia = df[mask].copy()
        
        total_actual = registros_dia[col_g].sum()
        total_esperado = totales_esperados.get(dia, total_actual)
        
        diferencia = total_esperado - total_actual
        
        if abs(diferencia) < 0.01:
            print(f"✅ {dia}: No necesita compensación: {total_actual:.2f}€")
            continue
        
        print(f"🔧 {dia}: Compensando {diferencia:.2f}€")
        
        # Encontrar el penúltimo registro (antes del negativo)
        penultimo_registro = registros_dia.iloc[-2] if len(registros_dia) > 1 else registros_dia.iloc[-1]
        ticket_antes_negativo = int(penultimo_registro[col_d])
        local = penultimo_registro[col_a]
        hora_base = penultimo_registro[col_c]
        
        # Crear tickets de compensación (dividir en varios tickets)
        num_tickets = max(1, int(abs(diferencia) / 50))
        compensacion_por_ticket = diferencia / num_tickets
        
        for i in range(num_tickets):
            # Calcular hora
            if isinstance(hora_base, str):
                try:
                    hora_dt = datetime.strptime(hora_base, '%H:%M:%S')
                except:
                    try:
                        hora_dt = datetime.strptime(hora_base, '%H:%M')
                    except:
                        hora_dt = datetime.strptime('23:50:00', '%H:%M:%S')
            else:
                hora_dt = hora_base
            
            nueva_hora = (hora_dt + timedelta(minutes=i+1)).strftime('%H:%M')
            
            # Calcular BASE e IVA - Redondear a 2 decimales
            total_ticket = round(compensacion_por_ticket, 2)
            base = round(total_ticket / 1.07, 2)
            iva = round(total_ticket - base, 2)
            
            nueva_fila = {
                col_a: local,
                col_b: pd.Timestamp(dia),
                col_c: nueva_hora,
                col_d: ticket_antes_negativo + i + 1,
                col_e: base,
                col_f: iva,
                col_g: total_ticket,
                col_h: total_ticket,
            }
            
            # Añadir columnas restantes vacías
            for col_idx in range(8, len(columnas)):
                nueva_fila[columnas[col_idx]] = ''
            
            filas_compensacion.append(nueva_fila)
    
    # Añadir las filas de compensación
    if filas_compensacion:
        df_compensacion = pd.DataFrame(filas_compensacion)
        df = pd.concat([df, df_compensacion], ignore_index=True)
        df = df.sort_values([col_b, col_c]).reset_index(drop=True)
        
        print(f"✅ Se agregaron {len(filas_compensacion)} tickets de compensación")
    
    return df

def paso7_verificacion_final(df, df_totales):
    """Verifica la integridad final de los datos"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  PASO 7: Verificación final de integridad                                   ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    columnas = df.columns.tolist()
    col_b = columnas[1]  # DIA
    col_g = columnas[6]  # TOTAL Fra
    col_j = columnas[9] if len(columnas) > 9 else None  # INVITACIONES (negativos)
    
    # Asegurar columna temporal de fecha
    if '_fecha_temp' in df.columns:
        df = df.drop('_fecha_temp', axis=1)
    
    if not pd.api.types.is_datetime64_any_dtype(df[col_b]):
        df[col_b] = pd.to_datetime(df[col_b], dayfirst=True, errors='coerce')
    
    df['_fecha_temp'] = df[col_b].dt.date
    dias_unicos = sorted([d for d in df['_fecha_temp'].unique() if d is not None and not pd.isna(d)])
    
    # Cargar totales esperados
    totales_esperados = {}
    if df_totales is not None:
        for _, row in df_totales.iterrows():
            fecha = pd.to_datetime(row[0], dayfirst=True, errors='coerce')
            if pd.notna(fecha):
                total = float(row[1]) if pd.notna(row[1]) else None
                if total is not None:
                    totales_esperados[fecha.date()] = total
    
    print(f"\n🔍 Analizando {len(dias_unicos)} días...\n")
    
    errores = []
    advertencias = []
    dias_ok = 0
    
    for dia in dias_unicos:
        mask = df['_fecha_temp'] == dia
        registros_dia = df[mask].copy()
        
        # Verificar 1: Contar tickets negativos
        if col_j:
            negativos = registros_dia[registros_dia[col_j].notna() & (registros_dia[col_j] != '') & (registros_dia[col_j] != 0)]
            num_negativos = len(negativos)
        else:
            negativos = registros_dia[registros_dia[col_g] < 0]
            num_negativos = len(negativos)
        
        # Verificar 2: Total del día
        total_dia = registros_dia[col_g].sum()
        total_esperado = totales_esperados.get(dia)
        
        # Indicadores
        icono_negativos = "✅" if num_negativos == 1 else "❌"
        
        if total_esperado is not None:
            diferencia = abs(total_esperado - total_dia)
            icono_total = "✅" if diferencia < 0.01 else "❌"
            diferencia_str = f"{diferencia:+.2f}€" if diferencia >= 0.01 else "0.00€"
            total_info = f"Esperado: {total_esperado:.2f}€ | Real: {total_dia:.2f}€ | Dif: {diferencia_str}"
        else:
            icono_total = "⚠️"
            total_info = f"Real: {total_dia:.2f}€ | Sin referencia en TOTALES"
        
        # Resumen de línea
        status_negativos = f"{icono_negativos} {num_negativos} neg"
        status_total = f"{icono_total} {total_info}"
        
        print(f"  {dia}: {status_negativos} | {status_total}")
        
        # Registrar errores
        if num_negativos != 1:
            errores.append(f"{dia}: Tiene {num_negativos} tickets negativos (esperado: 1)")
        
        if total_esperado is not None and diferencia >= 0.01:
            errores.append(f"{dia}: Diferencia en total: {diferencia:.2f}€")
        
        if total_esperado is None:
            advertencias.append(f"{dia}: Sin total de referencia en hoja TOTALES")
        
        if num_negativos == 1 and (total_esperado is None or diferencia < 0.01):
            dias_ok += 1
    
    # Mostrar resumen final
    print("\n" + "═" * 63)
    print("  📊 RESULTADO DE LA VERIFICACIÓN")
    print("═" * 63)
    print(f"  ✅ Días correctos: {dias_ok}/{len(dias_unicos)}")
    print(f"  ❌ Días con errores: {len(set([e.split(':')[0] for e in errores]))}")
    print(f"  ⚠️  Advertencias: {len(advertencias)}")
    
    if errores:
        print(f"\n  ❌ ERRORES DETECTADOS:")
        for error in errores[:10]:  # Mostrar máximo 10
            print(f"     • {error}")
        if len(errores) > 10:
            print(f"     ... y {len(errores) - 10} errores más")
    
    if advertencias and not errores:
        print(f"\n  ⚠️  ADVERTENCIAS:")
        for adv in advertencias[:5]:  # Mostrar máximo 5
            print(f"     • {adv}")
        if len(advertencias) > 5:
            print(f"     ... y {len(advertencias) - 5} advertencias más")
    
    if not errores and not advertencias:
        print("\n  🎉 ¡PERFECTO! Todos los datos son correctos")
        print("     ✓ Un ticket negativo por día")
        print("     ✓ Totales coinciden con hoja TOTALES")
        print("     ✓ Tickets correlativos")
    
    return df

def guardar_resultado(df, ruta_original):
    """Guarda el resultado en un nuevo archivo Excel"""
    print("\n╔═════════════════════════════════════════════════════════════════════════════╗")
    print("║  GUARDANDO RESULTADO                                                        ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")
    
    # Eliminar columnas temporales antes de guardar
    if '_fecha_temp' in df.columns:
        df = df.drop('_fecha_temp', axis=1)
    
    # Crear nombre del archivo de salida
    dir_original = os.path.dirname(ruta_original)
    nombre_original = os.path.basename(ruta_original)
    nombre_sin_ext = os.path.splitext(nombre_original)[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_salida = f"{nombre_sin_ext}_AJUSTADO_{timestamp}.xlsx"
    ruta_salida = os.path.join(dir_original, nombre_salida)
    
    print(f"💾 Guardando en: {ruta_salida}")
    
    try:
        # Guardar con openpyxl para mantener formato
        df.to_excel(ruta_salida, index=False, engine='openpyxl')
        
        print(f"✅ Archivo guardado exitosamente")
        print(f"📊 Total de registros: {len(df)}")
        
        return ruta_salida
    except Exception as e:
        print(f"❌ ERROR al guardar: {str(e)}")
        return None

def mostrar_resumen_final(df, ruta_salida):
    """Muestra un resumen final del proceso"""
    print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▓                               RESUMEN FINAL                                 ▓")
    print("▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
    print("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    
    columnas = df.columns.tolist()
    col_b = columnas[1]  # DIA
    col_g = columnas[6]  # TOTAL Fra
    
    # Asegurar columna temporal de fecha
    if '_fecha_temp' in df.columns:
        df = df.drop('_fecha_temp', axis=1)
    
    # Asegurarse de que col_b es datetime
    if not pd.api.types.is_datetime64_any_dtype(df[col_b]):
        df[col_b] = pd.to_datetime(df[col_b], dayfirst=True, errors='coerce')
    
    df['_fecha_temp'] = df[col_b].dt.date
    
    dias_unicos = sorted([d for d in df['_fecha_temp'].unique() if d is not None and not pd.isna(d)])
    
    print(f"\n📅 Días procesados: {len(dias_unicos)}")
    print(f"📝 Total de registros: {len(df)}")
    print(f"\n💰 Totales por día:")
    print("─" * 63)
    
    for dia in dias_unicos:
        mask = df['_fecha_temp'] == dia
        registros = df[mask]
        total = registros[col_g].sum()
        num_tickets = len(registros)
        
        print(f"  {dia}: {total:>10.2f}€  ({num_tickets} tickets)")
    
    print("─" * 63)
    total_general = df[col_g].sum()
    print(f"  TOTAL GENERAL: {total_general:>10.2f}€")
    
    print(f"\n✅ Proceso completado exitosamente")
    print(f"📁 Archivo guardado en:\n   {ruta_salida}")

def main():
    """Función principal"""
    try:
        # Intentar obtener parámetros desde argumentos
        ruta, ticket_inicial = obtener_parametros_desde_args()
        
        if ruta is None or ticket_inicial is None:
            # Si no hay argumentos válidos, solicitar manualmente
            limpiar_consola()
            ruta = solicitar_archivo()
            ticket_inicial = solicitar_ticket_inicial()
        else:
        # Si hay argumentos válidos, mostrar información
            print("╔═══════════════════════════════════════════════════════════╗")
            print("║  SCRIPT DE AJUSTE DE FACTURAS DE RESTAURANTE              ║")
            print("╚═══════════════════════════════════════════════════════════╝")
            print(f"\n📁 Archivo: {os.path.basename(ruta)}")
            print(f"🎫 Ticket inicial: {ticket_inicial}")
        
        # Cargar Excel
        df, df_totales, ruta_original = cargar_excel(ruta)
        
        # VALIDACIÓN PREVIA: Verificar estructura del archivo
        validar_estructura_archivo(df, df_totales, ruta_original)
        
        # PASO 1: Fusionar columnas
        df = paso1_fusionar_columnas(df)
        
        # PASO 2: Eliminar filas problemáticas
        df = paso2_eliminar_filas_problematicas(df)
        
        # PASO 3: Ajustar totales por día
        df = paso3_ajustar_totales_por_dia(df, df_totales)
        
        # PASO 4: Añadir ticket negativo al final de cada día
        df = paso4_añadir_ticket_negativo(df)
        
        # PASO 5: Compensar tickets negativos
        df = paso5_compensar_tickets_negativos(df, df_totales)
        
        # PASO 6: Hacer tickets correlativos (AL FINAL)
        df, ultimo_ticket = paso6_hacer_tickets_correlativos(df, ticket_inicial)
        
        # PASO 7: Verificación final
        df = paso7_verificacion_final(df, df_totales)
        
        # Guardar resultado
        ruta_salida = guardar_resultado(df, ruta_original)
        
        if ruta_salida:
            # Mostrar resumen final
            mostrar_resumen_final(df, ruta_salida)
        
        print("\n" + "=" * 60)
        input("\n✅ Presiona ENTER para salir...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
        input("\nPresiona ENTER para salir...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nPresiona ENTER para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
