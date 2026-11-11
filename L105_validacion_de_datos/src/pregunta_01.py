import json
import pandas as pd
from pathlib import Path

PATH = Path(__file__).resolve().parents[1]
INPUT_FILE = PATH / "data" / "ventas.csv.gz"
OUTPUT_FILE = PATH / "submission" / "data_quality_report.json"

def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    df = pd.read_csv(
        INPUT_FILE,
        sep=",",
        dtype=str,
        keep_default_na=False,
        compression="gzip",
        encoding="utf-8",
    )
    
    # Normalizar los encabezados
    df.columns = (
        df.columns.str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    
    columnas_requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]
    
    valores_faltantes = ["", "N/A"]
    patron_email = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    
    row_count = len(df)
    column_count = len(df.columns)
    
    columnas_archivo = list(df.columns)
    missing_required_columns = sorted(set(columnas_requeridas) - set(columnas_archivo))
    unexpected_columns = sorted(set(columnas_archivo) - set(columnas_requeridas))
    
    duplicate_row_count = int(df.duplicated().sum())
    duplicate_supplier_id_row_count = int(df["supplier_id"].duplicated(keep=False).sum())
    
    es_faltante = df.isin(valores_faltantes)
    missing_value_count_by_column = es_faltante.sum().astype(int).to_dict()

    emails = df["contact_email"]
    emails_presentes = emails[~emails.isin(valores_faltantes)]
    emails_validos = emails_presentes.str.match(patron_email)
    invalid_email_count = int((~emails_validos).sum())

    units_num = pd.to_numeric(df["units"], errors="coerce")
    es_numerico = units_num.notna()
    no_positivo = units_num <= 0
    no_entero = (units_num % 1) != 0
    invalid_unit_count = int((es_numerico & (no_positivo | no_entero)).sum())
    
    paises = df["country"]
    paises_presentes = paises[~paises.isin(valores_faltantes)]
    country_values = sorted(paises_presentes.unique().tolist())
    
    reporte = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values
    }
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(reporte, f)

    return reporte
