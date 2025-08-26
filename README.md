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
