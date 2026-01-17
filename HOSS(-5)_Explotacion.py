# -*- coding: utf-8 -*-
"""
HOSS(-5)_Explotacion.py
Explotación unificada
FASES (MAT_ACT en dos matrices pob y act + HOSS (CSV/XLSX)
Una sola GUI · Arquitectura simple y robusta
"""

import os
import sys
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from scipy import stats                     # >>> NUEVO GAMMA
import openpyxl                             # >>> NUEVO GAMMA

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

OUTPUT_DIR = r"C:\Users\Pepo\ph_5_Working\Notebooks"
MAT_ACT_DIR = r"C:\Users\Pepo\ph_5_Working"
MAT_ACT_PATH = os.path.join(MAT_ACT_DIR, "auditoria_mat_act.npy")
MAT_POB_PATH = os.path.join(MAT_ACT_DIR, "auditoria_mat_pob.npy")   # >>> NUEVO GAMMA
CSV_HOSS = os.path.join(MAT_ACT_DIR, "hoss_parametrizado.csv")
XLSX_HOSS = os.path.join(MAT_ACT_DIR, "hoss_parametrizado.xlsx")   # >>> NUEVO GAMMA

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# PARTE 1 — ESPACIO DE FASES (MAT_ACT)
# ============================================================


# ============================================================
# PARTE 1 — ESPACIO DE FASES (MAT_ACT)
# ============================================================


NIVELES = {
    1: {"valor": 0.1, "acts": [2,3,4]},
    2: {"valor": 0.2, "acts": [5,6,7,8]},
    3: {"valor": 0.3, "acts": [9,10,11,12,13,14]},
    4: {"valor": 0.4, "acts": [15,16,17,18,19,20]},
    5: {"valor": 0.5, "acts": [21,22,23,24,25,26,27]},
}
PESO_ACTIVIDAD = 1 / 26


def actividades_activas(mat_act, año, dni):
    return [
        act for act in range(mat_act.shape[2])
        if mat_act[año, dni, act, 0] > 0
    ]


def genera_indice_año(acts_activas):
    valor1 = 0.0
    for cfg in NIVELES.values():
        if any(act in cfg["acts"] for act in acts_activas):
            valor1 = max(valor1, cfg["valor"])
    valor2 = len(acts_activas) * PESO_ACTIVIDAD
    return valor1 + valor2



def genera_datos_Fases(
        file_pob='auditoria_mat_pob.npy',
        file_act='auditoria_mat_act.npy',
        edad_min=18,
        max_dni=None
    ):
    """
    Genera datos para espacios de fases:
    un punto por año vivido y por DNI.

    Devuelve:
        data = [dni, indice_inten, palp, edad]
    """

    if not os.path.exists(file_pob) or not os.path.exists(file_act):
        print("❌ Error: ejecutar la simulación antes (faltan .npy)")
        return []

    try:
        mat_pob = np.load(file_pob)
        mat_act = np.load(file_act)
    except Exception as e:
        print(f"❌ Error al cargar matrices: {e}")
        return []

    n_anios, n_dni, _ = mat_pob.shape
    data = []
    contador_dni = 0
    lifespans = []
    # Recorremos DNIs
    for dni in range(n_dni):

        # Buscar primer año en que el DNI está vivo
        anios_vivo = np.where(mat_pob[:, dni, 0] > 0)[0]
        if len(anios_vivo) == 0:
            continue

        contador_dni += 1
        if max_dni and contador_dni > max_dni:
            break

        # Recorremos toda su vida
        for anio in anios_vivo:
            anio_nac = anios_vivo[0]
            edad = anio - anio_nac
            if edad < edad_min:
                continue

            palp = float(mat_pob[anio, dni, 1])

            acts = actividades_activas(mat_act, anio, dni)
            indice = round(genera_indice_año(acts), 3)

            data.append([
                int(dni),
                indice,
                palp,
                int(edad)
            ])

        anios_vivo = np.where(mat_pob[:, dni, 0] > 0)[0]
        if len(anios_vivo) > 0:
            lifespans.append(len(anios_vivo))
        print(f"DNI {dni}: {len(anios_vivo)} años vivos, "
              f"{sum(1 for a in anios_vivo if (a - anios_vivo[0]) >= edad_min)} puntos útiles")
      
    print("Vida media DNI:", np.mean(lifespans))
    print("Vida máxima DNI:", np.max(lifespans))
    print("DNIs con vida >=17 años:", sum(l >= 17 for l in lifespans))
    print(f"✔️ Total puntos de fase generados: {len(data)}")
    return data

