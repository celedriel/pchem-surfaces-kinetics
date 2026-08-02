import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# CONSTANTES

CONSTANTE_R_GASES = 8.314  # J/(mol.K)


# FUNÇÕES AUXILIARES

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
    plt.close(fig)

def renderizar_resultados(modulo: str, parametros: dict, grafico, df_resultados: pd.DataFrame, nome_arquivo_csv: str, modelo_escolhido: str = None):
    
    if "aviso" in parametros:
        st.warning(parametros["aviso"])

    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.write("### Parâmetros Calculados")
        
        if modulo == "Isotermas de Adsorção":
            if modelo_escolhido == "Freundlich":
                st.write(f"**K:** {parametros.get('K', 0):.4f}")
                st.write(f"**n:** {parametros.get('n', 0):.4f}")
            elif modelo_escolhido == "Langmuir":
                st.write(f"**$q_{{max}}$:** {parametros.get('q_max', 0):.4f} g/g")
                st.write(f"**$K_L$:** {parametros.get('K_L', 0):.4f} L/mol")
            st.write(f"**$R^2$:** {parametros.get('R2', 0):.4f}")
            
        elif modulo == "Cinética (Arrhenius)":
            st.write(f"**Energia de Ativação ($E_a$):** {parametros.get('Ea_J', 0):.2f} J/mol ({parametros.get('Ea_kJ', 0):.2f} kJ/mol)")
            st.write(rf"**Fator de Frequência ($\ln A$):** {parametros.get('ln_A', 0):.4f}")
            st.write(f"**$R^2$:** {parametros.get('R2', 0):.4f}")
            
        elif modulo == "Ordem de Reação":
            if '1a_ordem' in parametros:
                st.write("**Ajuste 1ª Ordem**")
                st.write(f"Constante (k): {parametros['1a_ordem']['k']:.5f}")
                st.write(f"MSE (Erro): {parametros['1a_ordem']['MSE']:.2e}")
                st.write("---")
            if '2a_ordem' in parametros:
                st.write("**Ajuste 2ª Ordem**")
                st.write(f"Constante (k): {parametros['2a_ordem']['k']:.5f}")
                st.write(f"MSE (Erro): {parametros['2a_ordem']['MSE']:.2e}")

    with col_res2:
        if grafico is not None:
            st.pyplot(grafico)
            close_plot(grafico)
            
    with st.expander("Ver Dados e Matriz de Cálculos"):
        st.dataframe(df_resultados)
        render_download_button(df_resultados, nome_arquivo_csv)
