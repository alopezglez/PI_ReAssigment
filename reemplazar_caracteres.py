import sys
import os
import time
import shutil
from datetime import datetime

def mostrar_cabecera():
    """Muestra la cabecera del programa"""
    print("\n")
    print("░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░")
    print("░░░░▒▒▒▒▓▓▓           REEMPLAZO DE CARACTERES UTF-8 con BOM         ▓▓▓▒▒▒▒░░░░")
    print("░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░")
    print()

def mostrar_barra_progreso(progreso, total, texto="Procesando"):
    """Muestra una barra de progreso con el texto en una línea separada"""
    porcentaje = int((progreso / total) * 100)
    barra_llena = int((progreso / total) * 40)
    barra_vacia = 40 - barra_llena
    
    barra = "█" * barra_llena + "░" * barra_vacia
    
    # Limpiar las dos líneas anteriores y mostrar el progreso
    print(f"\r{texto:<50}", end="")
    print(f"\n[{barra}] {porcentaje}%", end="", flush=True)
    
    # Mover el cursor hacia arriba para sobrescribir en la siguiente actualización
    if progreso < total:
        print("\033[F\033[F", end="", flush=True)  # Subir 2 líneas
    else:
        print()  # Nueva línea al terminar

def reemplazar_caracteres(ruta_archivo):
    """
    Reemplaza caracteres y patrones específicos en un archivo de texto.
    """
    # Diccionario de reemplazos (de -> a)
    reemplazos = {
        '     ,######0.00': 'TARJETA',
        'õ': '─',
        'ý': '┬',
        'ÿ': '┼',
        'ú': '│',
        'ü': '┌',
        'þ': '├',
        'ù': '┐',
        'û': '┤',
        '[@DG]├': '├',
        '[@FG]├': '├',
        '[@FG]ö': '└',
        '÷': '┴',
        'ó': '┘'
    }
    
    backup_creado = None
    archivo_temporal = None
    
    try:
        print(f"📄 Archivo: {os.path.basename(ruta_archivo)}")
        print(f"📂 Ruta: {os.path.dirname(ruta_archivo)}")
        
        # Obtener tamaño del archivo original
        tamanio_original = os.path.getsize(ruta_archivo)
        print(f"📊 Tamaño original: {tamanio_original:,} bytes")
        print()
        
        # Crear copia de seguridad con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_base = os.path.splitext(ruta_archivo)[0]
        extension = os.path.splitext(ruta_archivo)[1]
        ruta_backup = f"{nombre_base}_BACKUP_{timestamp}{extension}"
        
        # Paso 1: Crear backup INMEDIATAMENTE
        mostrar_barra_progreso(1, 7, "Creando respaldo seguro")
        time.sleep(0.1)
        shutil.copy2(ruta_archivo, ruta_backup)
        backup_creado = ruta_backup
        
        # Verificar que el backup se creó correctamente
        if not os.path.exists(ruta_backup) or os.path.getsize(ruta_backup) != tamanio_original:
            raise Exception("El backup no se creó correctamente. Operación abortada.")
        
        # Paso 2: Leer archivo con detección de codificación
        mostrar_barra_progreso(2, 7, "Leyendo archivo")
        time.sleep(0.2)
        
        # Intentar diferentes codificaciones
        codificaciones = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'cp850']
        lineas = None
        encoding_usado = None
        
        for encoding in codificaciones:
            try:
                with open(ruta_archivo, 'r', encoding=encoding) as f:
                    lineas = f.readlines()
                encoding_usado = encoding
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if lineas is None:
            raise Exception("No se pudo leer el archivo con ninguna codificación soportada")
        
        # Paso 3: Validar archivo
        mostrar_barra_progreso(3, 7, "Validando estructura")
        time.sleep(0.1)
        lineas_originales = len(lineas)
        
        # Verificar que el archivo tiene suficientes líneas
        if lineas_originales < 8:
            raise Exception(f"El archivo tiene solo {lineas_originales} líneas. Se necesitan al menos 8 líneas para procesar.")
        
        # Paso 4: Eliminar filas
        mostrar_barra_progreso(4, 7, "Eliminando filas")
        time.sleep(0.2)
        
        # Eliminar las 4 primeras filas
        lineas = lineas[4:]
        
        # Eliminar la fila 8 original (ahora sería índice 3 tras eliminar las 4 primeras)
        # La fila 8 original ahora está en el índice 3 (fila 5, 6, 7, 8 -> índices 0, 1, 2, 3)
        if len(lineas) > 3:
            lineas.pop(3)
        
        # Eliminar líneas vacías y líneas con 'Registro(s) Seleccionado(s)'
        lineas_antes_filtro = len(lineas)
        lineas = [
            linea for linea in lineas 
            if linea.strip() != '' and 'Registro(s) Seleccionado(s)' not in linea
        ]
        lineas_filtradas = lineas_antes_filtro - len(lineas)
        
        # Unir las líneas
        contenido = ''.join(lineas)
        lineas_despues_eliminar = len(lineas)
        
        # VALIDACIÓN CRÍTICA: Verificar que el contenido tiene sentido
        if not contenido or len(contenido) == 0:
            raise Exception(f"CRÍTICO: El archivo resultante está vacío. Operación abortada.")
        
        if len(contenido) < 100:
            raise Exception(f"CRÍTICO: El archivo resultante tiene solo {len(contenido)} bytes. Demasiado pequeño. Operación abortada.")
        
        # Validar que al menos quedó el 80% del contenido original
        ratio_contenido = len(contenido) / tamanio_original
        if ratio_contenido < 0.8:
            raise Exception(f"CRÍTICO: El archivo perdió más del 20% de contenido ({ratio_contenido*100:.1f}% restante). Operación abortada.")
        
        # Paso 5: Realizar reemplazos
        mostrar_barra_progreso(5, 7, "Reemplazando caracteres")
        time.sleep(0.2)
        contenido_modificado = contenido
        total_reemplazos = len(reemplazos)
        contador_reemplazos = {}
        
        for antiguo, nuevo in reemplazos.items():
            count = contenido_modificado.count(antiguo)
            contador_reemplazos[antiguo] = count
            contenido_modificado = contenido_modificado.replace(antiguo, nuevo)
        
        # VALIDACIÓN CRÍTICA: Verificar que el contenido modificado tiene sentido
        if len(contenido_modificado) == 0:
            raise Exception(f"CRÍTICO: El contenido modificado está vacío. Operación abortada.")
        
        # Paso 6: Guardar en archivo temporal primero
        mostrar_barra_progreso(6, 7, "Guardando a temporal")
        time.sleep(0.1)
        archivo_temporal = ruta_archivo + '.tmp'
        
        # Guardar siempre en UTF-8 porque los caracteres de reemplazo lo requieren
        with open(archivo_temporal, 'w', encoding='utf-8') as f:
            f.write(contenido_modificado)
        
        # Verificar que el archivo temporal se creó correctamente
        if not os.path.exists(archivo_temporal):
            raise Exception("CRÍTICO: No se pudo crear el archivo temporal. Operación abortada.")
        
        tamanio_temporal = os.path.getsize(archivo_temporal)
        if tamanio_temporal == 0:
            raise Exception("CRÍTICO: El archivo temporal está vacío. Operación abortada.")
        
        # Paso 7: Reemplazar el archivo original con el temporal
        mostrar_barra_progreso(7, 7, "Completando operación")
        time.sleep(0.1)
        
        # Hacer el reemplazo atómico
        shutil.move(archivo_temporal, ruta_archivo)
        archivo_temporal = None  # Ya no existe
        print()
        print()
        print("╔═════════════════════════════════════════════════════════════════╗")
        print("║     ARCHIVO PROCESADO CORRECTAMENTE                             ║")
        print("╚═════════════════════════════════════════════════════════════════╝")
        print(f"  📁 Archivo: {os.path.basename(ruta_archivo):<49}")
        print(f"  🔤 Codificación origen: {encoding_usado:<38}")
        print(f"  🔤 Codificación destino: UTF-8")
        print("───────────────────────────────────────────────────────────────────")
        print(f"  📊 Líneas originales: {lineas_originales:<42}")
        print(f"  📊 Líneas procesadas: {lineas_despues_eliminar:<42}")
        print(f"  📊 Líneas finales: {len(contenido_modificado.splitlines()):<45}")
        print(f"  ✂️  Filas eliminadas: 5 (4 primeras + fila 8)")
        print(f"  🗑️  Líneas vacías/filtradas eliminadas: {lineas_filtradas}")
        print("───────────────────────────────────────────────────────────────────")
        print(f"  💾 Tamaño original: {tamanio_original:>12,} bytes")
        print(f"  💾 Tamaño final:    {len(contenido_modificado):>12,} bytes")
        print(f"  📈 Ratio: {(len(contenido_modificado)/tamanio_original)*100:>6.2f}%")
        print("───────────────────────────────────────────────────────────────────")
        
        # Mostrar reemplazos realizados
        reemplazos_efectivos = sum(1 for c in contador_reemplazos.values() if c > 0)
        print(f"  🔄 Patrones aplicados: {reemplazos_efectivos}/{total_reemplazos}")
        print()
        
        # Mostrar todos los reemplazos que se aplicaron
        for patron, count in contador_reemplazos.items():
            if count > 0:
                patron_corto = patron[:20] + '...' if len(patron) > 20 else patron
                print(f"     • '{patron_corto}' -> {count:,} veces")
        
        print("───────────────────────────────────────────────────────────────────")
        print(f"  🛡️  BACKUP GUARDADO:")
        print(f"     {os.path.basename(ruta_backup):<61}")
        print("───────────────────────────────────────────────────────────────────")
        print()
        print("✅ OPERACIÓN COMPLETADA CON ÉXITO")
        print("⚠️  El archivo de backup se mantiene por seguridad.")
        
    except Exception as e:
        print()
        print()
        print("╔═════════════════════════════════════════════════════════════════╗")
        print("║     ERROR AL PROCESAR EL ARCHIVO                                ║")
        print("╚═════════════════════════════════════════════════════════════════╝")
        
        # Mostrar el error en múltiples líneas si es necesario
        error_msg = str(e)
        while error_msg:
            linea = error_msg[:61]
            print(f"║  {linea:<61}║")
            error_msg = error_msg[61:]
        
        print("───────────────────────────────────────────────────────────────────")
        
        # Intentar limpiar archivos temporales
        if archivo_temporal and os.path.exists(archivo_temporal):
            try:
                os.remove(archivo_temporal)
                print("  🧹 Archivo temporal eliminado")
            except:
                pass
        
        # Informar sobre el backup
        if backup_creado and os.path.exists(backup_creado):
            print("  ✓ TUS DATOS ESTÁN SEGUROS")
            print(f"  🛡️  Backup disponible:")
            print(f"     {os.path.basename(backup_creado):<61}")
        
        print("───────────────────────────────────────────────────────────────────")
        input("\nPresiona Enter para salir...")
        sys.exit(1)

