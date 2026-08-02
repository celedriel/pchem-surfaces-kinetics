import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func_1a_ordem(t, C0, k):
    return C0 * np.exp(-k * t)

def func_2a_ordem(t, C0, k):
    return 1.0 / ((1.0 / C0) + k * t)

class OrdemReacao:
    def __init__(self, df_raw):
        self.df = df_raw.copy()
        self.results = {}
        self.col_t = 'Tempo (s)'
        self.col_c = '[H2O2] (mol/L)'
        
    def process_data(self):
        self.df = self.df[(self.df[self.col_t] >= 0) & (self.df[self.col_c] > 0)].copy()
        return self.df
        
    def fit_models(self):
        t = self.df[self.col_t].values
        c = self.df[self.col_c].values
        
        p0_guess = [c[0], 0.001]
        
        try:
            # Fit 1ª Ordem 
            popt1, _ = curve_fit(func_1a_ordem, t, c, p0=p0_guess, bounds=([0, 0], [np.inf, np.inf]), maxfev=10000)
            c_pred1 = func_1a_ordem(t, *popt1)
            mse1 = np.mean((c - c_pred1)**2)
            
            # Fit 2ª Ordem 
            popt2, _ = curve_fit(func_2a_ordem, t, c, p0=p0_guess, bounds=([0, 0], [np.inf, np.inf]), maxfev=10000)
            c_pred2 = func_2a_ordem(t, *popt2)
            mse2 = np.mean((c - c_pred2)**2)
            
            best_fit = "1ª Ordem" if mse1 < mse2 else "2ª Ordem"
            
            self.results = {
                '1a_ordem': {'C0': popt1[0], 'k': popt1[1], 'MSE': mse1},
                '2a_ordem': {'C0': popt2[0], 'k': popt2[1], 'MSE': mse2},
                'best_fit': best_fit
            }
        except (RuntimeError, ValueError) as e:
            self.results = {"erro": f"Falha na convergência matemática: {str(e)}"}
        except Exception as e:
            self.results = {"erro": str(e)}
            
        return self.results
        
    def plot_graphs(self):
        t = self.df[self.col_t].values
        c = self.df[self.col_c].values
        t_smooth = np.linspace(min(t), max(t), 100)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico 1ª Ordem
        c_fit1 = func_1a_ordem(t_smooth, self.results['1a_ordem']['C0'], self.results['1a_ordem']['k'])
        ax1.plot(t, c, 'ro', label='Experimental')
        ax1.plot(t_smooth, c_fit1, 'k-', label=f"Fit 1ª Ordem\nMSE: {self.results['1a_ordem']['MSE']:.2e}")
        ax1.set_xlabel('Tempo (s)')
        ax1.set_ylabel('[H2O2] (mol/L)')
        ax1.set_title('Ajuste Não-Linear: 1ª Ordem')
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        # Gráfico 2ª Ordem
        c_fit2 = func_2a_ordem(t_smooth, self.results['2a_ordem']['C0'], self.results['2a_ordem']['k'])
        ax2.plot(t, c, 'bo', label='Experimental')
        ax2.plot(t_smooth, c_fit2, 'k--', label=f"Fit 2ª Ordem\nMSE: {self.results['2a_ordem']['MSE']:.2e}")
        ax2.set_xlabel('Tempo (s)')
        ax2.set_ylabel('[H2O2] (mol/L)')
        ax2.set_title('Ajuste Não-Linear: 2ª Ordem')
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)
        
        return fig
