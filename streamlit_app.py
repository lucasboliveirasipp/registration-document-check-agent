"""Ponto de entrada do app:  streamlit run streamlit_app.py

O app/agent.py usa imports relativos, então é executado como módulo do pacote app.
"""
import runpy
import sys
from pathlib import Path

_PASTA = Path(__file__).resolve().parent
for caminho in (str(_PASTA), str(_PASTA / "app")):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

runpy.run_module("app.agent", run_name="__main__")