def dibu_espacio_fase(data, output_dir=None, guardar=True):

    if not data:
        print("⚠️ No hay datos de fase para mostrar (data vacía).")
        return

    datos_por_dni = {}
    for dni, ind, palp, edad in data:
        datos_por_dni.setdefault(dni, []).append((ind, palp, edad))

    if guardar and output_dir:
        os.makedirs(output_dir, exist_ok=True)

    for dni, lista in datos_por_dni.items():
        x = np.array([v[0] for v in lista])
        y = np.array([v[1] for v in lista])
        z = np.array([v[2] for v in lista])

        X = np.column_stack((x, y))
        poly = PolynomialFeatures(2)
        Xp = poly.fit_transform(X)

        model = LinearRegression()
        model.fit(Xp, z)

        xg, yg = np.meshgrid(
            np.linspace(x.min(), x.max(), 80),
            np.linspace(y.min(), y.max(), 80)
        )
        zg = model.predict(
            poly.transform(np.column_stack((xg.ravel(), yg.ravel())))
        ).reshape(xg.shape)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z)
        ax.plot_surface(xg, yg, zg, alpha=0.4)

        ax.set_xlabel("Índice intencionalidad")
        ax.set_ylabel("PALP")
        ax.set_zlabel("Edad")
        ax.set_title(f"Espacio de fase · DNI {dni}")
        if guardar and output_dir:
            plt.savefig(os.path.join(output_dir, f"dni_{dni:03d}.png"))
            plt.close(fig)
        else:
            plt.show()
            plt.close(fig)
    return

def mostrar_un_dni(output_dir, dni):
    fname = os.path.join(output_dir, f"dni_{dni:03d}.png")
    if os.path.exists(fname):
        img = plt.imread(fname)
        plt.imshow(img)
        plt.axis("off")
        plt.show()
    else:
        messagebox.showwarning("Fase", f"No existe gráfico guardado para DNI {dni}")

# ============================================================
# PARTE 2 — HOSS (CSV)
# ============================================================

VAR_LABELS = {
    'Poblacion': 'Población total',
    'Nacidos': 'Nacimientos por año',
    'Muertos': 'Defunciones por año',
    'Tasa hijos x mujer': 'Tasa de hijos por mujer',
    'IDH': 'Índice de Desarrollo Humano',
    'Gini': 'Índice de desigualdad (Gini)',
    'PIB': 'Producto Interior Bruto',
    'ISP': 'Índice de Sostenibilidad Pública',
    'Paro': 'Tasa de paro',
    'IAE': 'Índice de Actividad Económica',
    'RBU': 'Renta Básica Universal',
    'pagoxTrabOrgaS': 'Pagos por trabajo en organizaciones',
    'pagoxTrabEmprS': 'Pagos por trabajo en empresas',
    'ingrxRBUS': 'Ingresos por RBU',
    'comprphS': 'Consumo personas',
    'impuPhS': 'Impuestos personas',
    'otroPhS(ahorro)': 'Ahorro personas',
    'otroPhS(INVERSION)': 'Inversión personas',
    'EquilibrioPh': 'Equilibrio personas',
    'EquilibrioEmpr': 'Equilibrio empresas',
    'EquilibrioOrga': 'Equilibrio Estado',
}

GENERAL_VARS = [
    'Poblacion','Nacidos','Muertos','IDH','Gini','PIB','ISP',
    'Paro','IAE','RBU','pagoxTrabOrgaS','pagoxTrabEmprS',
    'ingrxRBUS','comprphS','impuPhS','otroPhS(ahorro)',
    'otroPhS(INVERSION)','EquilibrioPh','EquilibrioEmpr','EquilibrioOrga'
]

