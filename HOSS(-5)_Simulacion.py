"""
FICHERO: HOSS(-5)-15-10.py
Versión Depuración: Elimina multiproceso para garantizar volcado de datos.
Genera 'auditoria_mat_act.npy' al finalizar.
"""
import os
import random
import statistics
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Frame, Scrollbar, messagebox, ttk, Canvas, filedialog,scrolledtext
import pandas as pd 
import math
from collections import Counter
from scipy import stats
import warnings
import io
import json 
import sys
import time
import openpyxl

#from tkinter import scrolledtext
# --- ELIMINADO MULTIPROCESSING PARA EVITAR ERRORES DE MEMORIA ---
# from multiprocessing import shared_memory (Eliminado)

warnings.filterwarnings("ignore")

# ==========================================
# DATOS CSV INTEGRADOS (puestos_trabajo.csv)
# ==========================================
CSV_PUESTOS_DATA = """clave,descripcion,salarioMaxi,sector
1,Infancia,0,No asignado
2,Adolescencia,0,No asignado
3,Paro,11400,No asignado
4,Situacion que,0,No asignado
5,Jubilacion co,35000,No asignado
6,Jubilacion no,15000,No asignado
7,S-dificil,200000,finanzas
8,Cientifico de,101923,investigacion
9,Estadistico,75436,investigacion
10,Catedratico,67640,ensenanza
11,Terapeuta oc,74048,sanidad
12,Asesor genet,68957,ensenanza
13,Seguridad de,85004,software
14,Matematico,75436,ensenanza
15,Actuario,90388,administracion
16,Desarrollado,92168,software
17,Logopeda,68183,sanidad
18,Higienista de,65922,sanidad
19,Radioterapeu,71707,sanidad
20,Desarrollado,60511,software
21,Desarrollado,90593,software
22,Terapeuta Fi,77297,sanidad
23,Fisico,104326,ensenanza
24,Optometrista,98167,sanidad
25,Terapeuta de,35591,sanidad
26,Analista S In,78979,software
27,Meteorologo,83758,servicios
28,Gerente Reci,100837,servicios
29,Analista Fina,76237,finanzas
30,Biologo,83019,ensenanza
31,Redes Inform,73025,software
32,Quiropractic,63555,sanidad
33,Bibliotecario,52555,ensenanza
34,Secretario M,31826,sanidad
35,Terapia Ocup,51282,sanidad
36,Economista,92863,administracion
37,Ingeniero de,122081,industria
38,Tecnico de la,46574,investigacion
39,Veterinario,83509,campo
40,Ingeniero Ae,102546,investigacion
41,Farmaceutic,112247,sanidad
42,Redactor Tec,63915,administracion
43,Ingeniero Civ,77110,administracion
44,Traductor,44438,ensenanza
45,Contador,62745,finanzas
46,Ingeniero Ind,77466,industria
47,Artista Multi,64543,servicios
48,Dietista,53729,sanidad
49,Especialista,47588,industria
50,Ortodoncista,185120,sanidad
51,Diagnostico,63555,sanidad
52,Podologo,115300,sanidad
53,Consejero vo,50116,administracion
54,Tecnologo m,46075,sanidad
55,Estilista,23007,servicios
56,Programado,75009,software
57,Ingeniero Me,77759,industria
58,Historiador,54415,ensenanza
59,Ingeniero Ele,88172,industria
60,Gerente de M,51202,servicios
61,optico,32939,sanidad
62,Ingeniero Am,77982,industria
63,Psiquiatra,127671,servicios
64,Ingeniero Te,57254,industria
65,Geologo,81106,campo
66,Tecnico Farm,28258,sanidad
67,Enfermera Pr,101398,sanidad
68,Zoologo,56444,campo
69,Reparador d,25774,servicios
70,Psicologo,70319,sanidad
71,Quimico,68432,ensenanza
72,Juez,104299,seguridad
73,Cartografo,57343,ensenanza
74,Gerente de S,63306,administracion
75,Ingeniero Nu,95764,investigacion
76,Costurera,25454,servicios
77,Contador,35814,finanzas
78,Gerente de ve,80198,servicios
79,Gerente Soci,58135,servicios
80,Tecnico de la,32654,sanidad
81,Joyero,33784,servicios
82,Conservador,43076,servicios
83,Tecnico Elec,49119,industria
84,Sociologo,73025,administracion
85,Asistente Me,96663,sanidad
86,Medico,188484,sanidad
87,Director de c,84826,ensenanza
88,Dentista,139054,sanidad
89,Tecnico en C,51825,sanidad
90,Trabajador S,44028,ensenanza
91,Disenador In,59265,industria
92,Cirujano,227048,sanidad
93,Capacitacion,54174,servicios
94,Tecnico Vete,30634,servicios
95,Procesador c,35369,ensenanza
96,carretilla ele,39400,industria
97,Logista,66394,industria
98,Reparador d,45951,industria
99,Cientifico Ag,56978,campo
100,Asistente de,24003,ensenanza
101,investigacion,56177,investigacion
102,Fontanero,47980,servicios
103,Taquigrafo,50864,servicios
104,Gerente de C,83099,industria
105,Cuidado Per,21378,sanidad
106,Enfermera R,63840,sanidad
107,Conserje,23238,ensenanza
108,Reparador e,33962,industria
109,Examinador,48452,finanzas
110,Cajero finan,26211,finanzas
111,Recaudacion,53356,finanzas
112,Preparador c,35057,finanzas
113,Ayudante Sa,21413,servicios
114,Topografo,55696,industria
115,Arqueologo,55545,ensenanza
116,Tecnico de ra,38857,industria
117,Instalador de,35013,servicios
118,Clero,41919,servicios
119,Autor,55331,servicios
120,Ensamblado,28071,industria
121,Abogado,107610,ensenanza
122,Mecanico de,49929,software
123,Reclutador,54183,servicios
124,Inspector de,53133,servicios
125,Inspector de,35244,campo
126,Cajero,19963,finanzas
127,Reparador d,51522,industria
128,Trabajador c,22303,servicios
129,Reparador d,36784,industria
130,Directivo ser,93183,industria
131,Electricista,49119,industria
132,Tapicero de,28436,servicios
133,Maquinista,40006,industria
134,Ejecutivo de,99039,servicios
135,Tecnico en tu,48389,industria
136,Editor de pub,52937,servicios
137,Empleado de,28605,servicios
138,Inspector de,53578,servicios
139,Maestra de E,51602,ensenanza
140,Gerente de C,60164,servicios
141,Auxiliar de vu,49840,industria
142,Controlador,110841,administracion
143,Representan,54824,administracion
144,Operador de,41634,administracion
145,Piloto de aer,99618,industria
146,Lavaplatos,19345,servicios
147,Instalador So,37985,industria
148,Actor,32470,servicios
149,Trabajador c,48042,industria
150,Ejecutivo de,104246,servicios
151,Camarero,20070,servicios
152,Gerente de A,47517,servicios
153,Recepcionist,25935,servicios
154,Operador de,41821,industria
155,Empleada do,20345,servicios
156,Agente inmo,44767,servicios
157,Agente de se,45034,servicios
158,Recolector d,33161,servicios
159,Cristalero,38760,servicios
160,Auxiliar de e,24973,sanidad
161,Trabajador c,21316,servicios
162,Guardia de s,25392,seguridad
163,Disenador de,64721,servicios
164,Mecanico de,56123,industria
165,Broker de?yb,57067,finanzas
166,Entrenador d,35440,servicios
167,Asistente de,25392,sanidad
168,Ensamblado,29210,industria
169,Granjero,60476,campo
170,Arquitecto,70648,industria
171,Director de fu,51246,sanidad
172,Trabajador c,43129,industria
173,Ferretero,46965,servicios
174,Oficial de po,56034,seguridad
175,Servidor de c,19197,servicios
176,Carnicero,28106,servicios
177,Coordinador,42978,servicios
178,Carpintero,41465,campo
179,Fotografo,30260,servicios
180,Tecnico med,30545,sanidad
181,Coreografo,33633,servicios
182,Trabajador c,48416,industria
183,Soldador,36828,industria
184,Mecanico de,36232,industria
185,Comprador,55848,servicios
186,Cartero de co,52296,servicios
187,Conductor de,38875,servicios
188,Techador,35573,industria
189,Albanil,39881,industria
190,Obrero de co,30572,industria
191,Chef,43129,servicios
192,Trabajador c,31693,sanidad
193,Trabajador c,20684,servicios
194,Conductor d,30661,servicios
195,Bombero,43681,servicios
196,Trabajador p,25151,industria
197,Pintor,33704,industria
198,Emisora,55990,servicios
199,Vendedor de,46049,servicios
200,Tecnico en d,37407,industria
201,Disc Jockey,28471,servicios
202,Oficial penit,39516,seguridad
203,Militar,23854,seguridad
204,Vendedor mi,21663,servicios
205,Periodista pr,38706,servicios
206,Lenador,36179,campo
207,Taxista,23122,servicios"""


# -----------------------------------------------------------------------------
# 1. TEXTO DE DOCUMENTACIÓN (Formateado para lectura en GUI)
# -----------------------------------------------------------------------------
INFO_HOSS_TEXTO = """
DOCUMENTACIÓN DE REFERENCIA: MÓDULO DE SIMULACIÓN HOSS(-5)
HACIA LA VERSIÓN CERO
==========================================================

1. INTRODUCCIÓN Y PROPÓSITO
---------------------------
El módulo HOSS(-5) Simulación.py constituye el motor central actual del proyecto. 
Su objetivo no es representar la versión final (CERO), sino servir como un 
prototipo funcional avanzado que valida las dinámicas de población, economía 
básica y gestión de datos en memoria.

2. EL AGENTE: EL "PUNTO HUMANO" (ph)
------------------------------------
La unidad fundamental es el objeto ph(). Su modelado abarca:

  * Ciclo de Vida: Gestación, nacimiento y muerte. La mortalidad es probabilística 
    pero sensible a eventos (pandemias, crisis) y al desarrollo social.
  * Psicología: Definida por una Matriz Psicológica (Arquetipo x Carácter). 
    Las decisiones se mapean en un plano de Intencionalidad y Estatus Económico.
  * Actividades: Agenda anual entre actividades obligatorias, educativas, lúdicas, 
    organizativas y laborales.
  * Evolución: Mecanismo de carrera profesional, mejora de ingresos por formación 
    o azar, y profesionalización de aficiones.

3. ENTORNO SOCIAL Y MACROECONOMÍA
---------------------------------
Universo organizativo: ph() (familias), Empresas y Estado.

  * Estructura Productiva: Pool de empresas (10 sectores). Producción y precios 
    basados en azar/ajuste (no mercado libre aún). Salarios modulados por 200 categorías.
  * Rol del Estado: Provee servicios, empleo público y Renta Básica Universal (RBU). 
    Se financia con impuestos.
  * Homeostasis: Auto-regulación anual de impuestos y RBU para equilibrar déficits, 
    buscando saldo fiscal nulo con presión fiscal < 50%.
  * Métricas: Cálculo de Gini, IDH y verificación con distribución Gamma.

4. ARQUITECTURA TÉCNICA
-----------------------
  * Optimización RAM: Sustitución de MySQL por estructuras en memoria para alto rendimiento.
  * Persistencia: Volcado de memoria a archivos binarios, .csv y .xlsx para auditoría 
    externa al finalizar la simulación.
  * Interfaz: Configuración de parámetros y gestión de escenarios (guardar/cargar).

5. LIMITACIONES ACTUALES (LO QUE NO HACE)
-----------------------------------------
  * Sin "Relaciones" complejas directas entre ph().
  * Mercado simulado, no real (sin oferta/demanda en tiempo real).
  * Organizaciones "Caja Negra" (sin protocolos internos complejos).

6. HORIZONTES: HACIA LA VERSIÓN CERO
------------------------------------
Objetivos futuros para modelar áreas metropolitanas y complejidad política:

  1. Liderazgo de Recursos (Lrec) y General (LGen).
  2. Temperatura Ciudadana (TC) y Compromiso (Cag).
  3. Desempeño Institucional (Oficina Técnica y Organización Marco).
  4. Manejo de la Complejidad (MC).
(Gemini)
"""

