import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar dados de tratamentos
@st.cache_data
def load_treatment_data():
    try:
        data = pd.read_csv('.github/dados_bezerras_pre_registrados.csv', delimiter=";")
        st.write("Dados de tratamentos carregados com sucesso.")
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Propriedade", "Brinco da Bezerra", "Razão do Tratamento", "Tipo de Medicamento", "Nome do Medicamento", "Dose", "Data da 1ª Dose", "Nº de Doses", "Responsável"])
        st.write("Arquivo de tratamentos não encontrado, criando novo DataFrame.")
    except Exception as e:
        st.write(f"Erro ao carregar os dados de tratamentos: {e}")
        data = pd.DataFrame(columns=["Propriedade", "Brinco da Bezerra", "Razão do Tratamento", "Tipo de Medicamento", "Nome do Medicamento", "Dose", "Data da 1ª Dose", "Nº de Doses", "Responsável"])
    return data

# Função para salvar dados de tratamentos
def save_treatment_data(data):
    try:
        data.to_csv('.github/dados_bezerras_pre_registrados.csv', index=False, sep=';')
        st.write("Dados de tratamentos salvos com sucesso.")
    except Exception as e:
        st.write(f"Erro ao salvar os dados de tratamentos: {e}")

# Função para carregar dados de cadastro de bezerras
@st.cache_data
def load_bezerra_data():
    try:
        data = pd.read_csv('.github/Cadastro_de_bezerra.csv', delimiter=";")
        st.write("Dados de cadastro de bezerras carregados com sucesso.")
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Propriedade", "Brinco", "Nascimento", "Brinco mãe", "Peso", "Altura", "Vol. Colostro", "Brix"])
        st.write("Arquivo de cadastro de bezerras não encontrado, criando novo DataFrame.")
    except Exception as e:
        st.write(f"Erro ao carregar os dados de cadastro de bezerras: {e}")
        data = pd.DataFrame(columns=["Propriedade", "Brinco", "Nascimento", "Brinco mãe", "Peso", "Altura", "Vol. Colostro", "Brix"])
    return data

# Função para salvar dados de cadastro de bezerras
def save_bezerra_data(data):
    try:
        data.to_csv('.github/Cadastro_de_bezerra.csv', index=False, sep=';')
        st.write("Dados de cadastro de bezerras salvos com sucesso.")
    except Exception as e:
        st.write(f"Erro ao salvar os dados de cadastro de bezerras: {e}")

# Carregar dados
treatment_data = load_treatment_data()
bezerra_data = load_bezerra_data()

# Navegação por páginas
st.sidebar.title("Menu de Navegação")
page = st.sidebar.radio("Ir para", ["Cadastro de Tratamento", "Cadastro de Bezerra", "Tabela de Dados", "Gráficos", "Linha do Tempo"])

if page == "Cadastro de Tratamento":
    st.title("Cadastro de Tratamentos de Bezerras")
    
    # Formulário para adicionar novos dados de tratamento
    st.header("Adicionar Novo Tratamento")
    with st.form("Adicionar Tratamento"):
        propriedade = st.text_input("Propriedade")
        brinco = st.text_input("Brinco da Bezerra")
        razao = st.text_input("Razão do Tratamento")
        tipo_medicamento = st.text_input("Tipo de Medicamento")
        medicamento = st.text_input("Nome do Medicamento")
        dose = st.text_input("Dose")
        data_primeira_dose = st.date_input("Data da 1ª Dose")
        n_doses = st.number_input("Nº de Doses", min_value=1, step=1)
        responsavel = st.text_input("Responsável")
        submit = st.form_submit_button("Adicionar")

        if submit:
            new_data = pd.DataFrame({
                "Propriedade": [propriedade],
                "Brinco da Bezerra": [brinco],
                "Razão do Tratamento": [razao],
                "Tipo de Medicamento": [tipo_medicamento],
                "Nome do Medicamento": [medicamento],
                "Dose": [dose],
                "Data da 1ª Dose": [data_primeira_dose.strftime('%d/%m/%Y')],
                "Nº de Doses": [n_doses],
                "Responsável": [responsavel]
            })
            st.write("Dados do novo tratamento:")
            st.write(new_data)
            treatment_data = pd.concat([treatment_data, new_data], ignore_index=True)
            st.write("Dados de tratamentos após concatenação:")
            st.write(treatment_data)
            save_treatment_data(treatment_data)
            st.success("Dados de tratamento adicionados com sucesso!")

elif page == "Cadastro de Bezerra":
    st.title("Cadastro de Bezerra")
    
    # Formulário para adicionar novas bezerras
    st.header("Adicionar Nova Bezerra")
    with st.form("Adicionar Bezerra"):
        propriedade = st.text_input("Propriedade")
        brinco = st.text_input("Brinco")
        nascimento = st.date_input("Nascimento")
        brinco_mae = st.text_input("Brinco mãe")
        peso = st.number_input("Peso", min_value=0.0, step=0.1)
        altura = st.number_input("Altura", min_value=0.0, step=0.1)
        vol_colostro = st.number_input("Vol. Colostro", min_value=0.0, step=0.1)
        brix = st.number_input("Brix", min_value=0.0, step=0.1)
        submit = st.form_submit_button("Adicionar")

        if submit:
            new_bezerra = pd.DataFrame({
                "Propriedade": [propriedade],
                "Brinco": [brinco],
                "Nascimento": [nascimento.strftime('%d/%m/%Y')],
                "Brinco mãe": [brinco_mae],
                "Peso": [peso],
                "Altura": [altura],
                "Vol. Colostro": [vol_colostro],
                "Brix": [brix]
            })
            st.write("Dados da nova bezerra:")
            st.write(new_bezerra)
            bezerra_data = pd.concat([bezerra_data, new_bezerra], ignore_index=True)
            st.write("Dados de bezerras após concatenação:")
            st.write(bezerra_data)
            save_bezerra_data(bezerra_data)
            st.success("Dados de bezerra adicionados com sucesso!")