HOSS_SCHEMA = {
    'ph': {
        'entradas': ['pagoxTrabOrgaS','pagoxTrabEmprS','ingrxRBUS'],
        'salidas': ['comprphS','impuPhS','otroPhS(ahorro)','otroPhS(INVERSION)'],
        'equilibrio': 'EquilibrioPh'
    },
    'empr': {
        'entradas': ['comprphS'],
        'salidas': ['pagoxTrabEmprS'],
        'equilibrio': 'EquilibrioEmpr'
    },
    'orga': {
        'entradas': ['impuPhS'],
        'salidas': ['pagoxTrabOrgaS','ingrxRBUS'],
        'equilibrio': 'EquilibrioOrga'
    }
}


def etiqueta_usuario(var):
    return VAR_LABELS.get(var, var)

def cargar_csv_hoss(path):

    if not os.path.exists(path):
        print("⚠️ CSV no encontrado:", path)
        return pd.DataFrame()

    # --- Intento 1: separador coma
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp1252")

    # --- Si solo hay UNA columna y contiene ';', releer con ';'
    if len(df.columns) == 1 and ';' in df.columns[0]:
        try:
            df = pd.read_csv(path, sep=';', encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(path, sep=';', encoding="cp1252")

    # --- Limpieza de nombres
    df.columns = [c.strip() for c in df.columns]

    # --- Localizar columna tiempo
    posibles = ["Año", "Tiempo", "YEAR", "Year", "year", "time", "Time"]
    col_tiempo = None

    for c in posibles:
        if c in df.columns:
            col_tiempo = c
            break

    if col_tiempo is None:
        print("❌ CSV sin columna de tiempo reconocible.")
        print("Columnas encontradas:", list(df.columns))
        return pd.DataFrame()

    # --- Normalizar SIEMPRE a "Año"
    if col_tiempo != "Año":
        df = df.rename(columns={col_tiempo: "Año"})

    # --- Asegurar tipo numérico
    df["Año"] = pd.to_numeric(df["Año"], errors="coerce")
    df = df.dropna(subset=["Año"])

    return df

def plot_general(df, var, show=False):
    if var not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["Año"], df[var])
    ax.set_title(etiqueta_usuario(var))
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"GENERAL_{var}.png"))
    if show:
        plt.show()
    else:
        plt.close(fig)

def verificar_equilibrios(df, schema, tol=10):

    fig_all, ax_all = plt.subplots(figsize=(10,5))

    colores = {
        'ph': 'tab:blue',
        'empr': 'tab:orange',
        'orga': 'tab:green'
    }

    for entidad, cfg in schema.items():
        eq = cfg['equilibrio']
        if eq not in df.columns:
            continue

        ingresos = df[cfg['entradas']].sum(axis=1)
        gastos = df[cfg['salidas']].sum(axis=1)
        balance = ingresos - gastos

        # --- Gráfico individual (como ahora)
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(df['Año'], balance)
        ax.axhline(0, color='black')
        ax.set_title(f"Equilibrio {entidad.upper()}")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f"EQ_{entidad}.png"))
        plt.close(fig)

        # --- Añadir al gráfico conjunto
        ax_all.plot(
            df['Año'],
            balance,
            label=f"{entidad.upper()}",
            color=colores.get(entidad, None)
        )

    # --- Gráfico conjunto
    ax_all.axhline(0, color='black', linewidth=1)
    ax_all.set_title("Equilibrios HOSS · Conjunto")
    ax_all.set_xlabel("Año")
    ax_all.set_ylabel("Ingresos − Gastos")
    ax_all.legend()
    ax_all.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "EQ_TODOS.png"))
    plt.close(fig_all)