# -----------------------------------------------------------------------------
# 2. FUNCIÓN PARA ABRIR LA VENTANA EMERGENTE
# -----------------------------------------------------------------------------
def abrir_ventana_info_hoss():
    """
    Abre una ventana secundaria (Toplevel) mostrando la documentación
    de HOSS(-5). Al cerrar, se regresa a la ventana principal.
    """
    ventana_info = tk.Toplevel()
    ventana_info.title("HOSS: Simulación Avanzada - Documentación")
    ventana_info.geometry("800x600")  # Tamaño inicial razonable

    # Título interno
    lbl_titulo = tk.Label(ventana_info, text="Resumen Técnico HOSS(-5)", 
                          font=("Helvetica", 14, "bold"), pady=10)
    lbl_titulo.pack()

    # Área de texto con scroll
    # Usamos ScrolledText para manejar textos largos cómodamente
    txt_area = scrolledtext.ScrolledText(ventana_info, wrap=tk.WORD, 
                                         font=("Consolas", 10), padx=10, pady=10)
    txt_area.pack(expand=True, fill='both', padx=10)

    # Insertamos el texto y lo hacemos de solo lectura
    txt_area.insert(tk.INSERT, INFO_HOSS_TEXTO)
    txt_area.configure(state='disabled') # Bloquea la edición para que solo se lea

    # Botón para cerrar
    btn_cerrar = tk.Button(ventana_info, text="Cerrar y Volver", 
                           command=ventana_info.destroy, 
                           bg="#dddddd", height=2)
    btn_cerrar.pack(pady=10, fill='x', padx=10)

    # Opcional: Hace que la ventana sea modal (obliga a cerrarla para usar la otra)
    # ventana_info.grab_set()

# ==========================================
# 1. CONFIGURACIÓN GLOBAL
# ==========================================
class Config:
    SIM_ANOS = 50           
    POB_INICIAL = 100       
    ANOS_ESCOLARIZACION = 14 
    
    RBU_ACTIVA = 1          
    SALARIO_MINIMO = 12600    
    RATIO_MM_PRIV_PUB = 1.0 
    RBU_PORC_PIB = 10.0     
    RBU_MONTO_ACTUAL = 8800 
    IAE_BASE = 25.0         
    FACTOR_IRPF = 1.0       
    UMBRAL_INVERSION = 30000 

    FERTILIDAD_BAJA = 0.25      
    FERTILIDAD_ALTA = 0.15      
    FERTILIDAD_POBREZA = 0.20   
    LIMITE_HIJOS = 7
    BRECHA_EDAD_PAREJA = 10
    FACTOR_MUERTE_VEJEZ = 1.1   
    ESPERANZA_VIDA = 80
    EDAD_JUBILACION = 65
    
    SALARIO_INI_MIN = 0.51      
    SALARIO_INI_MAX = 0.99
    VAR_SALARIAL_MEDIA = 1.03
    VAR_SALARIAL_DEV = 0.05
    OBJETIVO_EMPLEO_PUB = 0.15  
    PLUS_SALARIAL_PUB = 1.3
    
    PROPENSION_CONSUMO = 0.80 
    RIESGO_REBELDE = 0.05
    RIESGO_NORMAL = 0.01
    FACTOR_DESESPERACION = 0.10
    PROB_PELOTAZO = 0.02
    
    CICLO_CORTO_FREQ = 15
    CICLO_CORTO_IMPACTO = 0.75
    CICLO_LARGO_FREQ = 90
    CICLO_LARGO_IMPACTO = 0.50

    FACTOR_ECONOMICO = 1.0 
    INFLACION_SIMULADA = 0.0 
    
    TRAMOS_IRPF_BASE = [
        (20000, 0.00), (25000, 0.15), (50000, 0.25), (100000, 0.35), (float('inf'), 0.45)
    ]

    MAPA_SECTORES = {
        0: "industria", 1: "servicios", 2: "sanidad", 3: "ensenanza", 
        4: "administracion", 5: "investigacion", 6: "finanzas", 
        7: "software", 8: "seguridad", 9: "campo"
    }

# ==========================================
# 2. ACTIVIDADES Y DATOS
# ==========================================
ACTIVIDADES = {
    1:  {"id": 1,  "nombre": "Trabajar",         "nivel": 0, "pro": False, "coste": 0,    "tiempo": 8, "sector": None}, 
    #Nivel 1
    2:  {"id": 2,  "nombre": "Comer/Dormir",     "nivel": 1, "pro": False, "coste": 2000, "tiempo": 10,"sector": 9},
    3:  {"id": 3,  "nombre": "Salud/Higiene",    "nivel": 1, "pro": False, "coste": 100,  "tiempo": 1, "sector": 7},
    4:  {"id": 4,  "nombre": "Crianza Hijos",    "nivel": 3, "pro": False, "coste": 500, "tiempo": 3, "sector": 7},
    #Nivel 2
    5:  {"id": 5,  "nombre": "Casa/Refugio",     "nivel": 2, "pro": False, "coste": 1500, "tiempo": 0, "sector": 3},
    6:  {"id": 6,  "nombre": "Vestido/Ropa",     "nivel": 2, "pro": False, "coste": 300,  "tiempo": 0, "sector": 5},
    7:  {"id": 7,  "nombre": "Gestión Hogar",    "nivel": 2, "pro": False, "coste": 100,  "tiempo": 2, "sector": 9},
    8:  {"id": 8,  "nombre": "Estudios Básicos", "nivel": 2, "pro": False, "coste": 200,  "tiempo": 5, "sector": 3},
   #Nivel 3
    9:  {"id": 9,  "nombre": "Familia",          "nivel": 3, "pro": False, "coste": 800, "tiempo": 2, "sector": 9},
    10: {"id": 10, "nombre": "Pareja",           "nivel": 3, "pro": False, "coste": 1200, "tiempo": 2, "sector": 9},
    11: {"id": 11, "nombre": "Amigos",           "nivel": 3, "pro": False, "coste": 300,  "tiempo": 2, "sector": 9},
    12: {"id": 12, "nombre": "Sexo",             "nivel": 3, "pro": True,  "coste": 500,  "tiempo": 1, "sector": 9},
    13: {"id": 13, "nombre": "Redes Sociales",   "nivel": 3, "pro": True,  "coste": 100,  "tiempo": 2, "sector": 10},
    14: {"id": 14, "nombre": "Comunidad/ONG",    "nivel": 3, "pro": True,  "coste": 200,  "tiempo": 2, "sector": 9},
    #Nivel 4
    15: {"id": 15, "nombre": "Coche/Transp.",    "nivel": 4, "pro": False, "coste": 2500, "tiempo": 1, "sector": 6},
    16: {"id": 16, "nombre": "Moda/Imagen",      "nivel": 4, "pro": True,  "coste": 1500, "tiempo": 1, "sector": 5},
    17: {"id": 17, "nombre": "Formación Sup.",   "nivel": 4, "pro": False, "coste": 1000, "tiempo": 4, "sector": 3},
    18: {"id": 18, "nombre": "Deporte/Fit",      "nivel": 4, "pro": True,  "coste": 800,  "tiempo": 2, "sector": 9},
    19: {"id": 19, "nombre": "Negocios/Poder",   "nivel": 4, "pro": True,  "coste": 2000, "tiempo": 4, "sector": 4},
    20: {"id": 20, "nombre": "Tecnología",       "nivel": 4, "pro": True,  "coste": 500,  "tiempo": 1, "sector": 5},
    #nivel 5
    21: {"id": 21, "nombre": "Arte/Cultura",     "nivel": 5, "pro": True,  "coste": 1200, "tiempo": 3, "sector": 2},
    22: {"id": 22, "nombre": "Ciencia/Saber",    "nivel": 5, "pro": True,  "coste": 500,  "tiempo": 3, "sector": 6},
    23: {"id": 23, "nombre": "Leer/Escribir",    "nivel": 5, "pro": True,  "coste": 300,  "tiempo": 3, "sector": 2},
    24: {"id": 24, "nombre": "Espiritualidad",   "nivel": 5, "pro": True,  "coste": 200,  "tiempo": 2, "sector": 9},
    25: {"id": 25, "nombre": "Inventar/Crear",   "nivel": 5, "pro": True,  "coste": 600,  "tiempo": 3, "sector": 6},
    26: {"id": 26, "nombre": "Viajar",           "nivel": 5, "pro": True,  "coste": 2000, "tiempo": 2, "sector": 6},
    27: {"id": 27, "nombre": "Activismo Pol.",   "nivel": 5, "pro": True,  "coste": 200,  "tiempo": 3, "sector": 8},
    #Nivel oscuro
    28: {"id": 28, "nombre": "Vicios/Drogas",    "nivel": -1,"pro": False, "coste": 2000, "tiempo": 4, "sector": 9}, 
    29: {"id": 29, "nombre": "Juego/Azar",       "nivel": -1,"pro": True,  "coste": 1500, "tiempo": 3, "sector": 9},
}

LISTA_ARQUETIPOS = ['amigo', 'cuidador', 'explorador', 'heroe', 'amante', 
                    'inocente', 'rebelde', 'sabio', 'gobernante', 'creador', 'bufon', 'mago']

LISTA_CARACTERES = ['amorfo', 'apasionado', 'apatico', 'colerico',
                    'flematico', 'sanguineo', 'sentimental']

PREFERENCIAS_ARQ = {
    'amigo': [11, 13, 20], 
    'cuidador': [14, 9, 4, 7], 
    'explorador': [26, 15],
    'heroe': [18, 1], 
    'amante': [12, 10, 16],    
    'inocente': [24, 9, 3],
    'rebelde': [27, 28, 29], 
    'sabio': [22, 23, 17], 
    'gobernante': [19, 27],
    'creador': [21, 25, 16], 
    'bufon': [13, 28, 29], 
    'mago': [25, 20, 22]
}
PREFERENCIAS = {
    'amorfo': [2, 13, 28], 
    'apasionado': [21, 27, 12, 29], 
    'apatico': [2, 5, 24],
    'colerico': [19, 18, 27, 15], 
    'flematico': [22, 23, 7],
    'sanguineo': [11, 10, 26, 14], 
    'sentimental': [9, 24, 4, 14]   
}

# ==========================================
# 3. FUNCIONES AUXILIARES
# ==========================================
def calcular_irpf(ingreso_anual):
    impuesto_total = 0
    ultimo_limite = 0
    for limite, tipo in Config.TRAMOS_IRPF_BASE:
        if ingreso_anual > limite:
            tramo = limite - ultimo_limite
            impuesto_total += tramo * tipo
            ultimo_limite = limite
        else:
            tramo = ingreso_anual - ultimo_limite
            impuesto_total += tramo * tipo
            break
    if ingreso_anual > Config.TRAMOS_IRPF_BASE[-1][0]:
        impuesto_total += (ingreso_anual - Config.TRAMOS_IRPF_BASE[-1][0]) * Config.TRAMOS_IRPF_BASE[-1][1]
    return impuesto_total * Config.FACTOR_IRPF

def ajustar_y_pintar(datos, titulo="Ajuste de distribuciones", bins=50, usar_log_y=True, usar_percentiles=True):
    datos = np.asarray(datos)
    datos = datos[np.isfinite(datos)]
    datos = datos[datos > 0]

    if len(datos) == 0:
        print("No hay datos positivos válidos.")
        return

    resultados = {}

    def registra_resultado(nombre, dist_obj, params, datos_fit):
        if dist_obj is None or params is None: return
        logpdf = dist_obj.logpdf(datos_fit)
        logpdf = logpdf[np.isfinite(logpdf)]
        if len(logpdf) == 0: return
        logL = np.sum(logpdf)
        n = len(datos_fit); k = len(params)
        aic = 2 * k - 2 * logL; bic = k * np.log(n) - 2 * logL
        resultados[nombre] = {"dist": dist_obj, "params": params, "logL": logL, "AIC": aic, "BIC": bic}

    try:
        params_gamma = stats.gamma.fit(datos)
        registra_resultado("Gamma", stats.gamma(*params_gamma), params_gamma, datos)
    except: pass

    try:
        params_lognorm = stats.lognorm.fit(datos, floc=0)
        registra_resultado("Lognormal", stats.lognorm(*params_lognorm), params_lognorm, datos)
    except: pass

    try:
        params_genhyp = stats.genhyperbolic.fit(datos)
        registra_resultado("GenHyperbolic", stats.genhyperbolic(*params_genhyp), params_genhyp, datos)
    except: pass

    try:
        params_pareto = stats.genpareto.fit(datos)
        registra_resultado("Pareto", stats.genpareto(*params_pareto), params_pareto, datos)
    except: pass

    if not resultados: return
    mejor_aic = min(resultados, key=lambda k: resultados[k]["AIC"])
    
    if usar_percentiles:
        x_min = np.percentile(datos, 0.1); x_max = np.percentile(datos, 99.9)
    else:
        x_min, x_max = datos.min(), datos.max()

    x_min_plot = max(x_min, 1e-9)
    x = np.linspace(x_min_plot, x_max, 2000)

    plt.figure(figsize=(7, 5))
    plt.hist(datos, bins=bins, range=(x_min, x_max), density=True, alpha=0.4, edgecolor='none', label="Histograma")

    if "Gamma" in resultados: plt.plot(x, resultados["Gamma"]["dist"].pdf(x), '--', label="Gamma")
    if "Lognormal" in resultados: plt.plot(x, resultados["Lognormal"]["dist"].pdf(x), '-.', label="Lognormal")
    if "GenHyperbolic" in resultados: plt.plot(x, resultados["GenHyperbolic"]["dist"].pdf(x), '-', label="GenHyperbolic")
    if "Pareto" in resultados: plt.plot(x, resultados["Pareto"]["dist"].pdf(x), ':', label="Pareto")

    if usar_log_y: plt.yscale("log")
    plt.xlabel("Valor"); plt.ylabel("Densidad" + (" (log)" if usar_log_y else ""))
    plt.title(f"{titulo}  –  Mejor (AIC): {mejor_aic}")
    plt.legend(); plt.grid(True, which="both", ls=":"); plt.tight_layout(); plt.show()

    # Desigualdad
    x_sorted = np.sort(datos); n = len(x_sorted)
    gini = (np.sum((2*np.arange(1, n+1) - n - 1) * x_sorted)) / (n * np.sum(x_sorted))
    mean_x = np.mean(datos)
    theil_T = np.mean((datos / mean_x) * np.log(datos / mean_x))
    theil_L = np.mean(np.log(mean_x / datos))
    print(f"\n--- DESIGUALDAD ({titulo}) ---\nGini: {gini:.5f} | Theil T: {theil_T:.5f} | Theil L: {theil_L:.5f}")
    return resultados