elif page == "Tabela de Dados":
    st.title("Tabela de Dados de Tratamentos de Bezerras")

    # Exibir e filtrar dados de tratamentos
    st.header("Consultar Dados de Tratamentos")
    filter_propriedade = st.selectbox("Filtrar por Propriedade", options=["Todas"] + list(treatment_data["Propriedade"].unique()))
    filtered_treatment_data = treatment_data if filter_propriedade == "Todas" else treatment_data[treatment_data["Propriedade"] == filter_propriedade]
    st.dataframe(filtered_treatment_data)

    if st.button("Atualizar"):
        treatment_data = load_treatment_data()
        st.experimental_rerun()

    st.title("Tabela de Dados de Cadastro de Bezerras")

    # Exibir e filtrar dados de bezerras
    st.header("Consultar Dados de Bezerras")
    filter_bezerra_propriedade = st.selectbox("Filtrar por Propriedade (Bezerras)", options=["Todas"] + list(bezerra_data["Propriedade"].unique()))
    filtered_bezerra_data = bezerra_data if filter_bezerra_propriedade == "Todas" else bezerra_data[bezerra_data["Propriedade"] == filter_bezerra_propriedade]
    st.dataframe(filtered_bezerra_data)

    if st.button("Atualizar Bezerras"):
        bezerra_data = load_bezerra_data()
        st.experimental_rerun()

elif page == "Gráficos":
    st.title("Gráficos de Tratamentos de Bezerras")

    st.header("Gráficos Interativos")

    # Número de Tratamentos por Propriedade
    st.subheader("Número de Tratamentos por Propriedade")
    chart_data = treatment_data.groupby("Propriedade").size().reset_index(name="Número de Tratamentos")
    st.bar_chart(chart_data.set_index("Propriedade"))

    # Distribuição de Tratamentos por Tipo (Razão do Tratamento)
    st.subheader("Distribuição de Tratamentos por Tipo")
    chart_data = treatment_data["Razão do Tratamento"].value_counts().reset_index()
    chart_data.columns = ["Razão do Tratamento", "Contagem"]
    st.bar_chart(chart_data.set_index("Razão do Tratamento"))

    # Tratamentos por Responsável
    st.subheader("Tratamentos por Responsável")
    chart_data = treatment_data["Responsável"].value_counts().reset_index()
    chart_data.columns = ["Responsável", "Contagem"]
    st.bar_chart(chart_data.set_index("Responsável"))

    # Número de Doses Administradas
    st.subheader("Número de Doses Administradas")
    chart_data = treatment_data["Nº de Doses"].value_counts().reset_index()
    chart_data.columns = ["Nº de Doses", "Contagem"]
    st.bar_chart(chart_data.set_index("Nº de Doses"))

    # Tratamentos ao Longo do Tempo
    st.subheader("Tratamentos ao Longo do Tempo")
    treatment_data["Data da 1ª Dose"] = pd.to_datetime(treatment_data["Data da 1ª Dose"], format='%d/%m/%Y')
    chart_data = treatment_data.groupby(treatment_data["Data da 1ª Dose"].dt.to_period("D")).size().reset_index(name="Número de Tratamentos")
    chart_data["Data da 1ª Dose"] = chart_data["Data da 1ª Dose"].dt.to_timestamp()
    st.line_chart(chart_data.set_index("Data da 1ª Dose"))

    # Mais gráficos podem ser adicionados conforme necessário

elif page == "Linha do Tempo":
    st.title("Linha do Tempo da Bezerra")

    # Formulário para buscar a linha do tempo da bezerra
    st.header("Buscar Linha do Tempo")
    bezerra_selecionada = st.multiselect("Selecione o(s) Brinco(s) da Bezerra", bezerra_data["Brinco"].unique())
    buscar = st.button("Buscar")

    if buscar and bezerra_selecionada:
        eventos = []
        for brinco_busca in bezerra_selecionada:
            # Filtrar dados de cadastro e tratamentos pela bezerra
            bezerra_info = bezerra_data[bezerra_data["Brinco"] == brinco_busca]
            tratamento_info = treatment_data[treatment_data["Brinco da Bezerra"] == brinco_busca]

            if not bezerra_info.empty:
                nascimento = pd.to_datetime(bezerra_info["Nascimento"].values[0], format='%d/%m/%Y')

                # Adicionar evento de nascimento
                eventos.append(dict(Task=f"{brinco_busca} - Nascimento", Start=nascimento, Finish=nascimento, Resource="Nascimento"))

                # Adicionar eventos de tratamentos
                for idx, row in tratamento_info.iterrows():
                    data_tratamento = pd.to_datetime(row["Data da 1ª Dose"], format='%d/%m/%Y')
                    eventos.append(dict(Task=f"{brinco_busca} - {row['Razão do Tratamento']}", Start=data_tratamento, Finish=data_tratamento, Resource="Tratamento"))

        # Criar DataFrame de eventos
        eventos_df = pd.DataFrame(eventos)

        # Plotar linha do tempo
        fig = px.timeline(eventos_df, x_start="Start", x_end="Finish", y="Task", color="Resource", title=f"Linha do Tempo das Bezerras Selecionadas")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig)
    elif buscar:
        st.write("Selecione pelo menos uma bezerra.")
