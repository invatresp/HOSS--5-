# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 22:44:05 2026

@author: Pepo & Gem
"""

# -*- coding: utf-8 -*-
"""
Corregido: El cálculo (varianza/media) da directamente la ESCALA (scale), 
no la tasa. Por tanto, no hay que invertirla al dársela a Scipy.
"""

import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np # Importamos numpy para el vector X de la línea

"""
Son datos de ingresos MEDIOS por persona y provincia
# Abrir el archivo y convertirlo directamente en lista
lista_datos = []
with open('INE2015.csv', 'r') as file:
    reader = csv.reader(file)
    lista_datos.extend([float(x) for x in file])
"""

lista_datos =[8029,8489,8614,8877,8401,8318,8688,9051,11297,10911,12020,11959,11213,9548,9073,11229,9745,12093,11138,11392,10667,10730,11674,11682,9859,9150,8786,9009,11036,8845,12853,11095,10914,10817,8695,10136,10377,8448,9081,11024,10283,10189,10153,13779,8908,13949,11191,10696,9961]

lista_datos.sort()

# Estadisticos necesarios
minimo = min(lista_datos)
maximo = max(lista_datos)

media = sum(lista_datos) / len(lista_datos)
varianza = sum((x - media)**2 for x in lista_datos) / (len(lista_datos) - 1)  
print('Minimo:',minimo,'Máximo:', maximo,'Media:', media,'Varianza:', varianza)


# ==========================================
# GRÁFICA 1 (media y varianza calculadas)
# ==========================================

# varianza/media calcula la ESCALA de la distribución Gamma
beta_tabla = varianza/media 
alfa_tabla = media / beta_tabla
print('\nPrimera elaboración->','Alfa: ', alfa_tabla, 'Scale: ', beta_tabla)

fig, ax = plt.subplots(2, 1, figsize=(8, 10))

# Eje X de los datos para el histograma
x_datos = lista_datos
ax[0].hist(x_datos, bins=12, density=True, alpha=0.4, color='green', edgecolor='black', label='Muestra CSV')

# Creamos un eje X de 200 puntos continuos para que la curva sea totalmente suave
x_plot = np.linspace(8000, 14000, 200)

# ¡Corregido! Usamos directamente la escala calculada
y_tabla = stats.gamma.pdf(x_plot, a=alfa_tabla, scale=beta_tabla)

ax[0].plot(x_plot, y_tabla, label='Gamma.España. Año 2015. € medio/ persona-año-provincial')
ax[0].set_title('Distribución Gamma de Ingresos')
ax[0].set_xlabel('x')
ax[0].set_ylabel('f(x)')
ax[0].set_ylim(0, 0.001) 
# Extendido a 14000 porque el máximo de tus datos es 13949
ax[0].set_xlim(8000, 14000) 
ax[0].legend()


# ==========================================
# GRÁFICA 2 (se conocen IDH, Gini y EM)
# ==========================================

IDH = 88.9
Gini = 34.6
EM = 59

beta_tabla = (IDH*EM)/Gini
alfa_tabla = media / beta_tabla

print('\nSegunda elaboración-> ','Alfa: ', alfa_tabla, 'Scale: ', beta_tabla)
print('Media Ingresos: ', media,'Media Constructo (IDH,Gini,EM:)', alfa_tabla * beta_tabla )

# ¡Corregido! Usamos directamente la escala calculada
y_tabla_2 = stats.gamma.pdf(x_plot, a=alfa_tabla, scale=beta_tabla)

ax[1].plot(x_plot, y_tabla_2, label='Gamma  España, año 2015. (IDH 88,9 Gini 34,6 EM 59)')
ax[1].set_title('Distribución Gamma (A partir de constructo: IDH,Gini,EM)')
ax[1].set_xlabel('x')
ax[1].set_ylabel('f(x)')
ax[1].set_ylim(0, 0.001) 
ax[1].set_xlim(8000, 14000)
ax[1].legend()

plt.tight_layout()
plt.show()