def plot_bar_from_dict(data_dict, title, x_label, y_label, horizontal=False):
    if not data_dict: return
    plt.figure(figsize=(10, 6))
    keys = list(data_dict.keys()); values = list(data_dict.values())
    if horizontal:
        plt.barh(keys, values, color='skyblue'); plt.xlabel(y_label); plt.ylabel(x_label)
    else:
        plt.bar(keys, values, color='skyblue'); plt.xlabel(x_label); plt.ylabel(y_label)
        plt.xticks(rotation=45, ha='right')
    plt.title(title); plt.tight_layout(); plt.show()

# --- ELIMINADA FUNCION LANZAR_HIJO ---

# ==========================================
# 4. CLASES DEL SISTEMA (ACTUALIZADAS CON CONFIG)
# ==========================================
class Actividad:
    def __init__(self, id_act_num, nombre, coste_anual, valor_venta):
        self.id = id_act_num; self.nombre = nombre
        self.coste_anual = coste_anual; self.valor_venta = valor_venta
        self.nivel = ACTIVIDADES[id_act_num]["nivel"]
        self.tiempo = ACTIVIDADES[id_act_num]["tiempo"]

class Estado:
    def __init__(self, capital_inicial):
        self.tesoro = capital_inicial
        self.empleados_publicos = []
        self.deuda_publica = 0
        self.reset_contadores()

    def reset_contadores(self):
        self.recaudacion_irpf = 0; self.recaudacion_is = 0 
        self.gasto_salarios_pub = 0; self.gasto_rbu = 0; self.gasto_pensiones = 0
        self.gasto_compras_empresas = 0 

    def recaudar_empresas(self, empresas, stats):
        for emp in empresas:
            beneficio = emp.ingresos_anuales - emp.gastos_anuales
            emp.resultado_anual = beneficio
            if beneficio > 0:
                impuesto = beneficio * (Config.IAE_BASE / 100.0)
                if emp.capital > impuesto:
                    emp.capital -= impuesto; self.tesoro += impuesto
                    self.recaudacion_is += impuesto; stats['impuEmprS'] += impuesto 
            emp.reset_fiscal()

    def gestionar_empleo_publico(self, poblacion):
        pob_activa = [p for p in poblacion if 18 <= p.edad < Config.EDAD_JUBILACION and p.vivo]
        if not pob_activa: return
        self.empleados_publicos = [p for p in self.empleados_publicos if p.vivo and p.edad < Config.EDAD_JUBILACION]
        desempleados = [p for p in pob_activa if p.empleo is None and p not in self.empleados_publicos]
        
        tasa_paro = len(desempleados) / len(pob_activa) if pob_activa else 0
        objetivo_base = int(len(pob_activa) * Config.OBJETIVO_EMPLEO_PUB) 
        if tasa_paro > 0.15:
            excedente = int(len(pob_activa) * (tasa_paro - 0.10))
            objetivo_base += excedente
            if self.tesoro < 0: objetivo_base = int(objetivo_base * 0.9)

        huecos = objetivo_base - len(self.empleados_publicos)
        if huecos > 0 and desempleados:
            candidatos = sorted(desempleados, key=lambda x: x.nivel_educativo, reverse=True)
            for p in candidatos[:huecos]:
                self.empleados_publicos.append(p); p.empleo = "ESTADO"
                if not any(a.id == 1 for a in p.actividades):
                    p.actividades.append(Actividad(1, "Trabajar", 0, 0))
                base = Config.SALARIO_MINIMO * Config.PLUS_SALARIAL_PUB 
                p.salario_actual = (base + (Config.SALARIO_MINIMO * p.nivel_educativo * 0.5))
                p.puesto_desc = "Funcionario"

    def pagar_nominas_y_social(self, poblacion, stats):
        for p in self.empleados_publicos:
            p.antiguedad_laboral += 1
            coste = p.salario_actual * Config.FACTOR_ECONOMICO 
            irpf = calcular_irpf(coste); neto = coste - irpf
            self.tesoro -= neto; p.dinero += neto 
            p.impuestos_pagados_ano = irpf; self.gasto_salarios_pub += coste; self.recaudacion_irpf += irpf
            stats['pagoxTrabOrgaS'] += neto; stats['impuPhS'] += irpf

        base_pension = Config.SALARIO_MINIMO * 0.7
        for p in poblacion:
            if not p.vivo: continue
            if Config.RBU_ACTIVA == 1 and Config.RBU_MONTO_ACTUAL > 0:
                self.tesoro -= Config.RBU_MONTO_ACTUAL; p.dinero += Config.RBU_MONTO_ACTUAL
                self.gasto_rbu += Config.RBU_MONTO_ACTUAL; stats['ingrxRBUS'] += Config.RBU_MONTO_ACTUAL

            if p.edad >= Config.EDAD_JUBILACION:
                pension = base_pension + (p.anos_cotizados * 15)
                irpf = calcular_irpf(pension); neto = pension - irpf
                self.tesoro -= neto; p.dinero += neto
                self.gasto_pensiones += pension; self.recaudacion_irpf += irpf
                stats['otroServOrgaS'] += neto; stats['impuPhS'] += irpf

        if self.tesoro < 0: self.deuda_publica += abs(self.tesoro)

    def ejecutar_compra_publica(self, empresas, stats):
        if not empresas: return
        presupuesto_compras = self.gasto_salarios_pub * 0.30 
        if presupuesto_compras == 0: presupuesto_compras = 1000 * len(empresas)
        monto_individual = presupuesto_compras / len(empresas)
        for e in empresas:
            e.ingresar_dinero(monto_individual) 
            self.tesoro -= monto_individual     
            stats['compOrgaS'] += monto_individual; stats['comOrgaS'] += monto_individual
        self.gasto_compras_empresas += presupuesto_compras

class Empresa:
    def __init__(self, id_empresa, nombre, id_sector_num, capital_inicial):
        self.id = id_empresa; self.nombre = nombre
        self.id_sector_num = id_sector_num
        self.sector_str = Config.MAPA_SECTORES.get(id_sector_num, "servicios")
        self.capital = capital_inicial
        self.empleados = []
        self.slots_empleo = 50 
        self.ingresos_anuales = 0; self.gastos_anuales = 0; self.resultado_anual = 0 
        
    def ingresar_dinero(self, monto):
        self.capital += monto * Config.FACTOR_ECONOMICO
        self.ingresos_anuales += monto * Config.FACTOR_ECONOMICO

    def recibir_inversion(self, monto):
        self.capital += monto 

    def reset_fiscal(self):
        self.ingresos_anuales = 0; self.gastos_anuales = 0

    def ajustar_capacidad(self):
        beneficio = self.ingresos_anuales - self.gastos_anuales
        
        # ### CORRECCIÓN: Lógica de expansión más agresiva
        # Si hay beneficio O si tienes mucho capital parado, contrata más.
        if beneficio > 0 or self.capital > (self.slots_empleo * 20000): 
            nuevo_cupo = int(self.slots_empleo * 1.1) + 1 # Crece un 10% + 1 minimo
            self.slots_empleo = min(nuevo_cupo, 500) # Tope para no explotar memoria
        else:
            # Solo reduce si está perdiendo mucho dinero Y tiene poco capital
            if self.capital < 10000 and self.slots_empleo > 5:
                 self.slots_empleo -= 1
    
    def contratar(self, agente, puesto_info):
        if len(self.empleados) < self.slots_empleo:
            self.empleados.append(agente)
            agente.empleo = self
            
            if not any(a.id == 1 for a in agente.actividades):
                agente.actividades.append(Actividad(1, "Trabajar", 0, 0))
            
            # Calculo salario base CSV
            salario_max_dataset = float(puesto_info['salarioMaxi'])
            if salario_max_dataset == 0: salario_max_dataset = 20000 # Parche para datos a 0

            factor_salarial = random.uniform(Config.SALARIO_INI_MIN, Config.SALARIO_INI_MAX)
            salario_calc = salario_max_dataset * factor_salarial * Config.FACTOR_ECONOMICO
            
            # ### CORRECCIÓN: SUELO SALARIAL
            # Nadie cobra menos del SMI configurado, garantiza poder adquisitivo
            agente.salario_actual = max(salario_calc, Config.SALARIO_MINIMO)
            
            agente.salario_max_puesto = salario_max_dataset
            agente.puesto_desc = str(puesto_info['descripcion'])
            agente.antiguedad_laboral = 0
            return True
        return False
    
    def pagar_salarios(self, estado, stats):
        despidos = []
        for emp in self.empleados:
            emp.anos_cotizados += 1; emp.antiguedad_laboral += 1
            
            # Variación salarial (subidas IPC)
            variacion = random.gauss(Config.VAR_SALARIAL_MEDIA, Config.VAR_SALARIAL_DEV) 
            emp.salario_actual *= variacion
            
            # Asegurar que incluso con bajadas, no cae por debajo del minimo
            if emp.salario_actual < Config.SALARIO_MINIMO: emp.salario_actual = Config.SALARIO_MINIMO

            coste = emp.salario_actual
            
            # La empresa paga si tiene capital
            if self.capital > coste:
                irpf = calcular_irpf(coste)
                neto = coste - irpf
                emp.dinero += neto
                emp.impuestos_pagados_ano = irpf
                
                self.capital -= coste
                self.gastos_anuales += coste
                
                estado.tesoro += irpf
                estado.recaudacion_irpf += irpf
                
                stats['pagoxTrabEmprS'] += neto
                stats['impuPhS'] += irpf
            else:
                despidos.append(emp)
        
        for emp in despidos:
            self.empleados.remove(emp)
            emp.empleo = None
            emp.salario_actual = 0
            emp.actividades = [a for a in emp.actividades if a.id != 1]
            emp.puesto_desc = "Despedido"
            emp.log(0, "Despedido por quiebra")
    
class MercadoLaboral:

    def __init__(self, df_puestos):
        self.empresas = []
        self.df_puestos = df_puestos

    def registrar_empresa(self, empresa): 
        self.empresas.append(empresa)

    def buscar_empleo(self, agente):
        if agente.empleo is not None: return 
        if not (18 <= agente.edad < Config.EDAD_JUBILACION): return 
        
        # Filtro de edad para alta formación (opcional, lo mantengo)
        if agente.formacion == "Superior" and agente.edad < 22: return
        
        # 1. INTENTO PRINCIPAL: BUSCAR EN SU SECTOR
        sector_agente = agente.sector_formacion
        candidatas = [e for e in self.empresas if e.sector_str == sector_agente and len(e.empleados) < e.slots_empleo]
        
        # 2. ### CORRECCIÓN: FALLBACK (PLAN B)
        # Si no hay hueco en su sector, busca EN CUALQUIER EMPRESA con huecos
        if not candidatas:
            candidatas = [e for e in self.empresas if len(e.empleados) < e.slots_empleo]

        if not candidatas: return # No hay huecos en todo el país (Crisis total)

        # Elegir empresa
        empresa_elegida = random.choice(candidatas)
        
        # Buscar puesto: Intentar casar con el sector de la empresa
        puestos_posibles = self.df_puestos[self.df_puestos['sector'] == empresa_elegida.sector_str]
        
        # Si la empresa tiene un sector raro sin puestos en el CSV, coger cualquiera del CSV
        if puestos_posibles.empty:
            puestos_posibles = self.df_puestos
            
        puesto_asignado = puestos_posibles.sample(n=1).iloc[0]
        empresa_elegida.contratar(agente, puesto_asignado)