def explotacion_gamma_desigualdad(
        mat_pob_path,
        xlsx_path,
        edad_min=18,
        min_obs=30,
        eps=1e-6
    ):
    """
    Contraste empírico:
    Gamma (micro) vs IDH / Gini (macro)
    """

    if not os.path.exists(mat_pob_path):
        messagebox.showerror("Gamma", "No existe auditoria_mat_pob.npy")
        return

    if not os.path.exists(xlsx_path):
        messagebox.showerror("Gamma", "No existe hoss_parametrizado.xlsx")
        return

    mat_pob = np.load(mat_pob_path)

    # ---- Gamma empírico anual
    alphas = []
    n_obs  = []

    for anio in range(mat_pob.shape[0]):
        ingresos = []

        for dni in range(mat_pob.shape[1]):
            edad = mat_pob[anio, dni, 0]
            palp = mat_pob[anio, dni, 1]
            if edad >= edad_min:
                ingresos.append(palp)

        ingresos = np.array(ingresos)

        if len(ingresos) < min_obs:
            alphas.append(np.nan)
            n_obs.append(len(ingresos))
            continue

        min_ing = ingresos.min()
        if min_ing <= 0:
            ingresos = ingresos - min_ing + eps

        try:
            alpha, loc, beta = stats.gamma.fit(ingresos, floc=0)
            alphas.append(alpha)
        except Exception:
            alphas.append(np.nan)

        n_obs.append(len(ingresos))

    # ---- Macro indicadores (XLSX)
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active

    data = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        data.append({
            "Año": row[0],
            "IDH": row[5],
            "Gini": row[6]
        })

    df = pd.DataFrame(data)
    df["alpha_emp"] = alphas[:len(df)]
    df["n_obs"] = n_obs[:len(df)]
    df = df.dropna(subset=["alpha_emp", "IDH", "Gini"])

    # ---- Contrastes
    c_idh = {
        "Pearson":  stats.pearsonr(df["alpha_emp"], df["IDH"]),
        "Spearman": stats.spearmanr(df["alpha_emp"], df["IDH"]),
        "Kendall":  stats.kendalltau(df["alpha_emp"], df["IDH"])
    }

    c_gini = {
        "Pearson":  stats.pearsonr(df["alpha_emp"], df["Gini"]),
        "Spearman": stats.spearmanr(df["alpha_emp"], df["Gini"]),
        "Kendall":  stats.kendalltau(df["alpha_emp"], df["Gini"])
    }

    print("\n=== CONTRASTES α_emp vs IDH ===")
    print(c_idh)
    print("\n=== CONTRASTES α_emp vs Gini ===")
    print(c_gini)

    # ---- Gráficos
    plt.figure()
    plt.plot(df["Año"], df["alpha_emp"], marker="o")
    plt.title("Evolución temporal de α_emp (Gamma)")
    plt.xlabel("Año")
    plt.ylabel("α_emp")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.scatter(df["alpha_emp"], df["Gini"])
    plt.xlabel("α_emp")
    plt.ylabel("Gini")
    plt.title("α_emp vs Gini")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.scatter(df["alpha_emp"], df["IDH"])
    plt.xlabel("α_emp")
    plt.ylabel("IDH")
    plt.title("α_emp vs IDH")
    plt.grid(True)
    plt.show()

    messagebox.showinfo(
        "Gamma",
        "Hipótesis Gamma ejecutada.\nResultados por consola y gráficos en pantalla."
    )
