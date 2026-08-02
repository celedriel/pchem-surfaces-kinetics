import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
from typing import Dict, Any
from .base import BaseAnalise
import utils 

class CineticaArrhenius(BaseAnalise):
    def __init__(self, df_raw: pd.DataFrame) -> None:
        super().__init__(df_raw)
        
    def process_data(self) -> pd.DataFrame:
        len_antes = len(self.df)
        self.df = self.df[(self.df['Temperatura (K)'] > 0) & (self.df['Tempo (s)'] > 0)].copy()
        self.linhas_descartadas = len_antes - len(self.df)
        
        self.df['k (1/s)'] = 1.0 / self.df['Tempo (s)']
        self.df['1/T'] = 1.0 / self.df['Temperatura (K)']
        self.df['ln(k)'] = np.log(self.df['k (1/s)'])
        
        return self.df
        
    def fit_model(self) -> Dict[str, Any]:
        if self.df.empty:
            return {"erro": "Sem dados suficientes após a filtragem."}
            
        try:
            reg = linregress(self.df['1/T'], self.df['ln(k)'])
            ea_j = -reg.slope * utils.CONSTANTE_R_GASES 
            
            self.results = {
                'Ea_J': ea_j,
                'Ea_kJ': ea_j / 1000,
                'ln_A': reg.intercept,
                'R2': reg.rvalue**2,
                'slope': reg.slope,
                'intercept': reg.intercept
            }
            
            
            if reg.slope > 0:
                 self.results['aviso'] = "Atenção: A inclinação (slope) é positiva, resultando em uma Energia de Ativação negativa. Verifique os dados, pois isso aponta uma anomalia termodinâmica."
                 
            return self.results
        except Exception as e:
            return {"erro": str(e)}
            
    def plot_graph(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(self.df['1/T'], self.df['ln(k)'], 'ro', label='Dados Experimentais')
        ax.plot(self.df['1/T'], self.results.get('slope', 0) * self.df['1/T'] + self.results.get('intercept', 0), 
                'k--', label=f"Arrhenius ($R^2={self.results.get('R2', 0):.4f}$)")
        
        ax.set_xlabel('1/T (1/K)')
        ax.set_ylabel('ln(k)')
        ax.set_title('Cinética de Arrhenius: ln(k) vs 1/T')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        return fig