class ph: 
    def __init__(self, id_persona, nombre, edad, sexo, madre=None, padre=None, dinero_inicial=0):
        self.id = id_persona; self.nombre = nombre; self.edad = edad; self.sexo = sexo
        self.vivo = True; self.dinero = dinero_inicial
        self.anos_cotizados = 0; self.impuestos_pagados_ano = 0
        self.actividades = []; self.hijos = []; self.causa_muerte = "" 
        self.arquetipo = random.choice(LISTA_ARQUETIPOS); self.caracter = random.choice(LISTA_CARACTERES)
        
        self.formacion = random.choice(["Basica", "Media", "Superior"])
        self.nivel_educativo = 0.3 if self.formacion=="Basica" else 0.6 if self.formacion=="Media" else 1.0
        sector_id = random.randint(0, 9); self.sector_formacion = Config.MAPA_SECTORES[sector_id]
        
        self.edu_padres = 0.0
        if madre and padre:
            self.genoma = madre.genoma; self.edu_padres = (madre.nivel_educativo + padre.nivel_educativo) / 2
        else:
            self.genoma = {"salud_base": random.uniform(0.7, 1.0)}; self.edu_padres = random.uniform(0, 0.5) 
        self.salud = self.genoma["salud_base"]
        self.empleo = None; self.salario_actual = 0; self.salario_max_puesto = 0
        self.puesto_desc = "Sin empleo"; self.antiguedad_laboral = 0
        self.pareja = None; self.intencionalidad = "SUPERVIVENCIA" 
        self.log_vida = []; self.pericia = {}
        self.log(0, "Nacimiento registrado. Perfil inicial creado.")

    def log(self, anio, evento): self.log_vida.append(f"A{anio}: {evento}")
    
    @property
    def palp(self):
        valor_activos = sum(a.valor_venta for a in self.actividades) if self.actividades else 0
        return self.dinero + valor_activos

    def asignar_actividades_basicas(self):
        ids_basicos = [2, 3, 5, 6, 7, 8]
        for id_act in ids_basicos:
            if not any(a.id == id_act for a in self.actividades):
                datos = ACTIVIDADES[id_act]
                self.actividades.append(Actividad(datos["id"], datos["nombre"], datos["coste"], 0))

    def asignar_actividades_afinidad(self):
        if self.edad < 18: return 
        gustos = PREFERENCIAS_ARQ.get(self.arquetipo, []) + PREFERENCIAS.get(self.caracter, [])
        gustos = list(set(gustos)); contador = 0
        for id_act in gustos:
            if contador >= 2: break
            if id_act in ACTIVIDADES:
                datos = ACTIVIDADES[id_act]
                if datos["nivel"] <= 3 and not any(a.nombre == datos["nombre"] for a in self.actividades):
                    precio = datos["coste"] * 2
                    if self.dinero > precio:
                        self.dinero -= precio
                        self.actividades.append(Actividad(datos["id"], datos["nombre"], datos["coste"], precio * 0.8))
                        contador += 1

    def determinar_intencionalidad(self):
        if not self.actividades: self.intencionalidad = "FISIOLOGICAS"; return
        max_nivel = max(a.nivel for a in self.actividades)
        if max_nivel == 2: self.intencionalidad = "SEGURIDAD"
        elif max_nivel == 3: self.intencionalidad = "SOCIAL"
        elif max_nivel == 4: self.intencionalidad = "ESTIMA"
        elif max_nivel == 5: self.intencionalidad = "AUTORREALIZACION"
        else: self.intencionalidad = "NO ASIGNADO"

    def revisar_cartera_actividades(self, stats=None):
        if self.edad < 18:
            ids_necesarios = [2, 3, 5, 6, 7, 8]
            for id_act in ids_necesarios:
                if not any(a.id == id_act for a in self.actividades):
                     d = ACTIVIDADES[id_act]
                     self.actividades.append(Actividad(d["id"], d["nombre"], d["coste"], 0))
            self.actividades = [a for a in self.actividades if a.id in ids_necesarios or a.id == 1]
            return

        ids_mandatorios = [2, 3, 5, 6, 7] 
        for id_act in ids_mandatorios:
            if not any(a.id == id_act for a in self.actividades):
                 d = ACTIVIDADES[id_act]
                 self.actividades.append(Actividad(d["id"], d["nombre"], d["coste"], 0))

        horas_ocupadas = sum(a.tiempo for a in self.actividades)
        horas_libres = 24 - horas_ocupadas
        ingresos_anuales = (self.salario_actual * 12) + (Config.RBU_MONTO_ACTUAL if Config.RBU_ACTIVA else 0)
        gastos_fijos = sum(a.coste_anual for a in self.actividades)
        superavit = ingresos_anuales - gastos_fijos
        
        # ... dentro de revisar_cartera_actividades ...
        
        # Si hay déficit grave y poco dinero
        if superavit < -2000 and self.dinero < 1000:
            candidatas_borrar = [a for a in self.actividades if a.nivel > 2] # Protegemos nivel 1 y 2
            if candidatas_borrar:
                # Priorizamos borrar las de mayor nivel primero (lujos)
                candidatas_borrar.sort(key=lambda x: x.nivel, reverse=True)
                elim = candidatas_borrar[0]
                self.actividades.remove(elim)
                
                # 2º) MATIZ: "Liquidación" en vez de venta pura.
                ingreso_venta = elim.valor_venta * 0.5
                self.dinero += ingreso_venta
                
                # Cambio de texto en el LOG
                accion = "Liquidada" if elim.nivel >= 4 else "Abandonada"
                self.log(0, f"{accion} actividad '{elim.nombre}' por insostenibilidad económica.")
                return

        if horas_libres >= 2 and self.dinero > 500: 
            gustos = PREFERENCIAS_ARQ.get(self.arquetipo, []) + PREFERENCIAS.get(self.caracter, [])
            candidatos_ids = list(set(gustos)); random.shuffle(candidatos_ids) 
            for id_cand in candidatos_ids:
                if id_cand not in ACTIVIDADES: continue
                if any(a.id == id_cand for a in self.actividades): continue 
                info_act = ACTIVIDADES[id_cand]; nivel = info_act['nivel']
                coste_entrada = info_act['coste'] * 3 
                if nivel == 5: coste_entrada = info_act['coste'] * 5 
                if nivel == -1: coste_entrada = info_act['coste'] 
                if info_act['tiempo'] > horas_libres: continue

                puede_comprar = False
            
                if nivel == 3: 
                    if self.dinero > (coste_entrada * 1.5): puede_comprar = True
                elif nivel == 4: 
                    if self.dinero > (coste_entrada * 3): puede_comprar = True
                elif nivel == 5: 
                    if self.dinero > (coste_entrada * 5): puede_comprar = True
                elif nivel == -1:
                    perfil_riesgo = self.arquetipo in ['rebelde', 'bufon'] or self.caracter in ['amorfo', 'apasionado']
                    desesperacion = (self.empleo is None and self.edad > 30)
                    chance = Config.RIESGO_REBELDE if perfil_riesgo else Config.RIESGO_NORMAL
                    if desesperacion: chance += Config.FACTOR_DESESPERACION
                    if random.random() < chance and self.dinero > coste_entrada: puede_comprar = True

                if puede_comprar:
                    self.dinero -= coste_entrada
                    if stats:
                        stats['comprphS'] += coste_entrada; stats['compPhs'] += coste_entrada
                    nueva_act = Actividad(info_act['id'], info_act['nombre'], info_act['coste'], coste_entrada*0.7)
                    self.actividades.append(nueva_act); self.log(0, f"Adquirida actividad: {info_act['nombre']} (Nivel {nivel})")
                    break 

    def ejecutar_actividades_pro(self):
        ingresos_extra = 0
        for act in self.actividades:
            info_base = ACTIVIDADES.get(act.id)
            if info_base and info_base["pro"]:
                rendimiento_base = act.coste_anual * random.uniform(0.5, 2.5) 
                bonus_edu = self.nivel_educativo * 1.5 
                pelotazo = 1.0
                if random.random() < Config.PROB_PELOTAZO: 
                    pelotazo = 5.0; self.log(0, f"¡Pelotazo con {act.nombre}! Ingresos multiplicados.")
                ingreso_neto = (rendimiento_base * bonus_edu * pelotazo) * Config.FACTOR_ECONOMICO
                if ingreso_neto > 0: ingresos_extra += ingreso_neto

        if ingresos_extra > 0:
            neto = ingresos_extra * 0.8; self.dinero += neto
            self.impuestos_pagados_ano += (ingresos_extra * 0.2)
            return ingresos_extra 
        return 0

    def vivir_y_consumir(self, engine, pob_map, stats):
        if not self.vivo: return
        
        hijos_en_casa = []
        for hid in self.hijos:
            h = pob_map.get(hid)
            if h and h.vivo and h.edad < 18: hijos_en_casa.append(h)
        
        miembros_hogar = 1 
        if self.pareja and self.pareja.vivo: miembros_hogar += 1
        miembros_hogar += len(hijos_en_casa)
        
        ahorro_familiar = 0
        if miembros_hogar > 1:
            divisor = max(1, 12 - miembros_hogar); ahorro_familiar = 6500 / divisor
            self.dinero += ahorro_familiar; stats['otroPhS_ahorro'] += ahorro_familiar

        for act in self.actividades[:]:
            if act.nombre == "Crianza Hijos":
                if not hijos_en_casa:
                    todos_mayores = True
                    for hid in self.hijos:
                        h = pob_map.get(hid)
                        if h and h.vivo and h.edad < 18: todos_mayores = False; break
                    if todos_mayores: self.actividades.remove(act) 

        self.edad += 1
        ingreso_pro_bruto = self.ejecutar_actividades_pro()
        if ingreso_pro_bruto > 0:
            stats['otroPhS_ahorro'] += (ingreso_pro_bruto * 0.8) 
            stats['impuPhS'] += (ingreso_pro_bruto * 0.2)

        self.revisar_cartera_actividades(stats)
        self.determinar_intencionalidad()

        coste_vida = sum(a.coste_anual for a in self.actividades)
        gasto_extra = 0
        if self.intencionalidad != "SUPERVIVENCIA":
            gasto_extra = (self.dinero - coste_vida) * Config.PROPENSION_CONSUMO
            if gasto_extra < 0: gasto_extra = 0
          
        gasto_total = coste_vida + gasto_extra
        
        # Bucle de emergencia: Si no tengo dinero para pagar el coste de vida, suelto lastre
        while self.dinero < gasto_total and len(self.actividades) > 5: 
            vendibles = [a for a in self.actividades if a.nivel >= 3]
            if not vendibles: break
            
            # Ordenamos por valor de venta para obtener liquidez rápido
            vendibles.sort(key=lambda x: x.valor_venta, reverse=True)
            vender = vendibles[0]
            
            self.dinero += vender.valor_venta
            self.actividades.remove(vender)
            
            # Cambio de texto en el LOG
            term = "Liquidado activo" if vender.nivel >= 4 else "Abandonada actividad"
            self.log(0, f"{term} '{vender.nombre}' para cubrir subsistencia básica.")
            
            # Recalculamos coste tras soltar la actividad
            coste_vida = sum(a.coste_anual for a in self.actividades)
            gasto_total = coste_vida

        self.dinero -= gasto_total
        if gasto_total > 0:
            stats['comprphS'] += gasto_total
            if engine.empresas:
                empresa_dest = random.choice(engine.empresas); empresa_dest.ingresar_dinero(gasto_total)
                stats['compPhs'] += gasto_total 

        if self.dinero > Config.UMBRAL_INVERSION:
            excedente = self.dinero - Config.UMBRAL_INVERSION
            monto_inversion = excedente * 0.20 
            empresas_finanzas = [e for e in engine.empresas if e.sector_str == "finanzas"]
            if empresas_finanzas:
                empresa_destino = random.choice(empresas_finanzas)
                self.dinero -= monto_inversion; empresa_destino.recibir_inversion(monto_inversion)
                stats['otroPhS_inversion'] += monto_inversion; stats['otroEmprS_financiar'] += monto_inversion 
                self.log(0, f"Invierte {monto_inversion:.0f} en {empresa_destino.nombre}")

