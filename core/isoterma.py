import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

class IsotermaAdsorcao:
    def __init__(self, df_raw, molar_mass, titrant_conc):
        self.df = df_raw.copy()
        self.molar_mass = molar_mass
        self.titrant_conc = titrant_conc
        self.results = {}
        self.linhas_descartadas = 0
        
    def process_data(self):
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
        
    def fit_model(self, model_name):
        try:
            if model_name == "Freundlich":
                reg = linregress(self.df['log_C'], self.df['log_xm'])
                self.results = {
                    'n': 1 / reg.slope if reg.slope != 0 else np.inf,
                    'K': 10**reg.intercept,
                    'R2': reg.rvalue**2,
                    'slope': reg.slope,
                    'intercept': reg.intercept
                }
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
            return self.results
        except Exception as e:
            return {"erro": str(e)}
        
    def plot_graph(self, model_name):
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
