import streamlit as st
import pandas as pd
from core.isoterma import IsotermaAdsorcao 
from core.arrhenius import CineticaArrhenius
from core.ordem import OrdemReacao

st.set_page_config(page_title="FQ: Superfícies e Cinética", layout="wide")

st.title("Físico-Química de Superfícies e Cinética")
st.markdown("Selecione o módulo de análise desejado na barra lateral para prosseguir.")

modulo = st.sidebar.radio(
    "Escolha a Análise", 
    ["Isotermas de Adsorção", "Cinética (Arrhenius)", "Ordem de Reação"]
)

# MÓDULO 1: ISOTERMAS
if modulo == "Isotermas de Adsorção":
    st.header("Isotermas de Adsorção")
    
    modelo_escolhido = st.radio("Selecione o modelo matemático:", ["Freundlich", "Langmuir"], horizontal=True)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        massa_molar = st.number_input("Massa Molar do Ácido (g/mol)", min_value=0.01, value=60.05)
    with col2:
        conc_titulante = st.number_input("Concentração do Titulante (mol/L)", min_value=0.001, value=0.1)

    st.subheader("Tabela de Dados Experimentais")
    
    df_isoterma = pd.DataFrame({
        "Amostra": [1, 2, 3, 4],
        "Massa_Carvao": [0.5, 0.5, 0.5, 0.5],
        "Vol_Total": [50.0, 50.0, 50.0, 50.0],
        "Conc_Inicial": [0.1, 0.05, 0.025, 0.0125],
        "Vol_Aliquota": [10.0, 10.0, 10.0, 10.0],
        "Vol_Gasto": [0.0, 0.0, 0.0, 0.0]
    })
    
    df_editado_iso = st.data_editor(df_isoterma, num_rows="dynamic")

    if st.button("Processar Dados", key="btn_iso", type="primary"):
        analise = IsotermaAdsorcao(df_editado_iso, massa_molar, conc_titulante)
        df_resultados = analise.process_data()
        
        if not df_resultados.empty:
            # Passa a escolha do usuário para a classe calcular
            parametros = analise.fit_model(modelo_escolhido)
            grafico = analise.plot_graph()
            
            st.success(f"Análise concluída usando o modelo de **{modelo_escolhido}**!")
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.write("### Constantes Calculadas")
                if modelo_escolhido == "Freundlich":
                    st.write(f"**K (Capacidade de Adsorção):** {parametros['K']:.4f}")
                    st.write(f"**n (Intensidade):** {parametros['n']:.4f}")
                elif modelo_escolhido == "Langmuir":
                    st.write(f"**$q_{{max}}$ (Capacidade Máxima):** {parametros['q_max']:.4f} g/g")
                    st.write(f"**$K_L$ (Const. Langmuir):** {parametros['K_L']:.4f} L/mol")
                
                st.write(f"**$R^2$:** {parametros['R2']:.4f}")
                
            with col_res2:
                st.pyplot(grafico)
                
            st.write("### Matriz de Cálculos")
            st.dataframe(df_resultados)
        else:
            st.error("Erro: Preencha a tabela com valores maiores que zero para prosseguir.")

# MÓDULO 2: ARRHENIUS

elif modulo == "Cinética (Arrhenius)":
    st.header("Dependência da Velocidade com a Temperatura")
    
    st.subheader("Tabela de Dados Experimentais")
    
    df_arrhenius = pd.DataFrame({
        "Tubo": [1, 2, 3, 4],
        "Temperatura (K)": [298.0, 308.0, 318.0, 328.0],
        "Tempo (s)": [68.0, 30.26, 22.97, 16.77]
    })
    
    df_editado_arr = st.data_editor(df_arrhenius, num_rows="dynamic")
    
    if st.button("Processar Dados", key="btn_arr", type="primary"):
        analise = CineticaArrhenius(df_editado_arr)
        df_resultados = analise.process_data()
        
        if not df_resultados.empty:
            parametros = analise.fit_model()
            grafico = analise.plot_graph()
            
            st.success("Análise de Arrhenius concluída!")
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.write("### Parâmetros Cinéticos")
                st.write(f"**Energia de Ativação ($E_a$):** {parametros['Ea_J']:.2f} J/mol ({parametros['Ea_kJ']:.2f} kJ/mol)")
                st.write(rf"**Fator de Frequência ($\ln A$):** {parametros['ln_A']:.4f}")
                st.write(f"**$R^2$:** {parametros['R2']:.4f}")
            with col_res2:
                st.pyplot(grafico)
                
            st.write("### Matriz de Cálculos")
            st.dataframe(df_resultados)
        else:
            st.error("Erro: Verifique se as temperaturas e tempos informados são maiores que zero.")


# MÓDULO 3: ORDEM DE REAÇÃO

elif modulo == "Ordem de Reação":
    st.header("Determinação da Ordem (Conc. em Excesso)")
    
    st.subheader("Tabela de Dados Experimentais")
    
    df_ordem = pd.DataFrame({
        "Titulação": [1, 2, 3, 4, 5],
        "Tempo (s)": [38.0, 15.0, 29.0, 18.0, 15.0],
        "[H2O2] (mol/L)": [0.010, 0.016, 0.032, 0.040, 0.047]
    })
    
    df_editado_ord = st.data_editor(df_ordem, num_rows="dynamic")
    
    if st.button("Processar Dados", key="btn_ord", type="primary"):
        analise = OrdemReacao(df_editado_ord)
        df_resultados = analise.process_data()
        
        if not df_resultados.empty:
            parametros = analise.fit_models()
            fig1, fig2 = analise.plot_graphs()
            
            st.success(f"O modelo que melhor descreve a reação é o de **{parametros['best_fit']}**.")
            
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.write("### Ajuste 1ª Ordem")
                st.write(f"**$R^2$:** {parametros['reg1'].rvalue**2:.4f}")
                st.write(f"**Erro Residual (SQE):** {parametros['sqe1']:.4f}")
                st.pyplot(fig1)
                
            with col_res2:
                st.write("### Ajuste 2ª Ordem")
                st.write(f"**$R^2$:** {parametros['reg2'].rvalue**2:.4f}")
                st.write(f"**Erro Residual (SQE):** {parametros['sqe2']:.4f}")
                st.pyplot(fig2)
                
            st.write("### Matriz de Cálculos")
            st.dataframe(df_resultados)
        else:
            st.error("Erro: Verifique se os dados de tempo e concentração são válidos.")
