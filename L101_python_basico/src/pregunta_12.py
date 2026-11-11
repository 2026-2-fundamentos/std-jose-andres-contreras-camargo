import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )
    dict_result = {}
    
    for letter, metrics in zip(df[0], df[4]):
        total = sum(int(metric.split(":")[1]) for metric in metrics.split(","))
        dict_result[letter] = dict_result.get(letter, 0) + total
    
    dict_ordenado = dict(sorted(dict_result.items()))
    return dict_ordenado