class HOSSEngine:
    def __init__(self):
        self.poblacion = []
        self.df_puestos = self.cargar_puestos_csv() 
        self.mercado = MercadoLaboral(self.df_puestos)
        self.empresas = []; self.estado = None
        self.anio_actual = 0; self.contador_ids = 0
        self.historial_macro = []; self.historial_gini = []; self.historial_idh = []; self.isp_history = [] 
        self.mat_act = None; self.stats_flujos = {}

    def cargar_puestos_csv(self):
        try:
            df = pd.read_csv(io.StringIO(CSV_PUESTOS_DATA))
            df['descripcion'] = df['descripcion'].fillna("Puesto Generico")
            df['sector'] = df['sector'].str.lower().str.strip()
            print(f"Dataset de Puestos Cargado: {len(df)} registros.")
            return df
        except Exception as e:
            print(f"Error cargando puestos: {e}"); return pd.DataFrame()
    
    def reset_stats_flujos(self):
        self.stats_flujos = {
            'pagoxTrabOrgaS': 0, 'ingrxRBUS': 0, 'pagoxTrabEmprS': 0,
            'comprphS': 0, 'impuPhS': 0, 'otroPhS_ahorro': 0, 'otroPhS_inversion': 0,
            'compPhs': 0, 'comOrgaS': 0, 'impuEmprS': 0, 'otroEmprS_beneficio': 0,
            'otroEmprS_financiar': 0, 'otroServOrgaS': 0, 'compOrgaS': 0
        }

    def inicializar_mundo(self):
        print("--- INICIALIZACIÓN AÑO CERO ---")
        
        # --- CREACIÓN DE MATRIZ LOCAL DIRECTA ---
        #capacidad_max = Config.POB_INICIAL * 10 # Aumentamos margen
        capacidad_max = 200000
        # Matriz de estado (Año, DNI, [Edad, Palp])
        self.mat_pob = np.zeros((Config.SIM_ANOS + 2, capacidad_max, 2), dtype=np.float32)
        # Matriz de actividades (Año, DNI, Slot, [Coste, Dato1, Dato2, Dato3])
        self.mat_act = np.zeros((Config.SIM_ANOS + 2, capacidad_max, 35, 4), dtype=np.float32)
        print("[ENGINE] Matrices unificadas a capacidad_max")
        
        masa_monetaria_total = Config.POB_INICIAL * 20000 
        ratio = Config.RATIO_MM_PRIV_PUB 
        fondos_privados = masa_monetaria_total * (ratio / (ratio+1))
        fondos_publicos = masa_monetaria_total * (1 / (ratio+1))
        self.estado = Estado(fondos_publicos)
        
        num_empresas_ini = max(2, int(Config.POB_INICIAL / 50)) 
        cap_emp = (fondos_privados * 0.6) / num_empresas_ini
        for i in range(num_empresas_ini):
            sec_id = i % 10
            e = Empresa(i, f"Empresa_{i}", sec_id, cap_emp)
            self.empresas.append(e); self.mercado.registrar_empresa(e)
            
        dinero_ph = (fondos_privados * 0.4) / Config.POB_INICIAL
        for i in range(Config.POB_INICIAL):
            self.contador_ids += 1
            p = ph(self.contador_ids, f"Fundador_{i}", random.randint(18,50), random.choice(["M","F"]), dinero_inicial=dinero_ph)
            p.asignar_actividades_basicas(); p.asignar_actividades_afinidad()
            self.poblacion.append(p)


    #borrada def registrar memoria(self)

    def ajustar_tejido_empresarial(self):
        pob_viva = len([p for p in self.poblacion if p.vivo and p.edad >= 18])
        target_empresas = int(pob_viva / 200); target_empresas = max(target_empresas, 5) 
        deficit = target_empresas - len(self.empresas)
        if deficit > 0:
            for _ in range(deficit):
                nuevo_id = len(self.empresas) + 1000
                sec_id = random.randint(0, 9); nombre = f"Empresa_Din_{self.anio_actual}_{sec_id}"
                nueva = Empresa(nuevo_id, nombre, sec_id, 100000)
                self.empresas.append(nueva); self.mercado.registrar_empresa(nueva)

    def ajuste_empresarial_macro(self):
        for emp in self.empresas: emp.ajustar_capacidad() 

    def gestionar_eventos_globales(self):
        Config.FACTOR_ECONOMICO = 1.0
        if self.anio_actual % Config.CICLO_CORTO_FREQ == 0: Config.FACTOR_ECONOMICO = Config.CICLO_CORTO_IMPACTO
        if self.anio_actual % Config.CICLO_LARGO_FREQ == 0 and self.anio_actual > 0: Config.FACTOR_ECONOMICO = Config.CICLO_LARGO_IMPACTO 

    def dinamica_social_y_reproductiva(self, vivos):
        solteros_m = [p for p in vivos if p.pareja is None and p.sexo == 'M' and 18<=p.edad<=60]
        solteros_f = [p for p in vivos if p.pareja is None and p.sexo == 'F' and 18<=p.edad<=60]
        random.shuffle(solteros_m)
        for i in range(min(len(solteros_m), len(solteros_f))):
            if abs(solteros_m[i].edad - solteros_f[i].edad) < Config.BRECHA_EDAD_PAREJA:
                solteros_m[i].pareja = solteros_f[i]; solteros_f[i].pareja = solteros_m[i]
                act_fam = Actividad(9, "Familia", 200, 0)
                solteros_m[i].actividades.append(act_fam); solteros_f[i].actividades.append(act_fam)
        
        mujeres_fertiles = [p for p in vivos if p.sexo == 'F' and 18 <= p.edad <= 45 and p.pareja]
        for madre in mujeres_fertiles:
            if len(madre.hijos) < Config.LIMITE_HIJOS: 
                prob = Config.FERTILIDAD_BAJA if len(madre.hijos) < 3 else Config.FERTILIDAD_ALTA
                if madre.intencionalidad == "SUPERVIVENCIA": prob = Config.FERTILIDAD_POBREZA
                if Config.FACTOR_ECONOMICO < 1.0: prob *= 0.5
                if random.random() < prob:
                    padre = madre.pareja
                    if padre and padre.vivo:
                        self.nacimiento(madre, padre)
                        if len(madre.hijos) == 1:
                            act_crianza = Actividad(4, "Crianza Hijos", 800, 0)
                            madre.actividades.append(act_crianza); padre.actividades.append(act_crianza)

    def nacimiento(self, madre, padre):
        self.contador_ids += 1
        bebe = ph(self.contador_ids, "Bebe", 0, random.choice(["M","F"]), madre, padre, 0)
        bebe.asignar_actividades_basicas()
        madre.hijos.append(bebe.id); padre.hijos.append(bebe.id)
        self.poblacion.append(bebe)

    def gestion_demografica_muertes(self, vivos):
        muertos_año = 0
        for p in vivos:
            prob_muerte = 0.001 * (Config.FACTOR_MUERTE_VEJEZ ** (p.edad - 50)) if p.edad > 50 else 0.0005
            if self.anio_actual % 100 == 50: prob_muerte *= 5 
            if p.edad >= 100 or random.random() < prob_muerte:
                p.vivo = False; p.causa_muerte = "Vejez" if p.edad > 65 else "Enfermedad"
                if p.empleo == "ESTADO" and p in self.estado.empleados_publicos: self.estado.empleados_publicos.remove(p)
                elif isinstance(p.empleo, Empresa) and p in p.empleo.empleados: p.empleo.empleados.remove(p)
                muertos_año += 1
        return muertos_año

    def mercado_laboral_y_economico(self, vivos): 
        pob_map = {p.id: p for p in self.poblacion}
        self.estado.gestionar_empleo_publico(vivos)
        self.estado.pagar_nominas_y_social(vivos, self.stats_flujos)
        self.estado.ejecutar_compra_publica(self.empresas, self.stats_flujos)
        for p in vivos: p.vivir_y_consumir(self, pob_map, self.stats_flujos)
        activos = [p for p in vivos if p.empleo is None]
        for p in activos: self.mercado.buscar_empleo(p)
        for emp in self.empresas: emp.pagar_salarios(self.estado, self.stats_flujos)
        self.estado.recaudar_empresas(self.empresas, self.stats_flujos)

    def calcular_metricas(self, vivos):
        poblacion_objetivo = [p for p in vivos if p.edad >= 18]
        if not poblacion_objetivo: return 0,0
        riquezas = sorted([max(0, p.dinero) for p in poblacion_objetivo]); n = len(riquezas)
        if n == 0 or sum(riquezas) == 0: gini = 0
        else:
            riquezas_np = np.array(riquezas, dtype=np.float64); index = np.arange(1, n + 1)
            gini = ((2 * np.sum(index * riquezas_np)) / (n * np.sum(riquezas_np))) - ((n + 1) / n)
        if not vivos: return 0,0
        media_salud = statistics.mean([p.salud for p in vivos])
        media_edu = statistics.mean([p.nivel_educativo for p in vivos])
        media_ing = statistics.mean(riquezas) if riquezas else 1
        ingreso_norm = math.log(max(1, media_ing)) / math.log(100000); ingreso_norm = min(1.0, max(0, ingreso_norm))
        idh = (media_salud * media_edu * ingreso_norm) ** (1/3)
        return round(gini, 3), round(idh, 3)

    def ajuste_homeostatico(self):
        ingrTotEmpr = sum(e.ingresos_anuales for e in self.empresas)
        gastTotEmpr = sum(e.gastos_anuales for e in self.empresas)
        difeEmpr = ingrTotEmpr - gastTotEmpr
        self.stats_flujos['otroEmprS_beneficio'] = max(0, difeEmpr)

        ingrTotOrga = self.estado.recaudacion_irpf + self.estado.recaudacion_is
        gastTotOrga = (self.estado.gasto_salarios_pub + self.estado.gasto_rbu + self.estado.gasto_pensiones + self.estado.gasto_compras_empresas)
        difeOrga = ingrTotOrga - gastTotOrga
        gastTotPh = sum(sum(a.coste_anual for a in p.actividades) for p in self.poblacion if p.vivo)
        isp = round((gastTotPh + gastTotEmpr)/gastTotOrga, 2) if gastTotOrga > 0 else 1.0
        self.isp_history.append(isp)
        
        if difeEmpr < 0: Config.IAE_BASE -= 1.0; Config.FACTOR_IRPF -= 0.02
        if difeOrga < 0: Config.IAE_BASE += 1.5; Config.FACTOR_IRPF += 0.03; Config.RBU_PORC_PIB -= 0.5
        else: Config.IAE_BASE -= 0.5; Config.RBU_PORC_PIB += 0.3
        Config.IAE_BASE = max(10, min(50, Config.IAE_BASE))
        Config.RBU_PORC_PIB = max(5, min(40, Config.RBU_PORC_PIB))
        pib_est = ingrTotOrga * 4
        if len([p for p in self.poblacion if p.vivo]) > 0:
            Config.RBU_MONTO_ACTUAL = (pib_est/len([p for p in self.poblacion if p.vivo])) * (Config.RBU_PORC_PIB/100)
        return isp, difeOrga

    def generar_excel_hoss(self, datos_para_guardar):
            """
            Genera hoss_parametrizado.xlsx detectando las cabeceras automáticamente
            desde el diccionario de datos.
            """
            if not datos_para_guardar:
                print("No hay datos para generar el Excel.")
                return
    
            print("Generando fichero Excel...")
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Datos HOSS"
        
            # 1. Obtenemos las cabeceras dinámicamente del primer registro
            # Esto asegura que el Excel tenga las MISMAS columnas que el CSV y que fila_macro
            primer_registro = datos_para_guardar[0]
            cabeceras = list(primer_registro.keys())
        
            # 2. Escribimos las cabeceras
            ws.append(cabeceras)
        
            # 3. Escribimos los datos
            # Como 'fila' es un diccionario, extraemos solo los valores convertidos a lista
            for fila in datos_para_guardar:
                ws.append(list(fila.values()))
        
            # 4. Guardamos el archivo
            nombre_archivo = "hoss_parametrizado.xlsx"
            wb.save(nombre_archivo)
            print(f"Fichero {nombre_archivo} generado correctamente.")

    
    def ciclo(self):
        self.anio_actual += 1
        print(f"\n--- AÑO {self.anio_actual} ---")
        
        # 1. Ejecutar Lógica del Mundo
        self.reset_stats_flujos()
        self.estado.reset_contadores()
        self.gestionar_eventos_globales()
        self.ajustar_tejido_empresarial(); self.ajuste_empresarial_macro()
        vivos = [p for p in self.poblacion if p.vivo]
        self.dinamica_social_y_reproductiva(vivos)
        vivos = [p for p in self.poblacion if p.vivo]
        n_muertos = self.gestion_demografica_muertes(vivos)
        vivos = [p for p in self.poblacion if p.vivo]
        nacidos = len([p for p in vivos if p.edad == 0])
        self.mercado_laboral_y_economico(vivos)
        isp_val, deficit_est = self.ajuste_homeostatico()
        gini, idh = self.calcular_metricas(vivos)
        self.historial_gini.append(gini); self.historial_idh.append(idh)
        
        # 2. Métricas Macro (Código original tuyo)
        activos_totales = [p for p in vivos if 18 <= p.edad < Config.EDAD_JUBILACION]
        tasa_paro = (len([p for p in activos_totales if p.empleo is None])/len(activos_totales)*100) if activos_totales else 0
        mujeres_fertiles = [p for p in vivos if p.sexo == 'F' and 18 <= p.edad <= 45]
        tasa_hijos = (sum(len(p.hijos) for p in mujeres_fertiles) / len(mujeres_fertiles)) if mujeres_fertiles else 0
        
        pib_calculado = self.stats_flujos['comprphS'] + self.stats_flujos['compOrgaS'] + self.stats_flujos['otroPhS_inversion']
        
        # ... (cálculo de equilibrios macro igual que tenías) ...
        ingresos_ph = self.stats_flujos['pagoxTrabEmprS'] + self.stats_flujos['pagoxTrabOrgaS'] + self.stats_flujos['ingrxRBUS'] + self.stats_flujos['otroServOrgaS']
        gastos_ph = self.stats_flujos['comprphS'] + self.stats_flujos['impuPhS']
        equilibrio_ph = ingresos_ph - gastos_ph 
        ingresos_empr = self.stats_flujos['compPhs'] + self.stats_flujos['comOrgaS']
        gastos_empr = self.stats_flujos['pagoxTrabEmprS'] + self.stats_flujos['impuEmprS']
        equilibrio_empr = ingresos_empr - gastos_empr
        ingresos_orga = self.stats_flujos['impuPhS'] + self.stats_flujos['impuEmprS']
        gastos_orga = self.stats_flujos['pagoxTrabOrgaS'] + self.stats_flujos['ingrxRBUS'] + self.stats_flujos['compOrgaS'] + self.stats_flujos['otroServOrgaS']
        equilibrio_orga = ingresos_orga - gastos_orga

        fila_macro = {
            "Tiempo": self.anio_actual, "Poblacion": len(vivos), "Nacidos": nacidos,
            "Tasa hijos x mujer": round(tasa_hijos, 2), "Muertos": n_muertos, "IDH": idh, "Gini": gini,
            "ISP": isp_val, "Paro": round(tasa_paro, 2), "IAE": Config.IAE_BASE, "RBU": Config.RBU_MONTO_ACTUAL,
            "PIB": int(pib_calculado), "Factor_Econ": Config.FACTOR_ECONOMICO,
            "pagoxTrabOrgaS": int(self.stats_flujos['pagoxTrabOrgaS']), "ingrxRBUS": int(self.stats_flujos['ingrxRBUS']),
            "pagoxTrabEmprS": int(self.stats_flujos['pagoxTrabEmprS']), "comprphS": int(self.stats_flujos['comprphS']),
            "impuPhS": int(self.stats_flujos['impuPhS']), "otroPhS(ahorro)": int(self.stats_flujos['otroPhS_ahorro']),
            "otroPhS(INVERSION)": int(self.stats_flujos['otroPhS_inversion']), "EquilibrioPh": int(equilibrio_ph),
            "compPhs": int(self.stats_flujos['compPhs']), "comOrgaS": int(self.stats_flujos['comOrgaS']),
            "impuEmprS": int(self.stats_flujos['impuEmprS']), "otroEmprS(Beneficio)": int(self.stats_flujos['otroEmprS_beneficio']),
            "otroEmprS(financiar)": int(self.stats_flujos['otroEmprS_financiar']), "EquilibrioEmpr": int(equilibrio_empr),
            "compOrgaS": int(self.stats_flujos['compOrgaS']), "otroServOrgaS": int(self.stats_flujos['otroServOrgaS']),
            "EquilibrioOrga": int(equilibrio_orga)
        }
        self.historial_macro.append(fila_macro)
        # >>> PEGA ESTO AQUÍ (Justo antes del print de RESUMEN) <<<
        idx_anio = self.anio_actual - 1 
        if self.mat_pob is not None and idx_anio < self.mat_pob.shape[0]:
            limit_agentes = self.mat_pob.shape[1]
            reg_pob = 0
            reg_act = 0
            for p in self.poblacion:
                if not p.vivo: continue
                idx_p = p.id - 1
                if 0 <= idx_p < limit_agentes:
                    self.mat_pob[idx_anio, idx_p, 0] = float(p.edad)      
                    self.mat_pob[idx_anio, idx_p, 1] = float(p.palp)      
                    reg_pob += 1
                    for act_obj in p.actividades:
                        act_id = act_obj.id
                        if act_id is not None and 0 <= act_id < 35:
                            self.mat_act[idx_anio, idx_p, act_id, 0] = float(act_obj.coste_anual)
                            reg_act += 1
            # He puesto este mensaje para que confirmes que funciona al verlo en blanco
            print(f"   📝 [GRABANDO] Año {self.anio_actual}: {reg_pob} personas en memoria.")

        # Aquí termina el bloque pegado

        print(f"RESUMEN: Pob {len(vivos)} (+{nacidos}/-{n_muertos}) | Paro {tasa_paro:.1f}% | PIB {int(pib_calculado)}")
    
    def exportar_datos(self):
        if not self.historial_macro: return
        nombre_fichero = "hoss_parametrizado.csv"
        try:
            # 1. Exportar CSV
            df = pd.DataFrame(self.historial_macro)
            df.to_csv(nombre_fichero, sep=';', index=False, decimal=',')
            print(f"\n--- EXPORTACIÓN EXITOSA: {nombre_fichero} ---")
            
            # 2. Exportar Excel (AQUÍ ESTABA EL ERROR)
            # Hay que usar 'self.' para llamar al método de la propia clase
            self.generar_excel_hoss(self.historial_macro)
            
        except Exception as e: 
            print(f"Error al exportar: {e}")
    


