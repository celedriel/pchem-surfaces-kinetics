import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def render_download_button(df: pd.DataFrame, filename: str) -> None:
    csv = df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    
    st.download_button(
        label="Baixar Dados Tratados (CSV)",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

def close_plot(fig) -> None:
    plt.close(fig)
