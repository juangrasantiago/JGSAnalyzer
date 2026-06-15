import requests
import json
from datetime import datetime

ROJO    = "\033[91m"
AMARILLO= "\033[93m"
AZUL    = "\033[94m"
VERDE   = "\033[92m"
GRIS    = "\033[90m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

COLOR_RIESGO = {
    "ALTO":  ROJO,
    "MEDIO": AMARILLO,
    "BAJO":  AZUL,
}

#Hacer la petición HTTP y ver las cabeceras en crudo

def obtener_cabeceras(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers, timeout=5)
    return dict(response.headers)

CABECERAS_SEGURIDAD = {
    "Strict-Transport-Security": {
        "riesgo": "ALTO",
        "descripcion": "Sin HSTS: el navegador puede conectar por HTTP inseguro"
    },
    "Content-Security-Policy": {
        "riesgo": "ALTO",
        "descripcion": "Sin CSP: vulnerable a ataques XSS"
    },
    "X-Frame-Options": {
        "riesgo": "MEDIO",
        "descripcion": "Sin protección contra Clickjacking"
    },
    "X-Content-Type-Options": {
        "riesgo": "MEDIO",
        "descripcion": "Sin protección contra MIME sniffing"
    },
    "Referrer-Policy": {
        "riesgo": "BAJO",
        "descripcion": "Sin control de información en cabecera Referer"
    },
    "Permissions-Policy": {
        "riesgo": "BAJO",
        "descripcion": "Sin restricciones de APIs del navegador (cámara, micrófono...)"
    },
}

#Detectar qué cabeceras de seguridad faltan

def analizar_cabeceras(cabeceras: dict) -> dict:
    presentes = {}
    ausentes = {}

    for nombre, info in CABECERAS_SEGURIDAD.items():
        if nombre in cabeceras:
            presentes[nombre] = cabeceras[nombre]
        else:
            ausentes[nombre] = info

    return {"presentes": presentes, "ausentes": ausentes}

#Puntuación y calificación global del sitio

def calcular_puntuacion(resultado: dict) -> dict:
    PUNTOS = {"ALTO": 30, "MEDIO": 15, "BAJO": 5}
    puntuacion = 100

    for info in resultado["ausentes"].values():
        puntuacion -= PUNTOS.get(info["riesgo"], 0)

    puntuacion = max(0, puntuacion)

    if puntuacion >= 90:
        nota = "A"
        estado = "Excelente"
    elif puntuacion >= 70:
        nota = "B"
        estado = "Bueno"
    elif puntuacion >= 50:
        nota = "C"
        estado = "Mejorable"
    elif puntuacion >= 30:
        nota = "D"
        estado = "Deficiente"
    else:
        nota = "F"
        estado = "Crítico"

    return {"puntuacion": puntuacion, "nota": nota, "estado": estado}

#Exportar JSON

def exportar_json(url: str, resultado: dict, puntuacion: dict, fichero: str):
    datos = {
        "url": url,
        "fecha": datetime.now().isoformat(),
        "puntuacion": puntuacion["puntuacion"],
        "nota": puntuacion["nota"],
        "estado": puntuacion["estado"],
        "cabeceras_presentes": list(resultado["presentes"].keys()),
        "cabeceras_ausentes": {
            nombre: info for nombre, info in resultado["ausentes"].items()
        }
    }
    with open(fichero, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"\n{VERDE}[+] Reporte guardado en: {fichero}{RESET}")

#Banner
print(f"""
{BOLD}╔══════════════════════════════════════════════╗
║     JGSAnalyzer - Analizador de Cabeceras    ║                                           
╚══════════════════════════════════════════════╝{RESET}
""")

if __name__ == "__main__":
    url = input(f"{BOLD}🔍 Introduce la URL a analizar (ej: https://google.com): {RESET}").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print(f"\n{BOLD}Analizando:{RESET} {url}\n")

    cabeceras  = obtener_cabeceras(url)
    resultado  = analizar_cabeceras(cabeceras)
    puntuacion = calcular_puntuacion(resultado)

    print(f"{BOLD}{'─'*55}{RESET}")
    print(f"{BOLD}  ✅ CABECERAS DE SEGURIDAD PRESENTES{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}")
    if resultado["presentes"]:
        for nombre, valor in resultado["presentes"].items():
            valor_corto = valor[:60] + "..." if len(valor) > 60 else valor
            print(f"  {VERDE}✔{RESET}  {BOLD}{nombre}{RESET}")
            print(f"      {GRIS}{valor_corto}{RESET}")
    else:
        print(f"  {ROJO}Ninguna cabecera de seguridad encontrada{RESET}")

    print(f"\n{BOLD}{'─'*55}{RESET}")
    print(f"{BOLD}  ❌ CABECERAS AUSENTES{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}")
    for nombre, info in resultado["ausentes"].items():
        color = COLOR_RIESGO.get(info["riesgo"], RESET)
        print(f"  {color}✘{RESET}  {BOLD}{nombre}{RESET}  {color}[{info['riesgo']}]{RESET}")
        print(f"      {GRIS}{info['descripcion']}{RESET}")

    # Color de la nota según puntuación
    if puntuacion["nota"] in ("A",):
        color_nota = VERDE
    elif puntuacion["nota"] in ("B", "C"):
        color_nota = AMARILLO
    else:
        color_nota = ROJO

    print(f"\n{BOLD}{'─'*55}{RESET}")
    print(f"  {BOLD}PUNTUACIÓN:{RESET} {color_nota}{BOLD}{puntuacion['puntuacion']}/100  "
          f"Nota: {puntuacion['nota']} — {puntuacion['estado']}{RESET}")
    print(f"{BOLD}{'─'*55}{RESET}\n")

    #Guardar reporte JSON

    guardar = input(f"  {BOLD}¿Exportar reporte JSON? (s/n): {RESET}").strip().lower()
    if guardar == "s":
        nombre_fichero = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".json"
        exportar_json(url, resultado, puntuacion, nombre_fichero)

