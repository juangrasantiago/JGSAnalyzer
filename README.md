# JGSAnalyzer - Analizador de Cabeceras HTTP 🛡️

Herramienta de análisis de cabeceras de seguridad HTTP desarrollada en Python.
Detecta cabeceras ausentes, clasifica el riesgo y genera reportes JSON.


## Características
- Detección de 6 cabeceras críticas de seguridad
- Puntuación global de 0 a 100 con nota (A-F)
- Salida coloreada en terminal
- Exportación de reportes en JSON

## Instalación
pip install requests

## Uso
python analyzer.py

## Cabeceras analizadas
| Cabecera | Riesgo si ausente |
|---|---|
| Strict-Transport-Security | ALTO |
| Content-Security-Policy | ALTO |
| X-Frame-Options | MEDIO |
| X-Content-Type-Options | MEDIO |
| Referrer-Policy | BAJO |
| Permissions-Policy | BAJO |

## Ejemplos de resultados reales
- GitHub: 95/100 — Nota A
- YouTube: 95/100 — Nota A  
- Marca.com: 5/100 — Nota F

Creado por Juan Gabriel Santiago