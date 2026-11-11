import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )
    
    por_letra = df.groupby(0)[1].agg(["max", "min"])

    resultado = []
    for letra, fila in por_letra.iterrows():
        resultado.append((letra, int(fila["max"]), int(fila["min"])))

    return resultado
