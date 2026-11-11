import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )
    
    metrics = df[4].str.split(",", expand=True).stack().str.split(":", expand=True)
    metrics.columns = ["key","value"]
    metrics["value"] = metrics["value"].astype(int)
    
    por_clave = metrics.groupby("key")["value"].agg(["max", "min"])
    
    resultado = []
    for key, fila in por_clave.iterrows():
        resultado.append((key, int(fila["min"]), int(fila["max"])))
        
    return resultado