# ==========================================
# 5. GUI DE SALIDA DE DATOS
# ==========================================
MENU_ESTRUCTURA = {
    "1. Ph()": [
        "Distribución de Intencionalidad (Maslow)", "Esperanza de Vida Media (Fallecidos)",
        "Estadísticas de Ejecución (Ticks/Objs)", "Listado General Población Viva",
        "Logs Biográficos (Muestra Aleatoria 3 pax)", "Matriz MAT_ACT (Muestra Aleatoria 5 pax)", 
        "Movilidad Social (Hijos con estudios)", "Nacimientos por Año Estimados",
        "Nivel Educativo de la Población", "PALP (Patrimonio) Promedio por Edad",
        "Pirámide Poblacional (Grupos de Edad)", "Ratio Dependencia (Sostenibilidad)",
        "Ratio Hombres / Mujeres", "Relación de Fallecidos y Causas (Forense)",
        "Tasa Fertilidad (Hijos promedio x Mujer)",
    ],
    "2. EMPR": [
        "Detalle Tasa de Paro", "Empresas en Riesgo de Quiebra", "Listado de Desempleados (Perfil)",
        "Listado Empresas Activas y Capital", "Ranking Empresas por Beneficio",
        "Ranking Empresas por Nº Empleados", "Salario Medio del Mercado Actual", "Sectores más Capitalizados",
    ],
    "3. ESTADO/ORGANIZACIÓN": [
        "Carga Social (Pensiones+RBU vs Ingresos)", "Comparativa Fuentes Ingreso (IRPF vs IS)",
        "Situación Tesoro y Deuda", "Evolución ISP ( u.m.Privadas/u.m. Públicas = ISP )", "Evolución Fiscal (Recaudación y Tipos)",
    ],
    "4. SOCIEDAD": [
        "Ajuste funcional: Ingresos y Gastos", "Alerta Social (Estado SUPERVIVENCIA)",
        "Brecha Ricos vs Pobres (Ratio 10/10)", "IDH (Evolución)", "Capacidad de Ahorro (>20k)",
        "Coeficiente de Gini (Evolución)", "Élite Psicológica (AUTORREALIZACION)",
        "Evolución Histórica PIB (Estimado)", "Inventario de Activos (Casas, Coches...)",
        "Riqueza Nacional Neta (Suma PALP)", "Tasa de Soledad (Adultos sin pareja)",
        "RBU: evolución en el tiempo", 
    ]
}