# ============================================================
# TEXTO · EXPLOTACIÓN AVANZADA (DOCUMENTACIÓN INTERNA)
# ============================================================
TEXTO_EXPLOTACION_AVANZADA = """
EXPLORACIÓN AVANZADA DE RESULTADOS · HOSS

El módulo de Explotación de HOSS permite analizar los resultados de una simulación
desde distintos niveles de agregación, sin modificar en ningún caso el modelo
subyacente ni introducir hipótesis adicionales durante la fase de análisis.

Su objetivo es facilitar la observación, comparación e interpretación de los
datos generados, distinguiendo explícitamente entre comportamientos individuales
(nivel micro) y patrones agregados del sistema (nivel macro).

La explotación no añade conocimiento al modelo, pero sí contexto interpretativo
al análisis. Su función es ayudar al usuario a comprender qué está viendo,
qué puede comparar y qué tipo de inferencias son razonables a partir de los
resultados mostrados.

------------------------------------------------------------
1. ESPACIOS DE FASES INDIVIDUALES (NIVEL MICRO)
------------------------------------------------------------

La opción de Espacios de Fases representa trayectorias individuales de las
entidades ph() a lo largo del tiempo, proyectadas sobre un espacio de estados
definido por variables internas relevantes del modelo.

Cada punto corresponde al estado anual de un individuo adulto (edad ≥ 18),
y cada trayectoria describe la evolución dinámica de dicho individuo dentro
del sistema, no como una simple serie temporal, sino como una dinámica de estado.

Estas representaciones permiten:
- detectar regímenes estables o inestables a nivel individual
- observar dispersión, concentración o recorridos recurrentes
- comparar trayectorias entre individuos sin agregación previa
- explorar cómo las reglas del sistema afectan a biografías económicas concretas

Los espacios de fases no pretenden explicar causas, sino describir geometrías
dinámicas compatibles con el modelo. No se utilizan para predicción individual,
sino para explorar el espacio de posibilidades que el sistema permite.

------------------------------------------------------------
2. SERIES TEMPORALES AGREGADAS (NIVEL MACRO)
------------------------------------------------------------

Las series temporales agregadas condensan la información individual en magnitudes
globales del sistema, calculadas año a año a partir de la simulación.

Entre estas magnitudes se incluyen variables demográficas, económicas y
contables (población, PIB, IDH, Gini, RBU, equilibrios sectoriales, etc.).

Este nivel de análisis permite:
- observar tendencias globales del sistema
- identificar cambios de régimen o transitorios prolongados
- detectar convergencias, divergencias o ciclos
- verificar la coherencia contable entre agentes

La agregación implica pérdida de información individual, pero gana legibilidad
a escala del sistema completo. Las magnitudes representadas deben interpretarse
como propiedades emergentes del conjunto de interacciones simuladas, no como
atributos de ningún individuo concreto.

------------------------------------------------------------
3. CONTRASTE ESTRUCTURAL MICRO–MACRO (HIPÓTESIS GAMMA)
------------------------------------------------------------

La opción “Hipótesis Gamma vs Desigualdad” introduce un nivel adicional de análisis
estructural entre microdatos individuales y variables macroeconómicas agregadas.

A partir de los ingresos individuales de la población adulta, se ajusta
anualmente una distribución Gamma, obteniendo su parámetro de forma α como
descriptor de la estructura distributiva microeconómica.

Este parámetro se contrasta con indicadores agregados de desigualdad
(Gini e IDH), evaluando si existe una relación estructural entre:
- la forma de la distribución de ingresos individuales
- el comportamiento agregado del sistema

El contraste se realiza sin suavizados ni agregaciones artificiales,
manteniendo explícitamente ingresos negativos y aplicando únicamente un
desplazamiento técnico mínimo para permitir el ajuste estadístico.

Los resultados muestran una relación monótona negativa y estadísticamente
significativa bajo contrastes no paramétricos entre α y los indicadores de
desigualdad, aunque dicha relación no es lineal ni determinista.

En fases avanzadas de la simulación, el sistema puede entrar en regímenes de
fuerte homogeneización económica, en los que la distribución de ingresos pierde
estructura asimétrica y el parámetro α reduce su capacidad discriminativa.

Este análisis no establece relaciones causales directas, pero es compatible con
la hipótesis de que la estructura microeconómica contiene información relevante
sobre la desigualdad agregada.

------------------------------------------------------------
INTERPRETACIÓN CONJUNTA Y USO RECOMENDADO
------------------------------------------------------------

Las tres capas de análisis no deben interpretarse de forma aislada:
- los espacios de fases muestran qué puede ocurrirle a un individuo
- las series temporales muestran qué le ocurre al sistema
- el contraste Gamma explora cómo se relacionan ambas escalas

HOSS no proporciona predicciones empíricas, sino un entorno experimental que
permite comparar escenarios y observar cómo determinadas reglas generan
determinados regímenes económicos y sociales.

La explotación avanzada es especialmente útil para comparar simulaciones con
parámetros distintos (RBU, fiscalidad, salarios, demografía, duración),
y los resultados deben interpretarse siempre de forma comparativa y estructural,
no como valores absolutos extrapolables a sistemas reales.
(ChatGPT)
"""

# ============================================================
# GUI UNIFICADA
# ============================================================

