# Librerias necesarias para Proyecto Merrill-Crowe
# Ejecutar una sola vez

import subprocess
import sys

paquetes = [
    "pandas",
    "numpy",
    "scikit-learn",
    "xgboost",
    "lightgbm",
    "catboost",
    "statsmodels",
    "scipy",
    "matplotlib",
    "plotly",
    "shap",
    "optuna",
    "openpyxl",
    "joblib",
    "pyodbc",
    "sqlalchemy",
    "opcua",
    "pymssql"
]

for paquete in paquetes:
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

print("Instalacion completada.")