def solicitar_archivo():
    """Solicita la ruta del archivo al usuario"""
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│  Ingresa la ruta del archivo a procesar                         │")
    print("│  (o arrastra el archivo aquí y presiona Enter)                  │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()
    ruta = input("📁 Ruta del archivo: ").strip().strip('"')
    return ruta

if __name__ == "__main__":
    mostrar_cabecera()
    
    # Si se arrastró un archivo sobre el .bat
    if len(sys.argv) >= 2:
        archivo = sys.argv[1]
    else:
        # Si se ejecutó directamente, pedir el archivo
        archivo = solicitar_archivo()
    
    print()
    
    if not os.path.exists(archivo):
        print("┌─────────────────────────────────────────────────────────────────┐")
        print("│    ERROR: El archivo no existe                                  │")
        print("└─────────────────────────────────────────────────────────────────┘")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    print("═" * 69)
    reemplazar_caracteres(archivo)
    print("═" * 69)
    print()
    
    # Preguntar si quiere procesar otro archivo
    while True:
        respuesta = input("¿Deseas procesar otro archivo? (S/N): ").strip().upper()
        if respuesta == 'S':
            print()
            print("░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░")
            print("░░░░▒▒▒▒▓▓▓                    SIGUIENTE ARCHIVO                    ▓▓▓▒▒▒▒░░░░")
            print("░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░")
            print()
            archivo = solicitar_archivo()
            if os.path.exists(archivo):
                print()
                print("═" * 69)
                reemplazar_caracteres(archivo)
                print("═" * 69)
                print()
            else:
                print()
                print("┌─────────────────────────────────────────────────────────────────┐")
                print("│     ERROR: El archivo no existe                                 │")
                print("└─────────────────────────────────────────────────────────────────┘")
                break
        elif respuesta == 'N':
            print()
            print("👋 ¡Hasta pronto!")
            time.sleep(1)
            break
        else:
            print("⚠️  Por favor, responde S (Sí) o N (No)")
