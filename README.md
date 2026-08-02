<div align="center">

# Físico-Química de Superfícies e Cinética

</div>

<div align="center">

 **Aplicação web em Python para modelagem matemática, regressão não-linear e tratamento estatístico de dados.
<br>Web app for Physical Chemistry data processing.** 

</div>

<div align="center">

<a href="#">![badge](https://img.shields.io/badge/Made_by-celedriel-262622?style=for-the-badge&logo=github&logoColor=262622&logoSize=auto&color=4CAF50) </a>
<a href="https://streamlit.io/">![badge](https://img.shields.io/badge/Platform-Streamlit-262622?style=for-the-badge&logo=streamlit&logoColor=262622&logoSize=auto&color=FF4B4B) </a>
<a href="https://www.python.org/">![badge](https://img.shields.io/badge/Code-Python-262622?style=for-the-badge&logo=python&logoColor=262622&logoSize=auto&color=3776AB) </a>
<a href="#">![GitHub last commit](https://img.shields.io/github/last-commit/celedriel/pchem-surfaces-kinetics?style=for-the-badge&logo=git&logoColor=262622&color=4CAF50)</a>

</div>

<br>

### Interface e Entrada de Dados / Data Entry

| Módulo 1: Isotermas de Adsorção | Módulo 2: Cinética (Arrhenius) |
| :---: | :---: |
| <img width="450" alt="isotermas" src="https://github.com/user-attachments/assets/94e52953-2910-4691-ba80-b382fd066df5" /> | <img width="450" alt="arrhenius" src="https://github.com/user-attachments/assets/601734f2-f8e7-4102-9f30-2bc1b2ee5b24" /> |

| Módulo 3: Ordem de Reação |
| :---: |
| <img width="900" alt="o reação" src="https://github.com/user-attachments/assets/a81975e0-11b0-471a-a6b4-3964107cbe45" /> |

### Resultados e Gráficos / Results and Graphs

| Isoterma de Langmuir | Isoterma de Freundlich |
| :---: | :---: |
| <img width="450" alt="Langmuirexemp" src="https://github.com/user-attachments/assets/45b8928d-2579-48d7-99f1-9bf4ae83abb5" /> | <img width="450" alt="Freundlichexemp" src="https://github.com/user-attachments/assets/eeb0d183-a7ba-4b24-90f3-f2a14b08f6a2" /> |

| Cinética (Arrhenius) | Ordem de Reação (1ª e 2ª Ordem) |
| :---: | :---: |
| <img width="450" alt="arrheniusexemp" src="https://github.com/user-attachments/assets/7365155e-1434-49cb-a919-d10cde97f94e" /> | <img width="450" alt="o reaçãoexemp1" src="https://github.com/user-attachments/assets/70835bb7-e709-48e3-aed1-8c7b20086173" /><br><br><img width="450" alt="o reaçãoexemp2" src="https://github.com/user-attachments/assets/9dcc5354-cb2c-49e9-8b4a-7f93cc889774" /> |

___

> [!TIP]
> **Módulos de Análise / Analysis Modules:** O aplicativo foi dividido em três grandes módulos matemáticos para facilitar o processamento dos dados experimentais brutos.
> 
> | **Isotermas de Adsorção:** | **Cinética (Arrhenius):** |
> | :--- | :--- |
> | Compara o R² entre os modelos de monocamada (Langmuir) e multicamadas (Freundlich). | Calcula a Energia de Ativação ($E_a$) e o Fator de Frequência ($\ln A$) da reação. |
> | **Ordem de Reação:** | **Tratamento Estatístico:** |
> | Determina automaticamente se a reação segue a 1ª ou a 2ª ordem com base no Erro Residual (SQE). | Gera matrizes de cálculo e regressões lineares utilizando a biblioteca SciPy. |

____

### instalação / Installation 

> [!NOTE]
> **English speakers:** Check the dropdown below for the translated step-by-step guide on how to run this application locally.

> [!WARNING]
> **Language Notice:** Please be aware that this application's interface, data tables, labels, and generated insights are built entirely in **Brazilian Portuguese (PT-BR)**

<details>
<summary><b>Click here for the English version</b></summary>
<br>

Follow the step-by-step guide below to run the dashboard on your machine:

**1. Open your terminal and clone this project to your local machine.**

```bash
   git clone [https://github.com/celedriel/pchem-surfaces-kinetics.git](https://github.com/celedriel/pchem-surfaces-kinetics.git)
```
**2. Navigate to the project directory.**

 ```Bash
cd pchem-surfaces-kinetics
```

**3. Install the required Python libraries using pip.**

```Bash
pip install -r requirements.txt
```

**4. Start the Streamlit server. The dashboard will automatically open in your default web browser.**

```Bash
streamlit run app.py
```

<hr>
</details>
<br>

Siga o passo a passo abaixo para rodar o painel de Físico-Química no seu pc:

**1. Abra o seu terminal e clone este projeto para o seu computador.**

```Bash
git clone [https://github.com/celedriel/pchem-surfaces-kinetics.git](https://github.com/celedriel/pchem-surfaces-kinetics.git)
```
**2. Navegue até o diretório do projeto.**

```Bash
cd PChem-surfaces-kinetics
```

**3. Instale as bibliotecas necessárias do Python utilizando o pip.**

```Bash
pip install -r requirements.txt
```

**4. Rode o servidor do Streamlit. O painel abrirá automaticamente no seu navegador padrão.**

```Bash
streamlit run app.py
```






   
