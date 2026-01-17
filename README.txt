# HOSS(-5) · Human Organizations Simulations Start

## 1. ¿Qué es HOSS(-5)?
**HOSS(-5)** es un prototipo avanzado de simulación social desarrollado en Python. Su objetivo es explorar cómo reglas simples, aplicadas a individuos con intencionalidad, generan patrones sociales, económicos y organizativos complejos a lo largo del tiempo.

No pretende predecir sociedades reales. Es un entorno experimental para **comparar escenarios**, observar **regímenes emergentes** y reflexionar sobre el **diseño organizativo de la sociedad** desde una perspectiva ingenieril.

## 2. La pregunta de fondo
HOSS nace de una pregunta sencilla pero ambiciosa:

> *¿Podemos simular cómo se organiza una sociedad humana sin reducir a las personas a meras ecuaciones?*

La sociedad humana combina racionalidad e imprevisibilidad, intencionalidad y azar. HOSS intenta modelar ese espacio intermedio donde las decisiones individuales, los recursos y las reglas colectivas interactúan y producen resultados no triviales.

## 3. Qué hace hoy el código
La versión **HOSS(-5)** implementa una sociedad artificial de pequeña escala donde cada individuo (ph, *punto humano*):

*   Nace, se forma, trabaja, consume y desaparece.
*   Toma decisiones condicionadas por su psicología, estatus económico e intencionalidad.
*   Interactúa indirectamente con otros individuos a través de familias, empresas y Estado.

El sistema permite similar algunos miles de ph() durante decenas de años virtuales y generar grandes volúmenes de datos para su análisis posterior.

## 4. Arquitectura del modelo

### 4.1 El agente: ph (punto humano)
Cada individuo está modelado como un objeto autónomo con:
*   **Ciclo de vida:** gestación, nacimiento y muerte (probabilística y sensible a eventos).
*   **Psicología:** matriz psicológica (arquetipo × carácter).
*   **Decisión:** mapeo en un espacio de intencionalidad y estatus económico.
*   **Actividad anual:** trabajo, educación, ocio, organización y consumo.
*   **Evolución:** carrera profesional, mejora de ingresos por formación o azar.

### 4.2 Entorno social y macroeconomía
*   **Familias, empresas** (10 sectores) y **Estado**.
*   Producción y precios mediante reglas simples (no mercado libre pleno).
*   Salarios modulados por ~200 categorías profesionales.
*   Estado con servicios públicos, empleo y **Renta Básica Universal (RBU)**.
*   Ajuste automático anual de impuestos y RBU para buscar equilibrio fiscal.

### 4.3 Métricas del sistema
*   Población, PIB, ingresos.
*   Índice de Gini e IDH.
*   Contraste con distribuciones Gamma.

## 5. Arquitectura técnica
*   Sustitución completa de MySQL por **estructuras en memoria** (alto rendimiento).
*   Persistencia final en archivos binarios, CSV y XLSX para auditoría externa.
*   Configuración de escenarios y parámetros desde GUI.
*   Versión de depuración sin multiproceso para garantizar consistencia de datos.

## 6. Explotación y análisis de resultados
HOSS separa estrictamente **simulación y explotación**. El análisis no modifica el modelo ni introduce hipótesis nuevas.

### 6.1 Nivel micro · Espacios de fases
*   Trayectorias individuales en espacios de estado.
*   Observación de regímenes estables, dispersión y recorridos biográficos.
*   No predictivo, exploratorio.

### 6.2 Nivel macro · Series temporales
*   Variables agregadas año a año.
*   Detección de tendencias, ciclos y cambios de régimen.
*   Interpretación como propiedades emergentes del sistema.

### 6.3 Contraste micro–macro · Hipótesis Gamma
*   Ajuste anual de distribuciones Gamma sobre ingresos individuales.
*   Contraste del parámetro α con Gini e IDH.
*   Relación estructural compatible (no causal).

## 7. Qué NO hace (limitaciones actuales)
*   No existen relaciones sociales directas complejas entre individuos.
*   El mercado es simulado, no dinámico oferta–demanda.
*   Las organizaciones son cajas negras (sin protocolos internos detallados).
*   No pretende validación empírica directa.

**HOSS(-5) es un prototipo, no una versión final.**

## 8. Relación con el proyecto DOS
HOSS se enmarca en un trabajo más amplio: **Diseño Organizativo de la Sociedad (DOS)**, desarrollado durante más de 15 años a partir de investigación académica, análisis organizativo y reflexión teórica.

La hipótesis central es que el diseño organizativo social puede abordarse con un rigor comparable al del diseño industrial, arquitectónico o de software, integrando modelos, datos y validación posterior.

## 9. Estado del proyecto y futuro
HOSS(-5) no es el final. Conceptualmente, el proyecto necesitaría varias fases más para aproximarse a una versión “CERO” funcional.

Posibles líneas futuras:
En ausencia de  falsación, parece interesante dedicar esfuerzos a lograr métricas de las siguientes variables macroscópicas extraidas de los procesos de planificación estratégica de grandes ciudades y Áreas metropolitanas:
*   Liderazgo (Lrec, Lgen).
*   Temperatura ciudadana (TC) y compromise de los agentes (CAG).
*   Organización marco (OM) y desempeño institucional (OT).
*   Manejo de la complejidad política y metropolitana (MC).

Este repositorio se publica como **semilla abierta**.

---

## 10. Nota personal del autor
Hoy tengo 76 años. Sigo caminando, pero también cerrando etapas.

HOSS se libera con la esperanza de que alguien, en algún momento, quiera retomarlo, discutirlo, criticarlo y transformarlo.

Las versiones recientes han sido desarrolladas con la colaboración de **Gemini (Google)** y **ChatGPT (OpenAI)**. Las ideas, el marco conceptual y la validación crítica son humanos; la implementación ha sido asistida por IA.

> *“¿Qué pretendo encontrar, internándome en el viento?”*
> — Taneda Santōka

## 11. Enlaces y contacto
Material complementario referido a la versión HOSS(-6) (textos, vídeos y código):
*   [Adiós HOSS 1](https://onuglobal.com/2025/04/11/adios-hoss-1/)
*   [Adiós HOSS 2](https://onuglobal.com/2025/04/11/adios-hoss-2/)
*   [Adiós HOSS 3](https://onuglobal.com/2025/04/11/adios-hoss-3/)

**Contacto:** invatresp@gmail.com

Gracias por leer hasta aquí.

**José Quintás · Gemini · ChatGPT**