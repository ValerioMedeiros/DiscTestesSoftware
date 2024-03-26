import unittest
from sistema_acesso_db import registrar_acesso, registrar_veiculo, consultar_acessos, consultar_veiculos
from sqlalchemy import create_engine, MetaData, Table
from datetime import datetime

class TestSistemaAcessoDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Conecta ao banco de teste
        cls.engine = create_engine('sqlite:///test_meubanco.sqlite')
        cls.metadata = MetaData(bind=cls.engine)
        cls.metadata.reflect(bind=cls.engine)

        # Usa as mesmas tabelas, mas vinculadas ao banco de teste
        cls.acessos = Table('acessos', cls.metadata, autoload_with=cls.engine)
        cls.veiculos = Table('veiculos', cls.metadata, autoload_with=cls.engine)

    def setUp(self):
        # Inicia cada teste com um banco de dados limpo
        self.metadata.drop_all(self.engine)
        self.metadata.create_all(self.engine)

    def test_registrar_acesso(self):
        nome_pessoa = "Teste Pessoa"
        registrar_acesso(nome_pessoa)
        acessos_df = consultar_acessos()
        self.assertEqual(len(acessos_df), 1)
        self.assertEqual(acessos_df.iloc[0]['pessoa'], nome_pessoa)

    def test_registrar_veiculo_entrada(self):
        placa_veiculo = "ABC-1234"
        registrar_veiculo(placa_veiculo, entrada=True)
        veiculos_df = consultar_veiculos()
        self.assertEqual(len(veiculos_df), 1)
        self.assertEqual(veiculos_df.iloc[0]['veiculo_placa'], placa_veiculo)
        self.assertIsNotNone(veiculos_df.iloc[0]['data_veiculo_entrada'])

    def test_registrar_veiculo_saida(self):
        placa_veiculo = "ABC-1234"
        registrar_veiculo(placa_veiculo, entrada=True)
        registrar_veiculo(placa_veiculo, entrada=False)
        veiculos_df = consultar_veiculos()
        self.assertEqual(len(veiculos_df), 1)
        self.assertIsNotNone(veiculos_df.iloc[0]['data_veiculo_saida'])

if __name__ == '__main__':
    unittest.main()
