import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
from typing import Dict, Any
from .base import BaseAnalise

class IsotermaAdsorcao(BaseAnalise):
    def __init__(self, df_raw: pd.DataFrame, molar_mass: float, titrant_conc: float) -> None:
        super().__init__(df_raw)
        self.molar_mass = molar_mass
        self.titrant_conc = titrant_conc
        
    def process_data(self) -> pd.DataFrame:
        self.df['Conc_Final'] = (self.df['Vol_Gasto'] * self.titrant_conc) / self.df['Vol_Aliquota']
        self.df['X_Adsorvido'] = (self.df['Conc_Inicial'] - self.df['Conc_Final']) * (self.df['Vol_Total'] / 1000) * self.molar_mass
        self.df['X_m'] = self.df['X_Adsorvido'] / self.df['Massa_Carvao']
        
        len_antes = len(self.df)
        self.df = self.df[(self.df['Conc_Final'] > 0) & (self.df['X_m'] > 0)].copy()
        self.linhas_descartadas = len_antes - len(self.df)
        
        self.df['log_C'] = np.log10(self.df['Conc_Final'])
        self.df['log_xm'] = np.log10(self.df['X_m'])
        self.df['Ce_sobre_xm'] = self.df['Conc_Final'] / self.df['X_m']
        
        return self.df
        
    def fit_model(self, model_name: str) -> Dict[str, Any]:
        """Realiza a regressão linear para o modelo de Freundlich ou Langmuir."""
        if len(self.df) < 3:
            return {"erro": "Insuficiência de dados: o modelo exige pelo menos 3 pontos experimentais válidos após a filtragem."}
            
        if model_name not in ["Freundlich", "Langmuir"]:
            return {"erro": f"Modelo matemático '{model_name}' não é suportado."}
            
        try:
            if model_name == "Freundlich":
                reg = linregress(self.df['log_C'], self.df['log_xm'])
                n_val = 1 / reg.slope if reg.slope != 0 else None
                self.results = {
                    'n': n_val,
                    'K': 10**reg.intercept,
                    'R2': reg.rvalue**2,
                    'slope': reg.slope,
                    'intercept': reg.intercept
                }
                if n_val is None:
                    self.results['aviso'] = "Atenção: A inclinação da reta de Freundlich é zero, resultando em 'n' indefinido."
                    
            elif model_name == "Langmuir":
                reg = linregress(self.df['Conc_Final'], self.df['Ce_sobre_xm'])
                q_max = 1 / reg.slope if reg.slope != 0 else 0
                k_l = reg.slope / reg.intercept if reg.intercept != 0 else 0
                
                self.results = {
                    'q_max': q_max,
                    'K_L': k_l,
                    'R2': reg.rvalue**2,
                    'slope': reg.slope,
                    'intercept': reg.intercept
                }
                
                if reg.slope <= 0:
                     self.results['aviso'] = "Atenção: A inclinação é nula ou negativa. O modelo de Langmuir pode não ser aplicável."
                elif abs(reg.intercept) < 1e-10:
                    self.results['aviso'] = "Intercepto próximo de zero. Verifique a validade do modelo de Langmuir."
                    
            return self.results
        except Exception as e:
            return {"erro": str(e)}
            
    def plot_graph(self, model_name: str):
        fig, ax = plt.subplots(figsize=(8, 5))
        
        if model_name == "Freundlich":
            ax.plot(self.df['log_C'], self.df['log_xm'], 'bo', label='Dados Experimentais')
            ax.plot(self.df['log_C'], self.results.get('slope', 0) * self.df['log_C'] + self.results.get('intercept', 0), 
                    'k--', label=f"Freundlich ($R^2={self.results.get('R2', 0):.4f}$)")
            ax.set_xlabel('log C')
            ax.set_ylabel('log x/m')
            ax.set_title('Isoterma de Adsorção - Freundlich')
            
        elif model_name == "Langmuir":
            ax.plot(self.df['Conc_Final'], self.df['Ce_sobre_xm'], 'go', label='Dados Experimentais')
            ax.plot(self.df['Conc_Final'], self.results.get('slope', 0) * self.df['Conc_Final'] + self.results.get('intercept', 0), 
                    'k--', label=f"Langmuir ($R^2={self.results.get('R2', 0):.4f}$)")
            ax.set_xlabel('Ce (mol/L)')
            ax.set_ylabel('Ce / (x/m)')
            ax.set_title('Isoterma de Adsorção - Langmuir')
            
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        return fig
