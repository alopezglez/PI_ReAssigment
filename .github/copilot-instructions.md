# Instrucciones para GitHub Copilot

## 🚫 NUNCA CREAR

### Archivos de Documentación NO Deseados:
- ❌ NUNCA crear archivos .md (Markdown) de resumen o documentación
- ❌ NUNCA crear CHANGELOG.md, CHANGES.md, RESUMEN.md, etc.
- ❌ NUNCA crear archivos de "documentación de cambios"
- ❌ NUNCA crear archivos README adicionales sin solicitud explícita
- ❌ NUNCA crear archivos de "ejemplo" o "tutorial" no solicitados

### Excepciones (Solo si se solicita explícitamente):
- ✅ README.md principal del proyecto (si se pide)
- ✅ Documentación técnica específica (si se solicita)

---

## ✅ SIEMPRE CONFIRMAR ANTES DE:

### Operaciones Destructivas:
1. **Eliminar archivos o carpetas**
   - Preguntar: "¿Confirmas eliminar [archivo]?"
   - Esperar respuesta explícita

2. **Mover o renombrar archivos importantes**
   - Mostrar: origen → destino
   - Preguntar: "¿Confirmas mover estos archivos?"

3. **Modificaciones masivas**
   - Listar archivos a modificar
   - Preguntar: "¿Confirmas estos cambios?"

4. **Reorganización de estructura**
   - Mostrar estructura actual vs. propuesta
   - Preguntar: "¿Confirmas la reorganización?"

### Operaciones Complejas:
1. **Refactorización de código**
   - Explicar qué se va a cambiar
   - Preguntar: "¿Procedo con la refactorización?"

2. **Cambios en lógica de negocio**
   - Describir impacto del cambio
   - Preguntar: "¿Confirmas este cambio de lógica?"

3. **Instalación de dependencias nuevas**
   - Listar dependencias a instalar
   - Preguntar: "¿Confirmas instalar estas librerías?"

4. **Cambios en archivos de configuración**
   - Mostrar cambios a realizar
   - Preguntar: "¿Confirmas estos cambios de configuración?"

---

## 💡 COMPORTAMIENTO PREFERIDO

### Respuestas:
- ✅ **Directas y concisas**: Ir al grano
- ✅ **Solo código necesario**: No explicaciones innecesarias
- ✅ **Confirmar antes de ejecutar**: Operaciones complejas
- ❌ **NO crear documentación**: A menos que se solicite
- ❌ **NO resúmenes automáticos**: En archivos Markdown

### Formato de Confirmación:
```
🔍 Acción propuesta: [descripción]

Archivos afectados:
  • archivo1.py
  • archivo2.js

¿Confirmas esta operación? (Responde S/N)
```

### Flujo de Trabajo:
1. **Usuario solicita tarea**
2. **Copilot analiza complejidad**
3. **Si es compleja**: Solicitar confirmación
4. **Si es simple**: Ejecutar directamente
5. **Reportar resultado** (sin crear archivos de documentación)

---

## 📝 TIPOS DE SOLICITUDES

### Ejecutar Inmediatamente (SIN confirmar):
- Lectura de archivos
- Búsquedas en código
- Análisis de errores
- Corrección de bugs simples (1-2 líneas)
- Formateo de código

### Confirmar Antes (SIEMPRE):
- Eliminación de archivos
- Movimiento de archivos
- Refactorización
- Cambios de estructura
- Instalación de paquetes
- Modificación de múltiples archivos
- Cambios en lógica de negocio

---

## 🎯 EJEMPLOS

### ❌ MAL (No hacer):
```
Usuario: "Corrige el bug en ajustar_facturas.py"

Copilot: 
[Corrige el bug]
[Crea CAMBIOS.md documentando el fix]
[Crea RESUMEN.md con explicación]
```

### ✅ BIEN (Hacer):
```
Usuario: "Corrige el bug en ajustar_facturas.py"

Copilot: 
[Corrige el bug]
"✅ Bug corregido en ajustar_facturas.py línea 1063"
[FIN - No crea documentación]
```

---

### ❌ MAL (No hacer):
```
Usuario: "Reorganiza la estructura de carpetas"

Copilot:
[Mueve archivos inmediatamente]
[Crea ESTRUCTURA.md]
[Crea MIGRACION.md]
```

### ✅ BIEN (Hacer):
```
Usuario: "Reorganiza la estructura de carpetas"

Copilot:
"🔍 Acción propuesta: Reorganizar estructura

Cambios:
  • Crear scripts/
  • Mover *.py → scripts/
  • Actualizar rutas en código

¿Confirmas? (S/N)"

[Espera respuesta]
[Si S: ejecuta]
[Si N: cancela]
[NO crea documentación]
```

---

## 🔧 CONFIGURACIÓN DE PROYECTO

### Archivos Importantes (NO tocar sin confirmar):
- `EJECUTAR.bat` - Ejecutable principal
- `scripts/*.py` - Scripts Python
- Carpetas: `originales/`, `archivos/`, `resultados/`

### Archivos Permitidos Crear (solo si se solicita):
- Scripts Python (.py) si se pide
- Archivos de datos (.txt, .xlsx) si se pide
- Archivos de configuración (.json, .ini) si se pide

### Archivos NUNCA Crear (salvo solicitud explícita):
- Archivos .md de documentación
- Archivos de changelog
- Archivos de resumen
- Archivos de ejemplo
- Archivos de tutorial

---

## 📌 RESUMEN

### Regla de Oro:
> **"Si no se pidió explícitamente, no lo crees"**

### Principios:
1. 🚫 **NUNCA** crear archivos .md de documentación automáticamente
2. ✅ **SIEMPRE** confirmar operaciones complejas/destructivas
3. 💬 **RESPONDER** de forma directa y concisa
4. 🎯 **ENFOCARSE** en resolver el problema solicitado
5. 📝 **NO DOCUMENTAR** a menos que se solicite

---

**Última actualización**: 14 de noviembre de 2025  
**Versión**: 1.0