def lanzar_explotacion_datos(sim):
    raiz = tk.Tk(); raiz.geometry("1100x800"); raiz.title(f'HOSS v16.12 - INTELIGENCIA DE DATOS [PADRE]')
    frame_left = Frame(raiz, width=350, bg="#f0f0f0"); frame_left.pack(side="left", fill="y", padx=5, pady=5)
    tk.Label(frame_left, text="MENÚ DE ANÁLISIS", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)
    scroll_y = Scrollbar(frame_left); scroll_y.pack(side="right", fill="y")
    listbox = tk.Listbox(frame_left, font=("Consolas", 10), selectmode=tk.SINGLE, yscrollcommand=scroll_y.set, width=45, height=40)
    listbox.pack(side="left", fill="both", expand=True); scroll_y.config(command=listbox.yview)

    flat_map = [] 
    for categoria, items in MENU_ESTRUCTURA.items():
        listbox.insert(tk.END, f"--- {categoria} ---"); listbox.itemconfig(tk.END, {'bg':'#ddd', 'fg':'black'})
        flat_map.append(None) 
        for item in sorted(items): listbox.insert(tk.END, f"   {item}"); flat_map.append(item)

    frame_right = Frame(raiz, bg="white"); frame_right.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    txt_res = tk.Text(frame_right, font=("Consolas", 10), padx=10, pady=10); txt_res.pack(fill="both", expand=True)

    def calcular_dato(key, sim):
        vivos = [p for p in sim.poblacion if p.vivo]
        muertos = [p for p in sim.poblacion if not p.vivo]
        res = f"RESULTADO: {key}\n" + "="*60 + "\n"

        if "Distribución de Intencionalidad" in key:
            counts = Counter([p.intencionalidad for p in vivos])
            total = len(vivos) if vivos else 1
            for k,v in counts.items(): res += f"{k}: {v} ({v/total*100:.1f}%)\n"
            plot_bar_from_dict(counts, "Distribución niveles Maslow", "Intencionalidad", "Cantidad")
        
        elif "Esperanza de Vida" in key:
            if muertos:
                avg = statistics.mean([p.edad for p in muertos])
                res += f"Media Edad Fallecimiento: {avg:.2f} años\n(Total fallecidos: {len(muertos)})"
            else: res += "Sin fallecidos aún."
        
        elif "Estadísticas de Ejecución" in key:
            ticks = sim.anio_actual * len(sim.poblacion)
            res += f"Año Simulado: {sim.anio_actual}\nObjetos Totales Históricos: {len(sim.poblacion)}\nTicks Procesados (aprox): {ticks}"

        elif "Listado General Población" in key:
            res += f"Total Vivos: {len(vivos)}\n"
            res += f"{'ID':<6} | {'NOMBRE':<15} | {'EDAD':<5} | {'INTENCIONALIDAD'}\n" + "-"*60 + "\n"
            filas = [f"{p.id:<6} | {p.nombre:<15} | {p.edad:<5} | {p.intencionalidad}" for p in vivos]
            res += "\n".join(filas)

        elif "Logs Biográficos" in key:
            sample = random.sample(vivos, min(3, len(vivos)))
            for p in sample: res += f"\n--- {p.nombre} (ID {p.id}) ---\n" + "\n".join(p.log_vida[-10:]) + "\n"

        elif "Matriz MAT_ACT" in key:
            res += "Muestra últimos datos de Auditoría (Estado + Actividades):\n"
            if sim.mat_act is None or sim.mat_pob is None: 
                res += "Error: Matrices no inicializadas."
            else:
                idx_anio = sim.anio_actual - 1
                limit_agentes = sim.mat_pob.shape[1]
                candidatos = [p for p in vivos if (p.id - 1) < limit_agentes]
                if not candidatos:
                    res += "No hay agentes vivos dentro del rango de memoria."
                else:
                    sample = random.sample(candidatos, min(5, len(candidatos)))
                    for p in sample:
                        idx_p = p.id - 1
                        
                        # LEEMOS DE LA MATRIZ DE POBLACIÓN (FOTO FIJA)
                        edad_val = sim.mat_pob[idx_anio, idx_p, 0]
                        palp_val = sim.mat_pob[idx_anio, idx_p, 1]
                        
                        res += f"\nAgente {p.id} ({p.nombre}) | Edad: {edad_val:.0f} | Palp: {palp_val:,.2f}€:\n"
                        
                        # LEEMOS DE LA MATRIZ DE ACTIVIDADES (EVENTOS)
                        found = False
                        for act_id in range(sim.mat_act.shape[2]):
                            # El coste ahora está en la posición 0 de la última dimensión
                            coste = sim.mat_act[idx_anio, idx_p, act_id, 0]
                            if coste > 0: 
                                found = True
                                nombre_act = next((v['nombre'] for k,v in ACTIVIDADES.items() if v['id']==act_id), "?")
                                res += f"  - {nombre_act}: Coste Anual {coste:.1f}\n"
                        
                        if not found: res += "  (Sin gastos registrados este año)\n"

        elif "Movilidad Social" in key:
            res += "Análisis de Movilidad Social Ascendente (Hijo > Padres):\n" + "-"*60 + "\n"
            ascensos = [p for p in vivos if p.nivel_educativo > (p.edu_padres + 0.1)]
            de_basica_a_media = len([p for p in ascensos if p.formacion == "Media" and p.edu_padres < 0.5])
            de_media_a_superior = len([p for p in ascensos if p.formacion == "Superior" and 0.5 <= p.edu_padres < 0.9])
            de_basica_a_superior = len([p for p in ascensos if p.formacion == "Superior" and p.edu_padres < 0.5])
            total_ascensos = len(ascensos)
            tasa = (total_ascensos / len(vivos) * 100) if vivos else 0
            res += f"Total personas con ascenso social: {total_ascensos} ({tasa:.1f}% de la pob. total)\n\n"
            res += f"DESGLOSE DEL ASCENSO:\n"
            res += f"1. Paso de Básica a Media:     {de_basica_a_media}\n"
            res += f"2. Paso de Media a Superior:   {de_media_a_superior}\n"
            res += f"3. Salto de Básica a Superior: {de_basica_a_superior} (Gran Ascenso)\n"

        elif "Nacimientos por Año" in key:
            datos_nac = {d['Tiempo']: d['Nacidos'] for d in sim.historial_macro}
            if not datos_nac: res += "No hay datos históricos aún."
            else:
                total_nac = sum(datos_nac.values())
                promedio = total_nac / len(datos_nac)
                res += f"Histórico Completo ({len(datos_nac)} años):\nTotal: {total_nac}\nPromedio: {promedio:.1f}\n"
                plot_bar_from_dict(datos_nac, "Evolución de Nacimientos por Año", "Año", "Nº Nacimientos")

        elif "Nivel Educativo" in key:
            niveles = Counter([p.formacion for p in vivos])
            for k,v in niveles.items(): res += f"{k}: {v}\n"
            plot_bar_from_dict(niveles, "Nivel Educativo", "Nivel", "Personas")

        elif "PALP (Patrimonio)" in key:
            datos = [(p.edad, p.palp) for p in vivos]; datos.sort(key=lambda x: x[0])
            agrupado = {}
            for edad, palp in datos:
                decada = (edad // 10) * 10
                agrupado.setdefault(decada, []).append(palp)
            grafico_palp = {}
            for d in sorted(agrupado.keys()):
                media = statistics.mean(agrupado[d]); res += f"Grupo {d}-{d+9} años: {media:,.0f} €\n"
                grafico_palp[f"{d}-{d+9}"] = media
            plot_bar_from_dict(grafico_palp, "Patrimonio Medio por Edad", "Rango Edad", "Valor €")

        elif "Pirámide Poblacional" in key:
            bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            edades_h = [p.edad for p in vivos if p.sexo == 'M']; edades_m = [p.edad for p in vivos if p.sexo == 'F']
            hist_h, _ = np.histogram(edades_h, bins); hist_m, _ = np.histogram(edades_m, bins)
            plt.figure(figsize=(10, 6)); plt.hist([edades_h, edades_m], bins=bins, label=['Hombres', 'Mujeres'], color=['blue', 'orange'])
            plt.title("Histograma Pirámide Poblacional"); plt.legend(); plt.show()
            res += f"{'RANGO':<10} {'HOMBRES':<10} {'MUJERES':<10}\n"
            for i in range(len(bins)-1): res += f"{bins[i]}-{bins[i+1]:<4} {hist_h[i]:<10} {hist_m[i]:<10}\n"

        elif "Ratio Dependencia" in key:
            dependientes = len([p for p in vivos if p.edad < 16 or p.edad > 65])
            activos = len([p for p in vivos if 16 <= p.edad <= 65])
            ratio = (dependientes / activos * 100) if activos else 0
            res += f"Ratio de Dependencia: {ratio:.1f}% (Sostenible < 50%)"

        elif "Ratio Hombres / Mujeres" in key:
            h = len([p for p in vivos if p.sexo == 'M']); m = len([p for p in vivos if p.sexo == 'F'])
            res += f"Hombres: {h}\nMujeres: {m}\nRatio H/M: {(h/m if m else 0):.2f}"

        elif "Relación de Fallecidos" in key:
            causas = Counter([p.causa_muerte for p in muertos]); res += "Causas de Muerte Históricas:\n"
            for c, v in causas.items(): res += f"{c}: {v}\n"
            plot_bar_from_dict(causas, "Causas de Muerte", "Causa", "Cantidad")

        elif "Tasa Fertilidad" in key:
            mujeres_fertiles = [p for p in vivos if p.sexo == 'F' and 18 <= p.edad <= 45]
            if not mujeres_fertiles: res += "Sin mujeres en edad fértil."
            else:
                hijos_tot = sum(len(p.hijos) for p in mujeres_fertiles)
                tasa = hijos_tot / len(mujeres_fertiles)
                res += f"Tasa: {tasa:.2f} hijos/mujer"

        elif "Detalle Tasa de Paro" in key:
            activos = [p for p in vivos if 18 <= p.edad < 65]; parados = [p for p in activos if p.empleo is None]
            tasa = (len(parados)/len(activos)*100) if activos else 0; res += f"Tasa Paro: {tasa:.1f}%"

        elif "Empresas en Riesgo" in key:
            en_riesgo = [e for e in sim.empresas if e.capital < 20000]; res += f"Empresas en Riesgo de Quiebra (Capital < 20k):\n"
            for e in en_riesgo: res += f"{e.nombre} (Cap: {e.capital:.0f}€)\n"

        elif "Listado de Desempleados" in key:
            parados = [p for p in vivos if 18 <= p.edad < 65 and p.empleo is None]
            res += "Perfil Desempleados (Muestra 20):\n"
            for p in parados[:20]: res += f"ID {p.id} | Edad {p.edad} | Form: {p.formacion}\n"

        elif "Listado Empresas Activas" in key:
            for e in sim.empresas: res += f"{e.nombre} | Sector: {e.sector_str} | Capital: {e.capital:,.0f}€ | Empleados: {len(e.empleados)}\n"

        elif "Ranking Empresas por Beneficio" in key:
            ranking = sorted(sim.empresas, key=lambda x: x.resultado_anual, reverse=True)
            for i, e in enumerate(ranking, 1):
                res += f"{i}. {e.nombre}: {e.resultado_anual:,.0f}€\n"

        elif "Ranking Empresas por Nº Empleados" in key:
            ranking = sorted(sim.empresas, key=lambda x: len(x.empleados), reverse=True)
            for i, e in enumerate(ranking, 1): res += f"{i}. {e.nombre}: {len(e.empleados)} empleados\n"

        elif "Salario Medio" in key:
            asalariados = [p for p in vivos if p.empleo]
            if asalariados:
                vals = [p.salario_actual for p in asalariados]
                media = statistics.mean(vals); desv = statistics.stdev(vals) if len(vals)>1 else 0
                res += f"Salario Medio Bruto Mensual: {media/12:,.0f}€\nDesviación Típica: {desv:,.0f}€"
            else: res += "No hay asalariados."

        elif "Sectores más Capitalizados" in key:
            sectores = {}
            for e in sim.empresas: sectores[e.sector_str] = sectores.get(e.sector_str, 0) + e.capital
            sorted_sec = sorted(sectores.items(), key=lambda x: x[1], reverse=True)
            for k, v in sorted_sec: res += f"{k.upper()}: {v:,.0f}€\n"
            plot_bar_from_dict(dict(sorted_sec), "Capital por Sector", "Capital €", "Sector", horizontal=True)

        elif "Carga Social" in key:
            gastos = sim.estado.gasto_pensiones + sim.estado.gasto_rbu
            ingresos = sim.estado.recaudacion_irpf + sim.estado.recaudacion_is
            ratio = (gastos/ingresos*100) if ingresos > 0 else 0
            res += f"Ingresos Estado: {ingresos:,.0f}€\nGastos Sociales: {gastos:,.0f}€\nRatio Cobertura: {ratio:.1f}%"

        elif "Comparativa Fuentes Ingreso" in key:
            irpf = sim.estado.recaudacion_irpf; sociedades = sim.estado.recaudacion_is; total = irpf + sociedades
            res += f"IRPF (Trabajo): {irpf:,.0f}€ ({(irpf/total*100 if total else 0):.1f}%)\n"
            res += f"IS (Capital): {sociedades:,.0f}€ ({(sociedades/total*100 if total else 0):.1f}%)\n"

        elif "Situación Tesoro" in key:
            res += f"Tesoro Público: {sim.estado.tesoro:,.0f}€\nDeuda Pública: {sim.estado.deuda_publica:,.0f}€\n"
            res += f"Gasto Público en Empresas (comprOrgaS): {sim.estado.gasto_compras_empresas:,.0f}€\n"

        elif "Evolución ISP" in key:
            res += "Histórico ISP:\n"
            data_isp = {d['Tiempo']: d['ISP'] for d in sim.historial_macro}
            for t, v in data_isp.items(): res += f"Año {t}: ISP {v}\n"
            plot_bar_from_dict(data_isp, "Evolución Histórica ISP", "Año", "ISP")

        elif "Evolución Fiscal" in key:
            res += "Histórico Fiscal (IAE y Recaudación):\n"
            years = []
            rec_ph = []
            rec_empr = []
            
            for d in sim.historial_macro:
                res += f"Año {d['Tiempo']}: IAE {d.get('IAE','?')} | IRPF: {d['impuPhS']} | IS: {d['impuEmprS']}\n"
                years.append(d['Tiempo'])
                rec_ph.append(d['impuPhS'])
                rec_empr.append(d['impuEmprS'])
            
            # GRAFICO COMPARATIVO ESPECIAL
            x = np.arange(len(years))
            width = 0.35
            plt.figure(figsize=(10, 6))
            plt.bar(x - width/2, rec_ph, width, label='IRPF (ph)', color='skyblue')
            plt.bar(x + width/2, rec_empr, width, label='IS (Corporativo)', color='orange')
            plt.xlabel('Año')
            plt.ylabel('Recaudación')
            plt.title('Evolución Fiscal: Recaudación IRPF vs IS')
            plt.xticks(x, years, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

        elif "Ajuste funcional" in key:
            ingresos = [(p.salario_actual*12 + Config.RBU_MONTO_ACTUAL) for p in vivos]
            gastos = [sum(a.coste_anual for a in p.actividades) + p.impuestos_pagados_ano + (p.dinero*Config.PROPENSION_CONSUMO) for p in vivos]
            ajustar_y_pintar(ingresos, "Distribución Ingresos"); ajustar_y_pintar(gastos, "Distribución Gastos")
        
        elif "Alerta Social" in key:
            en_peligro = [p for p in vivos if p.intencionalidad == "SUPERVIVENCIA"]
            res += f"Personas en modo SUPERVIVENCIA: {len(en_peligro)}\n"

        elif "Brecha Ricos vs Pobres" in key:
            ricos = sorted([p.palp for p in vivos], reverse=True)
            if not ricos: res += "Sin población."
            else:
                top_10_n = max(1, int(len(ricos)*0.1))
                wealth_top = sum(ricos[:top_10_n])
                wealth_bot = sum(ricos[-top_10_n:])
                
                res += f"Riqueza Top 10%: {wealth_top:,.0f} €\n"
                res += f"Riqueza Bot 10%: {wealth_bot:,.0f} €\n"
                
                if wealth_bot <= 0:
                    res += "Ratio: N/A (El segmento inferior tiene deuda neta)"
                else:
                    ratio = wealth_top / wealth_bot
                    res += f"Ratio Brecha: {ratio:.2f}"

        elif "IDH (Evolución)" in key:
            gini, idh = sim.calcular_metricas(vivos)
            res += f"IDH Actual: {idh}\n"
            data_idh = {d['Tiempo']: d['IDH'] for d in sim.historial_macro}
            plot_bar_from_dict(data_idh, "Evolución Histórica IDH", "Año", "IDH")

        elif "Capacidad de Ahorro" in key:
            ahorradores = [p for p in vivos if p.dinero > 20000]
            res += f"Personas con >20k líquidos: {len(ahorradores)} ({(len(ahorradores)/len(vivos)*100):.1f}%)"

        elif "Coeficiente de Gini" in key:
            gini, idh = sim.calcular_metricas(vivos); res += f"GINI Actual: {gini}\n"
            data_gini = {d['Tiempo']: d['Gini'] for d in sim.historial_macro}
            plot_bar_from_dict(data_gini, "Evolución Histórica Gini", "Año", "Gini")

        elif "Élite Psicológica" in key:
            elite = [p for p in vivos if p.intencionalidad == "AUTORREALIZACION"]
            res += f"Personas Autorrealizadas: {len(elite)}\n"

        elif "Evolución Histórica PIB" in key:
            data_pib = {d['Tiempo']: d['PIB'] for d in sim.historial_macro}
            for t, v in data_pib.items(): res += f"Año {t}: {v:,.0f} um\n"
            plot_bar_from_dict(data_pib, "Evolución Histórica PIB", "Año", "PIB")

        elif "Inventario de Activos" in key:
            coches = 0; casas = 0
            for p in vivos:
                for a in p.actividades:
                    if "Coche" in a.nombre: coches += 1
                    if "Refugio" in a.nombre or "Casa" in a.nombre: casas += 1
            res += f"Total Coches: {coches}\nTotal Casas: {casas}"

        elif "Riqueza Nacional Neta" in key:
            total = sum(p.palp for p in vivos); res += f"Suma Patrimonio (PALP): {total:,.0f} €"

        elif "Tasa de Soledad" in key:
            solos = [p for p in vivos if p.edad > 30 and p.pareja is None]
            res += f"Adultos (>30) sin pareja: {len(solos)} ({(len(solos)/len(vivos)*100):.1f}%)"
            
        elif "RBU: evolución en el tiempo" in key:
            datos_rbu = {d['Tiempo']: d.get('RBU', 0) for d in sim.historial_macro}
            res += "Evolución RBU anual:\n"
            for t, v in datos_rbu.items():
                res += f"Año {t}: {v:,.2f} um\n"
            plot_bar_from_dict(datos_rbu, "Evolución Histórica de la RBU", "Año", "Cuantía RBU")

        else: res += "Selecciona opción válida."
        return res


    def ejecutar_consulta(event):
        idx = listbox.curselection()
        if not idx: return
        index_int = idx[0]; sel_key = flat_map[index_int]
        if sel_key is None: return 
        resultado_texto = calcular_dato(sel_key, sim)
        txt_res.config(state="normal"); txt_res.delete("1.0", tk.END); txt_res.insert("1.0", resultado_texto); txt_res.config(state="disabled")

    listbox.bind('<<ListboxSelect>>', ejecutar_consulta)
    tk.Button(frame_left, text="CERRAR", command=raiz.destroy, bg="#d32f2f", fg="white", font=("Arial", 10, "bold")).pack(side="bottom", fill="x", pady=10)
    raiz.mainloop()


# ==========================================
# 6. NUEVA GUI DE CONFIGURACIÓN (CON GUARDAR/CARGAR)
# ==========================================
def run_gui_parametrizada():
    root = tk.Tk()
    root.title("HOSS (-5): PANEL DE CONFIGURACIÓN Y ESCENARIOS")
    root.geometry("650x750") 

    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = Canvas(main_frame, bg="#f0f0f0")
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    parametros = {
        "GENERAL": {
            "SIM_ANOS": {"tipo": int, "def": 50, "min": 5, "max": 100, "desc": "Duración simulación (años)"},
            "POB_INICIAL": {"tipo": int, "def": 100, "min": 50, "max": 30000, "desc": "Población inicial (Fundadores)"},
            "ANOS_ESCOLARIZACION": {"tipo": int, "def": 14, "min": 0, "max": 20, "desc": "Años de escolarización obligatoria"},
            "COSTE_VIDA_BASE": {"tipo": float, "def": 6000, "min": 3000, "max": 12000, "desc": "Coste anual supervivencia (Nivel 1 Maslow)"},
        },
        "DEMOGRAFÍA Y POBLACIÓN": {
            "FERTILIDAD_BAJA": {"tipo": float, "def": 0.25, "min": 0.0, "max": 1.0, "desc": "Fertilidad Base (si hijos < 3)"},
            "FERTILIDAD_ALTA": {"tipo": float, "def": 0.15, "min": 0.0, "max": 1.0, "desc": "Fertilidad Base (si hijos >= 3)"},
            "FERTILIDAD_POBREZA": {"tipo": float, "def": 0.20, "min": 0.0, "max": 1.0, "desc": "Fertilidad en 'Supervivencia'"},
            "LIMITE_HIJOS": {"tipo": int, "def": 7, "min": 1, "max": 15, "desc": "Límite hijos por mujer"},
            "BRECHA_EDAD_PAREJA": {"tipo": int, "def": 10, "min": 1, "max": 30, "desc": "Brecha edad pareja (años)"},
            "FACTOR_MUERTE_VEJEZ": {"tipo": float, "def": 1.1, "min": 1.01, "max": 1.5, "desc": "Factor Muerte Vejez (Gompertz)"},
            "ESPERANZA_VIDA": {"tipo": int, "def": 80, "min": 50, "max": 100, "desc": "Esperanza de vida ref."},
        },
        "POLÍTICA ECONÓMICA (ESTADO)": {
            "RBU_ACTIVA": {"tipo": int, "def": 1, "min": 0, "max": 1, "desc": "RBU Activada (1=Sí, 0=No)"},
            "RBU_MONTO_ACTUAL": {"tipo": float, "def": 8800, "min": 0, "max": 20000, "desc": "Cuantía RBU anual (u.m.)"},
            "SALARIO_MINIMO": {"tipo": float, "def": 10800, "min": 8800, "max": 20000, "desc": "Salario Mínimo anual(SMI)"},
            "IAE_BASE": {"tipo": float, "def": 25.0, "min": 5.0, "max": 60.0, "desc": "Impuesto Sociedades Inicial (%)"},
            "OBJETIVO_EMPLEO_PUB": {"tipo": float, "def": 0.15, "min": 0.05, "max": 0.50, "desc": "% Empleo Público Objetivo"},
             "PLUS_SALARIAL_PUB": {"tipo": float, "def": 1.3, "min": 1.0, "max": 2.0, "desc": "Factor Salario Público vs Privado"},
             "INDEXACION": {"tipo": float, "def": 1.0, "min": 0.0, "max": 1.0, "desc": "% Indexación RBU/SMI al IPC/PIB (0=Fijo, 1=Total)"},
             "IMPUESTO_PATRIMONIO": {"tipo": float, "def": 0.0, "min": 0.0, "max": 5.0, "desc": "Impuesto a la Riqueza Acumulada (%)"},
        },
        "MERCADO LABORAL": {
            "SALARIO_INI_MIN": {"tipo": float, "def": 0.51, "min": 0.1, "max": 1.0, "desc": "Oferta Salarial Mín (% del Max)"},
            "VAR_SALARIAL_MEDIA": {"tipo": float, "def": 1.01, "min": 0.90, "max": 1.10, "desc": "Variación Salarial Anual (Media)"},
            "VAR_SALARIAL_DEV": {"tipo": float, "def": 0.05, "min": 0.01, "max": 0.20, "desc": "Variación Salarial Anual (Desv)"},
        },
        "PSICOLOGÍA Y CICLOS": {
            "FACTOR_DESESPERACION": {"tipo": float, "def": 0.10, "min": 0.0, "max": 0.5, "desc": "Factor Riesgo por Desesperación"},
            "CICLO_CORTO_IMPACTO": {"tipo": float, "def": 0.75, "min": 0.1, "max": 1.0, "desc": "Impacto Recesión (Factor Econ)"},
            "CICLO_LARGO_IMPACTO": {"tipo": float, "def": 0.50, "min": 0.1, "max": 1.0, "desc": "Impacto Depresión (Factor Econ)"},
            "PROB_PELOTAZO": {"tipo": float, "def": 0.02, "min": 0.0, "max": 0.10, "desc": "Probabilidad Éxito/Pelotazo"},
        }
    }

    entries = {}

    for categoria, items in parametros.items():
        labelframe = tk.LabelFrame(scrollable_frame, text=categoria, font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#333", padx=10, pady=10)
        labelframe.pack(fill="x", expand=True, padx=10, pady=5)

        row = 0
        for key, info in items.items():
            tk.Label(labelframe, text=info["desc"], bg="#f0f0f0", width=35, anchor="e").grid(row=row, column=0, padx=5, pady=2)
            ent = tk.Entry(labelframe, width=10, justify="center")
            ent.insert(0, str(info["def"]))
            ent.grid(row=row, column=1, padx=5, pady=2)
            tk.Label(labelframe, text=f"[{info['min']} - {info['max']}]", bg="#f0f0f0", fg="#666", font=("Arial", 8)).grid(row=row, column=2, padx=5, sticky="w")
            entries[key] = (ent, info)
            row += 1

    def guardar_configuracion():
        datos_guardar = {}
        for key, (ent, info) in entries.items():
            datos_guardar[key] = ent.get() 
        
        fichero = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos", "*.*")],
            title="Guardar Escenario HOSS"
        )
        if fichero:
            try:
                with open(fichero, 'w') as f:
                    json.dump(datos_guardar, f, indent=4)
                messagebox.showinfo("Éxito", f"Configuración guardada en:\n{fichero}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def cargar_configuracion():
        fichero = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json"), ("Todos", "*.*")],
            title="Cargar Escenario HOSS"
        )
        if fichero:
            try:
                with open(fichero, 'r') as f:
                    datos_cargados = json.load(f)
                
                count = 0
                for key, valor in datos_cargados.items():
                    if key in entries:
                        ent = entries[key][0]
                        ent.delete(0, tk.END)
                        ent.insert(0, str(valor))
                        count += 1
                messagebox.showinfo("Carga Completa", f"Se han actualizado {count} parámetros.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar: {e}")
    
    def cerrar_programa():
        print("Cerrando aplicación...")
        root.destroy()
        sys.exit() 


    def validar_y_lanzar():
        errores = []
        for key, (ent, info) in entries.items():
            val_str = ent.get()
            try:
                if info["tipo"] == int: val = int(val_str)
                else: val = float(val_str)
                
                if val < info["min"] or val > info["max"]:
                    errores.append(f"{key}: Valor {val} fuera de límites [{info['min']}-{info['max']}]")
                else:
                    setattr(Config, key, val)
            except ValueError:
                errores.append(f"{key}: '{val_str}' no es un número válido.")
        
        if errores:
            msg = "Se encontraron errores:\n\n" + "\n".join(errores[:10])
            messagebox.showerror("Error de Validación", msg)
        else:
            root.destroy()

    # -----------------------------------------------------------
    # CONFIGURACIÓN DE LA BOTONERA INFERIOR
    # -----------------------------------------------------------
    btn_frame = Frame(root, bg="#ddd")
    btn_frame.pack(fill="x", side="bottom")

    # --- FILA 1: GESTIÓN DE ARCHIVOS ---
    file_btn_frame = Frame(btn_frame, bg="#ddd")
    file_btn_frame.pack(fill="x", pady=5)
    
    tk.Button(file_btn_frame, text="💾 GUARDAR ESCENARIO", command=guardar_configuracion, 
              bg="#008CBA", fg="white", font=("Arial", 10, "bold"), width=20).pack(side="left", padx=20)
    
    tk.Button(file_btn_frame, text="📂 CARGAR ESCENARIO", command=cargar_configuracion, 
              bg="#008CBA", fg="white", font=("Arial", 10, "bold"), width=20).pack(side="right", padx=20)

    # --- FILA 2: INFORMACIÓN / AYUDA (NUEVO BOTÓN) ---
    # Lo colocamos con 'pack' simple para que quede centrado verticalmente entre las filas
    tk.Button(btn_frame, text="ℹ️ HOSS: Simulación avanzada", command=abrir_ventana_info_hoss, 
              bg="lightblue", fg="black", font=("Arial", 10, "bold"), width=30).pack(pady=5)

    # --- FILA 3: ACCIÓN PRINCIPAL ---
    # Nota: Usamos frames internos o pack con side para asegurar que queden a los lados
    action_btn_frame = Frame(btn_frame, bg="#ddd")
    action_btn_frame.pack(fill="x", pady=(0, 10))

    tk.Button(action_btn_frame, text="🚀 INICIAR SIMULACIÓN", command=validar_y_lanzar, 
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2).pack(side="left", padx=20)
    
    tk.Button(action_btn_frame, text="SALIR",  command=cerrar_programa,  
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2).pack(side="right", padx=20)

    root.mainloop()
    


# ==========================================
# 7. EJECUCIÓN SECUENCIAL BLINDADA
# ==========================================
if __name__ == "__main__":
    try:
        run_gui_parametrizada() # 1. Configurar
        
        print("\n--- INICIANDO SIMULACIÓN MODO SECUENCIAL ---")
        sim = HOSSEngine()
        sim.inicializar_mundo() # 2. Inicializar (MATRIZ LOCAL)
        
        # 3. Bucle Secuencial (Sin multiproceso)
        for _ in range(Config.SIM_ANOS): 
            sim.ciclo()
        
        sim.exportar_datos()

        # 4. GUARDADO DE SEGURIDAD (La "Base de Datos")
        print("\n--- VOLCANDO DATOS A DISCO (ETL) ---")
        print("Guardando matriz de actividades para auditoría...")
        print("\n--- VOLCANDO DATOS A DISCO ---")
        np.save('auditoria_mat_pob.npy', sim.mat_pob)
        np.save('auditoria_mat_act.npy', sim.mat_act)
        print("✅ Archivos guardados con éxito.")
        
        # 5. LANZAR GUI (Ahora lee directamente del objeto 'sim' local, que tiene los datos)
        print("--- ABRIENDO RESULTADOS ---")
        lanzar_explotacion_datos(sim)

    except KeyboardInterrupt:
        print("\n[MAIN] Interrupción por teclado (Ctrl+C).")
    except Exception as e:
        print(f"\n[MAIN] ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()