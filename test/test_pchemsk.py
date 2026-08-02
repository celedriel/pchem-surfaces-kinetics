import pytest
import pandas as pd
import numpy as np
from core.arrhenius import CineticaArrhenius
from core.isoterma import IsotermaAdsorcao
from core.ordem import OrdemReacao

def test_arrhenius_calculo_correto():
    df_input = pd.DataFrame({
        "Temperatura (K)": [298.0, 308.0, 318.0, 328.0],
        "Tempo (s)": [125.0, 64.0, 33.0, 17.0]
    })
    analise = CineticaArrhenius(df_input)
    df_proc = analise.process_data()
    resultados = analise.fit_model()
    
    assert "erro" not in resultados
    assert resultados['R2'] > 0.98
    assert resultados['Ea_J'] > 0  

def test_isoterma_freundlich_sucesso():
    df_input = pd.DataFrame({
        "Massa_Carvao": [0.5, 0.5, 0.5, 0.5],
        "Vol_Total": [50.0, 50.0, 50.0, 50.0],
        "Conc_Inicial": [0.1, 0.05, 0.025, 0.0125],
        "Vol_Aliquota": [10.0, 10.0, 10.0, 10.0],
        "Vol_Gasto": [8.5, 3.8, 1.6, 0.6]
    })
    analise = IsotermaAdsorcao(df_input, molar_mass=60.05, titrant_conc=0.1)
    df_proc = analise.process_data()
    resultados = analise.fit_model("Freundlich")
    
    assert "erro" not in resultados
    assert 'K' in resultados
    assert 'n' in resultados
    assert resultados['n'] is not None

def test_ordem_reacao_convergencia():
    df_input = pd.DataFrame({
        "Tempo (s)": [20.0, 40.0, 60.0, 80.0, 100.0],
        "[H2O2] (mol/L)": [0.082, 0.067, 0.055, 0.045, 0.037]
    })
    analise = OrdemReacao(df_input)
    df_proc = analise.process_data()
    resultados = analise.fit_model()
    
    assert "erro" not in resultados
    assert 'best_fit' in resultados
    assert '1a_ordem' in resultados or '2a_ordem' in resultados

def test_validador_centralizado_colunas_ausentes():
    df_invalido = pd.DataFrame({
        "ColunaErrada": [1, 2, 3]
    })
    analise = CineticaArrhenius(df_invalido)
    
    with pytest.raises(ValueError):
        analise.process_data()

def test_isoterma_dados_insuficientes():
    df_poucos_pontos = pd.DataFrame({
        "Massa_Carvao": [0.5, 0.5],
        "Vol_Total": [50.0, 50.0],
        "Conc_Inicial": [0.1, 0.05],
        "Vol_Aliquota": [10.0, 10.0],
        "Vol_Gasto": [8.5, 3.8]
    })
    analise = IsotermaAdsorcao(df_poucos_pontos, molar_mass=60.05, titrant_conc=0.1)
    analise.process_data()
    resultados = analise.fit_model("Langmuir")
    
    assert "erro" in resultados
    assert "Insuficiência de dados" in resultados["erro"]
