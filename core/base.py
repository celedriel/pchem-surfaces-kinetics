import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAnalise(ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()
        self.results: Dict[str, Any] = {}
        self.linhas_descartadas: int = 0

    @abstractmethod
    def process_data(self) -> pd.DataFrame:
        """Filtra dados inválidos e retorna o DataFrame processado."""
        pass

    @abstractmethod
    def fit_model(self, *args, **kwargs) -> Dict[str, Any]:
        """Realiza a regressão matemática e retorna o dicionário de resultados."""
        pass

    @abstractmethod
    def plot_graph(self, *args, **kwargs):
        """Gera e retorna a figura (gráfico) do Matplotlib."""
        pass
