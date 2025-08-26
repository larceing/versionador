# app.py
from __future__ import annotations
import sys, json, os, shutil, datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --------- UTIL: carpeta de la app (sirve en .py y en .exe) ----------
def app_dir() -> Path:
    if getattr(sys, "frozen", False):        # PyInstaller / exe
        return Path(sys.executable).parent
    return Path(__file__).parent.resolve()   # script .py

CONFIG_PATH = app_dir() / "config.json"

# --------- FUNCIÓN ÚNICA: versionado desde config.json ----------
def versionar(config_path: Path | None = None) -> Path:
    """
    Lee config.json (junto al .py/.exe) y crea una copia versionada del archivo.
    Config esperada:
      {
        "ruta_origen": "C:/.../",
        "archivo": "reporte.xlsx",
        "ruta_destino": "C:/.../Versiones/",
        "max_versions": 0   # opcional: 0 = sin límite
      }
    Devuelve la ruta del fichero creado.
    """
    cfg_path = Path(config_path or CONFIG_PATH)
    if not cfg_path.exists():
        raise FileNotFoundError(f"No existe config.json en:\n{cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)

    ruta_origen   = cfg.get("ruta_origen", "").strip()
    archivo       = cfg.get("archivo", "").strip()
    ruta_destino  = cfg.get("ruta_destino", "").strip()
    max_versions  = int(cfg.get("max_versions", 0) or 0)

    if not ruta_origen or not archivo or not ruta_destino:
        raise ValueError("Config incompleta: ruta_origen, archivo y ruta_destino son obligatorios.")

    src = Path(ruta_origen) / archivo
    if not src.is_file():
        raise FileNotFoundError(f"No existe el archivo origen:\n{src}")

    dst_dir = Path(ruta_destino)
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Usa Path para separar bien nombre y extensión
    p = Path(archivo)
    base = p.stem       # nombre sin extensión
    ext  = p.suffix     # extensión única, ej: ".xlsx"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = dst_dir / f"{base}_{ts}{ext}"

    shutil.copy2(src, dst)


    # Retención opcional: conservar solo las últimas N versiones
    if max_versions > 0:
        files = sorted(
            [p for p in dst_dir.glob(f"{base}_*{ext}") if p.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        for old in files[max_versions:]:
            try:
                old.unlink(missing_ok=True)
            except Exception:
                pass

    return dst


# ================== GUI mínima (bonita y sin magia rara) ==================
def ensure_config():
    """Crea config.json junto a la app si no existe."""
    if not CONFIG_PATH.exists():
        default = {
            "ruta_origen": "",
            "archivo": "",
            "ruta_destino": "",
            "max_versions": 0
        }
        CONFIG_PATH.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")

def load_config() -> dict:
    ensure_config()
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

def save_config(cfg: dict):
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Versionador de archivos")
        self.geometry("640x320")
        self.minsize(560, 280)

        # ttk style simple pero agradable
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("TButton", padding=8)
        style.configure("Primary.TButton", padding=10, background="#1f6feb", foreground="white")
        style.map("Primary.TButton", background=[("active", "#185fd0")])
        self.configure(bg="#F6F7FB")

        self.cfg = load_config()
        self._build_ui()

    def _build_ui(self):
        pad = 12
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="Versionador (config junto al programa)", font=("Segoe UI", 14, "bold"))
        title.pack(anchor="w", pady=(0, 8))

        card = ttk.Frame(frame, padding=12)
        card.pack(fill="x")
        card.configure(style="Card.TFrame")
        ttk.Style().configure("Card.TFrame", background="#FFFFFF")
        for w in (frame, self): ttk.Style().configure("TLabel")

        # Archivo origen
        ttk.Label(card, text="Archivo origen", background="#FFFFFF").grid(row=0, column=0, sticky="w")
        self.var_src = tk.StringVar(value=str(Path(self.cfg.get("ruta_origen","")) / self.cfg.get("archivo","")) if self.cfg.get("archivo") else "")
        ent_src = ttk.Entry(card, textvariable=self.var_src, state="readonly", width=60)
        btn_src = ttk.Button(card, text="Elegir archivo…", command=self.choose_src)
        ent_src.grid(row=1, column=0, sticky="we", padx=(0,pad), pady=(2,pad))
        btn_src.grid(row=1, column=1)

        # Carpeta destino
        ttk.Label(card, text="Carpeta destino", background="#FFFFFF").grid(row=2, column=0, sticky="w")
        self.var_dst = tk.StringVar(value=self.cfg.get("ruta_destino",""))
        ent_dst = ttk.Entry(card, textvariable=self.var_dst, state="readonly", width=60)
        btn_dst = ttk.Button(card, text="Elegir carpeta…", command=self.choose_dst)
        ent_dst.grid(row=3, column=0, sticky="we", padx=(0,pad), pady=(2,pad))
        btn_dst.grid(row=3, column=1)

        # Retención
        ttk.Label(card, text="Conservar solo las últimas N versiones (0 = sin límite)", background="#FFFFFF").grid(row=4, column=0, sticky="w")
        self.var_keep = tk.IntVar(value=int(self.cfg.get("max_versions", 0) or 0))
        spin = ttk.Spinbox(card, from_=0, to=999, textvariable=self.var_keep, width=6)
        spin.grid(row=5, column=0, sticky="w", pady=(2,0))

        card.columnconfigure(0, weight=1)

        # Botón principal
        ttk.Separator(frame).pack(fill="x", pady=(16,8))
        self.btn = ttk.Button(frame, text="Versionar ahora", style="Primary.TButton", command=self.on_versionar)
        self.btn.pack(pady=(0,8))

        self.status = ttk.Label(frame, text="", foreground="#6B7280")
        self.status.pack(anchor="w")

    def choose_src(self):
        initdir = self.cfg.get("ruta_origen") or str(Path.home())
        path = filedialog.askopenfilename(title="Selecciona archivo origen", initialdir=initdir)
        if path:
            p = Path(path)
            self.cfg["ruta_origen"] = str(p.parent)
            self.cfg["archivo"] = p.name
            save_config(self.cfg)
            self.var_src.set(str(p))

    def choose_dst(self):
        initdir = self.cfg.get("ruta_destino") or str(Path.home())
        d = filedialog.askdirectory(title="Selecciona carpeta de destino", initialdir=initdir)
        if d:
            self.cfg["ruta_destino"] = d
            save_config(self.cfg)
            self.var_dst.set(d)

    def on_versionar(self):
        # persistir keep
        try:
            self.cfg["max_versions"] = int(self.var_keep.get())
        except Exception:
            self.cfg["max_versions"] = 0
        save_config(self.cfg)

        try:
            self.btn.configure(state="disabled")
            self.status.config(text="Creando versión…")
            dst = versionar()  # 👈 LLAMADA A LA FUNCIÓN ÚNICA
            self.status.config(text=f"✔ Versión creada: {dst.name}")
            messagebox.showinfo("OK", f"Se guardó:\n{dst}")
        except Exception as e:
            self.status.config(text="")
            messagebox.showerror("Error", str(e))
        finally:
            self.btn.configure(state="normal")


# ---------- entrypoint ----------
if __name__ == "__main__":
    App().mainloop()
