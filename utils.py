import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def render_download_button(df: pd.DataFrame, filename: str) -> None:
    """Gera um botão de download do CSV padronizado para o Excel Brasileiro."""
    csv = df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    
    st.download_button(
        label="Baixar Dados Tratados (CSV)",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

def close_plot(fig) -> None:
    """Limpa a memória RAM fechando a figura do Matplotlib após a renderização."""
    plt.close(fig)
