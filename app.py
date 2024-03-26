import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime

# Cria conexão com o banco de dados SQLite
engine = create_engine('sqlite:///meubanco.sqlite')
metadata = MetaData()

# Definição das tabelas
acessos = Table('acessos', metadata,
                Column('id', Integer, primary_key=True),
                Column('pessoa', String),
                Column('data_acesso', DateTime))

veiculos = Table('veiculos', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('veiculo_placa', String),
                 Column('data_veiculo_entrada', DateTime, nullable=True),
                 Column('data_veiculo_saida', DateTime, nullable=True))

# Cria as tabelas no banco de dados, se não existirem
metadata.create_all(engine)

st.title('Sistema de Controle e Análise de Acesso')

# Sidebar para navegação
opcao = st.sidebar.selectbox(
    "Escolha a opção desejada",
    ("Registrar Acesso", "Controle de Veículos", "Análise de Acessos")
)

def registrar_acesso(pessoa):
    conn = engine.connect()
    ins = acessos.insert().values(pessoa=pessoa, data_acesso=datetime.now())
    conn.execute(ins)
    conn.close()

def registrar_veiculo(placa, entrada=True):
    conn = engine.connect()
    if entrada:
        ins = veiculos.insert().values(veiculo_placa=placa, data_veiculo_entrada=datetime.now())
    else:
        update = veiculos.update().where(veiculos.c.veiculo_placa==placa).values(data_veiculo_saida=datetime.now())
        conn.execute(update)
        return
    conn.execute(ins)
    conn.close()

def consultar_acessos():
    conn = engine.connect()
    sel = acessos.select()
    result = conn.execute(sel)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    conn.close()
    return df

def consultar_veiculos():
    conn = engine.connect()
    sel = veiculos.select()
    result = conn.execute(sel)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    conn.close()
    return df

if opcao == "Registrar Acesso":
    st.header("Registro de Acesso de Pessoa")
    nome_pessoa = st.text_input("Nome da Pessoa", "Digite aqui...")
    if st.button("Registrar Acesso"):
        registrar_acesso(nome_pessoa)
        st.success(f"Acesso registrado para {nome_pessoa}")

elif opcao == "Controle de Veículos":
    st.header("Controle de Entrada e Saída de Veículos")
    placa_veiculo = st.text_input("Placa do Veículo", "Digite aqui...")
    entrada_ou_saida = st.radio("Registro de", ("Entrada", "Saída"))
    if st.button("Registrar"):
        registrar_veiculo(placa_veiculo, entrada=entrada_ou_saida=="Entrada")
        if entrada_ou_saida == "Entrada":
            st.success(f"Entrada do veículo {placa_veiculo} registrada.")
        else:
            st.success(f"Saída do veículo {placa_veiculo} registrada.")

elif opcao == "Análise de Acessos":
    st.header("Análise de Acessos Registrados")
    acessos_df = consultar_acessos()
    veiculos_df = consultar_veiculos()
    st.write("Acessos de Pessoas", acessos_df)
    st.write("Controle de Veículos", veiculos_df)
