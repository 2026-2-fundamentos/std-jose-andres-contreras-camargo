import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )
    print(df.head())
    grouped = df.groupby(df[0]).sum()
    
    return [(letra, suma) for letra, suma in grouped.iloc[:, 0].items()]
