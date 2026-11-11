import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "clusters_report.txt"


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    clusters = []

    for line in lines:
        partes = line.split()
        # Línea vacía
        if len(partes) == 0:
            continue

        # Inicio de clúster
        es_inicio = len(partes) >= 4 and partes[0].isdigit() and partes[3] == "%"

        if es_inicio:
            clusters.append(
                {
                    "cluster": int(partes[0]),
                    "cantidad_de_palabras_clave": int(partes[1]),
                    "porcentaje_de_palabras_clave": float(partes[2].replace(",", ".")),
                    "texto": " ".join(partes[4:]),
                }
            )
        # Continuación de clúster
        elif len(clusters) > 0 and not line.startswith("-") and not line.startswith("Cluster"):
            clusters[-1]["texto"] = clusters[-1]["texto"] + " " + " ".join(partes)

    # Limpiar el texto
    for cluster in clusters:
        texto = cluster["texto"].strip()
    # Quitar el punto final
        if texto.endswith("."):
          texto = texto[:-1]

        palabras = [p.strip() for p in texto.split(",") if p.strip() != ""]
        cluster["principales_palabras_clave"] = ", ".join(palabras)
        del cluster["texto"]

    return pd.DataFrame(clusters)

