import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "data.csv.gz"

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    df = pd.read_csv(
        INPUT_FILE,
        sep="\t",
        header=None,
        compression="gzip",
    )
    
    values = df[1].unique()
    resultado = []
    for value in sorted(values):
        letras = set(df[df[1] == value][0].tolist())
        resultado.append((value, sorted(letras)))
    
    return resultado
