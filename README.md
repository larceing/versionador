# 🗂️ Versionador de Archivos (Python + Tkinter)

Este proyecto permite versionar cualquier archivo de forma sencilla:
- Seleccionas el archivo de origen.
- Indicas la carpeta destino.
- Opcionalmente defines cuántas versiones mantener.
- Pulsas **"Versionar ahora"** → se crea una copia con timestamp en el nombre.

Ejemplo:
reporte.xlsx → reporte_20250826_221045.xlsx



---

## 🚀 Uso

### 1. Clonar o descargar
Descarga este repositorio o el archivo `app.py`.

### 2. Dependencias
Solo requiere Python 3.8+ (usa solo librerías estándar).
No necesitas instalar nada extra.

### 3. Ejecutar
-> bash
python app.py
o
app.exe

Se abrirá una ventana GUI.

### 4. Configuración

El programa crea automáticamente un archivo config.json en la misma carpeta:

{
  "ruta_origen": "C:/Users/TuUsuario/Documents",
  "archivo": "reporte.xlsx",
  "ruta_destino": "C:/Users/TuUsuario/Documents/Versiones",
  "max_versions": 5
}

ruta_origen: carpeta donde está el archivo original.

archivo: nombre del archivo a versionar.

ruta_destino: carpeta donde se guardarán las versiones.

max_versions: número de copias a conservar (0 = sin límite).

Cada vez que ejecutes, se crea una copia nueva con timestamp.
Si max_versions > 0, las más antiguas se eliminarán automáticamente.

💻 Empaquetar como EXE (opcional)

pip install pyinstaller
pyinstaller --onefile versionador.py

🎨 Interfaz

Hecha con Tkinter y ttk (tema moderno clam).

Botón principal azul, labels con estilos diferenciados.

Mensajes claros y barra de estado.

📜 Licencia

MIT (puedes usarlo y adaptarlo libremente).

Descargo de responsabilidad
Este código se publica exclusivamente con fines educativos y/o demostrativos y no incorpora garantías, explícitas o implícitas, incluidas, entre otras, idoneidad para un propósito particular, comerciabilidad, rendimiento o seguridad.
El usuario es responsable de revisar, adaptar, auditar, probar y validar el código antes de emplearlo en entornos de producción. En ningún caso el autor será responsable de daños directos, indirectos, incidentales, especiales, consecuenciales o de cualquier otra naturaleza derivados del uso o la imposibilidad de uso de este código.
El usuario debe garantizar el cumplimiento de leyes aplicables, políticas internas, licencias de dependencias y requisitos de seguridad. Este texto no constituye asesoramiento legal.
