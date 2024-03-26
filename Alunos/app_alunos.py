# Importações
from unittest import TestCase
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base de dados
Base = declarative_base()

# Configuração da engine do SQLAlchemy
engine = create_engine('sqlite:///alunos.db')

# Classe Aluno
class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    matricula = Column(String(255))

# Funções CRUD
def criar_aluno(nome, matricula):
    # Criar uma nova sessão
    session = sessionmaker(bind=engine)()

    # Criar um novo objeto Aluno
    aluno = Aluno(nome=nome, matricula=matricula)

    # Adicionar o aluno à sessão
    session.add(aluno)

    # Commitar as alterações
    session.commit()

    # Fechar a sessão
    session.close()

def buscar_aluno(matricula):
    # Criar uma nova sessão
    session = sessionmaker(bind=engine)()

    # Buscar o aluno por matrícula
    aluno = session.query(Aluno).filter(Aluno.matricula == matricula).first()

    # Fechar a sessão
    session.close()

    return aluno

def atualizar_aluno(aluno):
    # Criar uma nova sessão
    session = sessionmaker(bind=engine)()

    # Atualizar os dados do aluno
    session.merge(aluno)

    # Commitar as alterações
    session.commit()

    # Fechar a sessão
    session.close()

def deletar_aluno(matricula):
    # Criar uma nova sessão
    session = sessionmaker(bind=engine)()

    # Buscar o aluno por matrícula
    aluno = session.query(Aluno).filter(Aluno.matricula == matricula).first()

    # Deletar o aluno da sessão
    session.delete(aluno)

    # Commitar as alterações
    session.commit()

    # Fechar a sessão
    session.close()

# Testes
class TestAluno(TestCase):
    def test_criar_aluno(self):
        aluno = criar_aluno("João Silva", "123456")
        self.assertEqual(aluno.nome, "João Silva")
        self.assertEqual(aluno.matricula, "123456")

        aluno_encontrado = buscar_aluno("123456")
        self.assertEqual(aluno_encontrado.nome, "João Silva")

    def test_atualizar_aluno(self):
        aluno = criar_aluno("Maria Oliveira", "789012")
        aluno.nome = "Maria Oliveira Santos"
        atualizar_aluno(aluno)

        aluno_encontrado = buscar_aluno("789012")
        self.assertEqual(aluno_encontrado.nome, "Maria Oliveira Santos")

    def test_deletar_aluno(self):
        criar_aluno("José Souza", "456789")
        deletar_aluno("456789")

        aluno_encontrado = buscar_aluno("456789")
        self.assertEqual(aluno_encontrado, None)

# Exemplo de uso
aluno = criar_aluno("Ana Costa", "987654")
aluno_encontrado = buscar_aluno("987654")

print(f"Aluno encontrado: {aluno_encontrado.nome}")

aluno.nome = "Ana Costa Pereira"
atualizar_aluno(aluno)

deletar_aluno("987654")



# Criar as tabelas do banco de dados
Base.metadata.create_all(engine)
