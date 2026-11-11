import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )

    codes_count = df[3].apply(lambda x: len(x.split(",")))
    metrics_count = df[4].apply(lambda x: len(x.split(",")))
    result = list(zip(df[0], codes_count, metrics_count))
    return result

