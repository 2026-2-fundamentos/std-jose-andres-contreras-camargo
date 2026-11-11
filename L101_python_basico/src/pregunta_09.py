import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )
    
    count_dict = {}
    for metrics in df[4]:
        for metric in metrics.split(","):
            key = metric.split(":")[0]
            count_dict[key] = count_dict.get(key, 0) + 1
    count_dict_ordenado = dict(sorted(count_dict.items()))
    return count_dict_ordenado