class MainGUI:

    def __init__(self, root, mat_act):
        self.root = root
        self.mat_act = mat_act
        self.df = cargar_csv_hoss(CSV_HOSS)

        root.title("HOSS (-5) · Explotación unificada")
        root.geometry("540x680")

        self.build()

    def build(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Explotación HOSS (-5)", font=("Segoe UI",11,"bold")).pack(anchor="w")
        #-------
        ttk.Button(
            top,
            text="Explotación avanzada",
            command=self.mostrar_explotacion_avanzada
        ).pack(anchor="w", pady=(5, 5))

        #--------
        self.flag_fase_todos = tk.BooleanVar()
        self.flag_fase_dni = tk.BooleanVar()
        self.flag_equilibrios = tk.BooleanVar()
        self.flag_vars = {}
        self.flag_gamma = tk.BooleanVar()   # >>> NUEVO GAMMA
        ttk.Checkbutton(
            top,
            text="Hipótesis Gamma vs Desigualdad",
            variable=self.flag_gamma
            ).pack(anchor="w")

        ttk.Checkbutton(top, text="Fases (todos)", variable=self.flag_fase_todos).pack(anchor="w")
        ttk.Checkbutton(top, text="Fase por DNI", variable=self.flag_fase_dni).pack(anchor="w")
        ttk.Checkbutton(top, text="Equilibrios HOSS", variable=self.flag_equilibrios).pack(anchor="w")

        ttk.Separator(self.root).pack(fill="x", pady=5)

        center = ttk.Frame(self.root, padding=5)
        center.pack(fill="both", expand=True)

        canvas = tk.Canvas(center, height=380)
        scrollbar = ttk.Scrollbar(center, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for v in GENERAL_VARS:
            f = tk.BooleanVar()
            self.flag_vars[v] = f
            ttk.Checkbutton(frame, text=etiqueta_usuario(v), variable=f).pack(anchor="w")

        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack(fill="x")

        ttk.Button(bottom, text="TODO", command=self.todo).pack(side="left", padx=5)
        ttk.Button(bottom, text="GENERAR", command=self.generar).pack(side="left", padx=5)
        ttk.Button(bottom, text="CERRAR", command=self.root.destroy).pack(side="right", padx=5)

    def todo(self):
        self.flag_fase_todos.set(True)
        self.flag_fase_dni.set(True)
        self.flag_equilibrios.set(True)
        self.flag_gamma.set(True)   # >>> NUEVO GAMMA

        for f in self.flag_vars.values():
            f.set(True)
        #----
        
    def mostrar_explotacion_avanzada(self):
        win = tk.Toplevel(self.root)
        win.title("HOSS · Explotación avanzada")
        win.geometry("720x560")
    
        frame = ttk.Frame(win, padding=10)
        frame.pack(fill="both", expand=True)
    
        text = tk.Text(
            frame,
            wrap="word",
            font=("Segoe UI", 10),
            state="normal"
        )
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
    
        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        text.insert("1.0", TEXTO_EXPLOTACION_AVANZADA)
        text.config(state="disabled")

        #----
    def generar(self):
        #  Recargar CSV SIEMPRE antes de explotar
        self.df = cargar_csv_hoss(CSV_HOSS)
        if self.flag_gamma.get():
            explotacion_gamma_desigualdad(
            MAT_POB_PATH,
            XLSX_HOSS
            )

        if self.flag_fase_todos.get():
            resp = messagebox.askyesno("Fases","¿Guardar gráficos en disco?")
            #data = genera_datos_Fases()
            data = genera_datos_Fases(max_dni=20)  #Para pruebas:limitar número

            dibu_espacio_fase(data, OUTPUT_DIR if resp else None, guardar=resp)

        if self.flag_fase_dni.get():
            dni = simpledialog.askinteger("DNI","Introduce DNI:")
            if dni is not None:
                mostrar_un_dni(OUTPUT_DIR, dni)

        if self.flag_equilibrios.get() and not self.df.empty:
            verificar_equilibrios(self.df, HOSS_SCHEMA)

        for v, f in self.flag_vars.items():
            if f.get():
                plot_general(self.df, v, show=True)

        messagebox.showinfo("HOSS","Explotación finalizada.")
        print("Año máximo en CSV:", self.df["Año"].max())
        print("Filas CSV:", len(self.df))

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()   # Oculta mientras se decide el fichero

    if not os.path.exists(MAT_ACT_PATH):
        MAT_ACT_PATH = filedialog.askopenfilename(
            title="Selecciona auditoria_mat_act.npy",
            filetypes=[("NumPy", "*.npy")]
        )
        if not MAT_ACT_PATH:
            root.destroy()
            sys.exit(1)

    mat_act = np.load(MAT_ACT_PATH)

    root.deiconify()  # Ahora mostramos la ventana principal
    app = MainGUI(root, mat_act)
    root.mainloop()
