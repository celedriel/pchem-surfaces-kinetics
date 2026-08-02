import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

class OrdemReacao:
    def __init__(self, df_raw):
        self.df = df_raw.copy()
        self.results = {}
        
    def process_data(self):
        self.df = self.df[(self.df['Tempo (s)'] > 0) & (self.df['[H2O2] (mol/L)'] > 0)].copy()
        
        self.df['log[H2O2]'] = np.log10(self.df['[H2O2] (mol/L)'])
        self.df['1/[H2O2]'] = 1.0 / self.df['[H2O2] (mol/L)']
        
        return self.df
        
    def fit_models(self):
        reg1 = linregress(self.df['Tempo (s)'], self.df['log[H2O2]'])
        reg2 = linregress(self.df['Tempo (s)'], self.df['1/[H2O2]'])
        
        pred1 = reg1.slope * self.df['Tempo (s)'] + reg1.intercept
        sqe1 = np.sum((self.df['log[H2O2]'] - pred1)**2)
        
        pred2 = reg2.slope * self.df['Tempo (s)'] + reg2.intercept
        sqe2 = np.sum((self.df['1/[H2O2]'] - pred2)**2)
        
        best_fit = "1ª Ordem" if reg1.rvalue**2 > reg2.rvalue**2 else "2ª Ordem"
        
        self.results = {
            'reg1': reg1,
            'sqe1': sqe1,
            'reg2': reg2,
            'sqe2': sqe2,
            'best_fit': best_fit
        }
        return self.results
        
    def plot_graphs(self):
        # Gráfico 1ª Ordem
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(self.df['Tempo (s)'], self.df['log[H2O2]'], 'gs', label='Exp')
        ax1.plot(self.df['Tempo (s)'], self.results['reg1'].slope * self.df['Tempo (s)'] + self.results['reg1'].intercept, 
                 'k-', label=f"1ª Ordem ($R^2={self.results['reg1'].rvalue**2:.4f}$)")
        ax1.set_xlabel('Tempo (s)')
        ax1.set_ylabel('log[H2O2]')
        ax1.set_title('Análise: 1ª Ordem')
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        # Gráfico 2ª Ordem
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(self.df['Tempo (s)'], self.df['1/[H2O2]'], 'bo', label='Exp')
        ax2.plot(self.df['Tempo (s)'], self.results['reg2'].slope * self.df['Tempo (s)'] + self.results['reg2'].intercept, 
                 'k--', label=f"2ª Ordem ($R^2={self.results['reg2'].rvalue**2:.4f}$)")
        ax2.set_xlabel('Tempo (s)')
        ax2.set_ylabel('1/[H2O2]')
        ax2.set_title('Análise: 2ª Ordem')
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)
        
        return fig1, fig2
