import streamlit as st
import pandas as pd
import utils
from core.isoterma import IsotermaAdsorcao
from core.arrhenius import CineticaArrhenius
from core.ordem import OrdemReacao

st.set_page_config(page_title="FQ: Superfícies e Cinética", layout="wide")
st.title("Físico-Química de Superfícies e Cinética")

if st.sidebar.button("Restaurar Dados Padrão"):
    st.session_state.clear()
    st.rerun()

modulo = st.sidebar.radio(
    "Escolha a Análise",
    ["Isotermas de Adsorção", "Cinética (Arrhenius)", "Ordem de Reação"],
)


# MÓDULO 1: ISOTERMAS

if modulo == "Isotermas de Adsorção":
    st.header("Isotermas de Adsorção")
    modelo_escolhido = st.radio(
        "Selecione o modelo matemático:", ["Freundlich", "Langmuir"], horizontal=True
    )
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        massa_molar = st.number_input(
            "Massa Molar do Adsorvato (g/mol)", min_value=0.01, value=60.05
        )
    with col2:
        conc_titulante = st.number_input(
            "Concentração do Titulante (mol/L)", min_value=0.001, value=0.1
        )
    with col3:
        fator_esteq = st.number_input(
            "Fator Estequiométrico (Titulante/Titulado)", min_value=0.01, value=1.0
        )

    st.subheader("Tabela de Dados Experimentais")
    if "df_iso" not in st.session_state:
        st.session_state.df_iso = pd.DataFrame(
            {
                "Amostra": [1, 2, 3, 4],
                "Massa_Adsorvente": [0.5, 0.5, 0.5, 0.5],
                "Vol_Total": [50.0, 50.0, 50.0, 50.0],
                "Conc_Inicial": [0.1, 0.05, 0.025, 0.0125],
                "Vol_Aliquota": [10.0, 10.0, 10.0, 10.0],
                "Vol_Gasto": [8.5, 3.8, 1.6, 0.6],
            }
        )

    df_editado_iso = st.data_editor(
        st.session_state.df_iso, num_rows="dynamic", key="editor_iso", width="stretch"
    )

    if st.button("Processar Dados", type="primary"):
        with st.spinner("Modelando isoterma..."):
            analise = IsotermaAdsorcao(
                df_editado_iso, massa_molar, conc_titulante, fator_esteq
            )
            df_resultados = analise.process_data()

            if analise.linhas_vazias > 0:
                st.warning(f"{analise.linhas_vazias} linha(s) vazia(s) ignorada(s).")

            if analise.linhas_descartadas > 0:
                st.warning(
                    f"Atenção: {analise.linhas_descartadas} linha(s) descartada(s) por valores inválidos ou erros físicos de bancada."
                )

            if not df_resultados.empty:
                parametros = analise.fit_model(modelo_escolhido)
                if "erro" in parametros:
                    st.error(f"Erro no ajuste: {parametros['erro']}")
                else:
                    grafico = analise.plot_graph(modelo_escolhido)
                    st.success(
                        f"Análise concluída usando o modelo de **{modelo_escolhido}**!"
                    )
                    utils.renderizar_resultados(
                        modulo,
                        parametros,
                        grafico,
                        df_resultados,
                        "isotermas_resultados.csv",
                        modelo_escolhido,
                    )
            else:
                st.error(
                    "Erro: Preencha a tabela com valores experimentais válidos. Nenhuma linha restou após os filtros de consistência."
                )


# MÓDULO 2: ARRHENIUS

elif modulo == "Cinética (Arrhenius)":
    st.header("Dependência da Velocidade com a Temperatura")
    st.subheader("Tabela de Dados Experimentais")

    if "df_arr" not in st.session_state:
        st.session_state.df_arr = pd.DataFrame(
            {
                "Tubo": [1, 2, 3, 4],
                "Temperatura (K)": [298.0, 308.0, 318.0, 328.0],
                "Tempo (s)": [125.0, 64.0, 33.0, 17.0],
            }
        )

    df_editado_arr = st.data_editor(
        st.session_state.df_arr, num_rows="dynamic", key="editor_arr", width="stretch"
    )

    if st.button("Processar Dados", type="primary"):
        with st.spinner("Ajustando dependência térmica..."):
            if (df_editado_arr["Temperatura (K)"] <= 0).any() or (
                df_editado_arr["Tempo (s)"] <= 0
            ).any():
                st.error(
                    "Erro: Temperaturas e Tempos devem ser estritamente maiores que zero."
                )
                st.stop()

            analise = CineticaArrhenius(df_editado_arr)
            df_resultados = analise.process_data()

            if analise.linhas_vazias > 0:
                st.warning(f"{analise.linhas_vazias} linha(s) vazia(s) ignorada(s).")

            if analise.linhas_descartadas > 0:
                st.warning(
                    f"Atenção: {analise.linhas_descartadas} linha(s) descartada(s)."
                )

            if not df_resultados.empty:
                parametros = analise.fit_model()
                if "erro" in parametros:
                    st.error(f"Erro no ajuste: {parametros['erro']}")
                else:
                    grafico = analise.plot_graph()
                    st.success("Análise de Arrhenius concluída!")
                    utils.renderizar_resultados(
                        modulo,
                        parametros,
                        grafico,
                        df_resultados,
                        "arrhenius_resultados.csv",
                    )
            else:
                st.error("Nenhuma linha restou após a filtragem.")


# MÓDULO 3: ORDEM DE REAÇÃO (Não-Linear)

elif modulo == "Ordem de Reação":
    st.header("Determinação da Ordem")
    st.subheader("Tabela de Dados Experimentais")

    if "df_ord" not in st.session_state:
        st.session_state.df_ord = pd.DataFrame(
            {
                "Titulação": [1, 2, 3, 4, 5],
                "Tempo (s)": [20.0, 40.0, 60.0, 80.0, 100.0],
                "[H2O2] (mol/L)": [0.082, 0.067, 0.055, 0.045, 0.037],
            }
        )

    df_editado_ord = st.data_editor(
        st.session_state.df_ord, num_rows="dynamic", key="editor_ord", width="stretch"
    )

    if st.button("Processar Dados", type="primary"):
        with st.spinner("Convergindo regressões não-lineares..."):
            analise = OrdemReacao(df_editado_ord)
            df_resultados = analise.process_data()

            if analise.linhas_vazias > 0:
                st.warning(f"{analise.linhas_vazias} linha(s) vazia(s) ignorada(s).")

            if analise.linhas_descartadas > 0:
                st.warning(
                    f"Atenção: {analise.linhas_descartadas} linha(s) descartada(s)."
                )

            if not df_resultados.empty:
                parametros = analise.fit_model()
                if "erro" in parametros:
                    st.error(f"Falha no ajuste das curvas: {parametros['erro']}")
                else:
                    grafico = analise.plot_graph()
                    st.success(
                        f"De acordo com o MSE na escala real, a reação é de **{parametros.get('best_fit')}**."
                    )
                    utils.renderizar_resultados(
                        modulo,
                        parametros,
                        grafico,
                        df_resultados,
                        "ordem_reacao_resultados.csv",
                    )
            else:
                st.error(
                    "Erro: Verifique se os dados são válidos. Nenhuma linha restou."
                )
