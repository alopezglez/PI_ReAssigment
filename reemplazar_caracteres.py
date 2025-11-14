import sys
import os
import time

def mostrar_cabecera():
    """Muestra la cabecera del programa"""
    print("\n")
    print("░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░")
    print("░░░░▒▒▒▒▓▓▓           REEMPLAZO DE CARACTERES EN ARCHIVOS           ▓▓▓▒▒▒▒░░░░")
    print("░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░")
    print()

def mostrar_barra_progreso(progreso, total, texto="Procesando"):
    """Muestra una barra de progreso"""
    porcentaje = int((progreso / total) * 100)
    barra_llena = int((progreso / total) * 40)
    barra_vacia = 40 - barra_llena
    
    barra = "█" * barra_llena + "░" * barra_vacia
    print(f"\r{texto}: [{barra}] {porcentaje}%", end="", flush=True)
    
    if progreso == total:
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
        'û': '┘',
        '[@DG]├': '├',
        '[@FG]├': '├',
        '[@FG]ö': '└',
        '÷': '┴',
        'ó': '┘'
    }
    
    try:
        print(f"📄 Archivo: {os.path.basename(ruta_archivo)}")
        print(f"📂 Ruta: {os.path.dirname(ruta_archivo)}")
        print()
        
        # Paso 1: Leer archivo
        mostrar_barra_progreso(1, 5, "Leyendo archivo")
        time.sleep(0.2)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        # Paso 2: Eliminar filas
        mostrar_barra_progreso(2, 5, "Eliminando filas")
        time.sleep(0.2)
        if len(lineas) > 4:
            lineas = lineas[4:]
        
        if len(lineas) > 3:
            lineas.pop(3)
        
        contenido = ''.join(lineas)
        
        # Paso 3: Realizar reemplazos
        mostrar_barra_progreso(3, 5, "Reemplazando caracteres")
        time.sleep(0.2)
        contenido_modificado = contenido
        total_reemplazos = len(reemplazos)
        for i, (antiguo, nuevo) in enumerate(reemplazos.items(), 1):
            contenido_modificado = contenido_modificado.replace(antiguo, nuevo)
        
        # Paso 4: Guardar archivo
        mostrar_barra_progreso(4, 5, "Guardando archivo")
        time.sleep(0.2)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_modificado)
        
        # Paso 5: Completado
        mostrar_barra_progreso(5, 5, "Completado")
        print()
        print()
        print("┌─────────────────────────────────────────────────────────────────┐")
        print("│  ✓ ARCHIVO PROCESADO CORRECTAMENTE                             │")
        print(f"│  • Filas eliminadas: 5 (4 primeras + fila 8)                   │")
        print(f"│  • Reemplazos aplicados: {total_reemplazos}                                      │")
        print("└─────────────────────────────────────────────────────────────────┘")
        
    except Exception as e:
        print()
        print()
        print("┌─────────────────────────────────────────────────────────────────┐")
        print("│     ERROR AL PROCESAR EL ARCHIVO                                │")
        print(f"│  {str(e)[:61]:<61}│")
        print("└─────────────────────────────────────────────────────────────────┘")
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
