from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios' # Nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    
    # Fundamental para a criptografia assimétrica de saques
    chave_publica = db.Column(db.Text, nullable=True) 
    
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class Amizade(db.Model):
    __tablename__ = 'amizades'
    id = db.Column(db.Integer, primary_key=True)
    remetente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    status = db.Column(db.String(20), default='pendente') # pendente, aceito, recusado
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    visualizada = db.Column(db.Boolean, default=False)
    # Relacionamentos para facilitar a busca de nomes depois
    remetente = db.relationship('Usuario', foreign_keys=[remetente_id])
    destinatario = db.relationship('Usuario', foreign_keys=[destinatario_id])

class Amigo(db.Model):
    __tablename__ = "meus_amigos"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    id_amigo = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nossa_sala = db.Column(db.String(45))
    dados_amigo = db.relationship("Usuario", foreign_keys=[id_amigo])
    dados_usuario = db.relationship("Usuario", foreign_keys=[id_usuario])

class Menssagens(db.Model):
    __tablename__ = "menssagens"
    id = db.Column(db.Integer , primary_key = True)
    id_remitente = db.Column (db.Integer , db.ForeignKey("usuarios.id") , nullable = False)
    id_destinatario = db.Column (db.Integer , db.ForeignKey("usuarios.id") , nullable = False)
    nome_remitente = db.Column(db.String(100) , nullable = False)
    nome_destinatario = db.Column(db.String(100) , nullable = False)
    nossa_sala = db.Column(db.String(100), nullable=False, index=True)
    lida = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.String(100))
    data_envio = db.Column(db.Text, default = "")
    menssagem = db.Column(db.Text, nullable=False)
    dados_remitente = db.relationship("Usuario" , foreign_keys = [id_remitente])
    dados_destinatario = db.relationship("Usuario" , foreign_keys = [id_destinatario])

class Registrar_produto(db.Model):
    __tablename__ = "Produto_usuario"
    id = db.Column(db.Integer , primary_key = True)
    nome_produto = db.Column(db.String(100), nullable = False)
    descricao_produto = db.Column(db.Text , nullable = False)
    tipo_produto = db.Column(db.Text , nullable = False)
    preco_produto = db.Column(db.Text , nullable = False)
    url_imagem_produto = db.Column(db.Text , nullable = False)
    id_usuario = db.Column(db.Integer , db.ForeignKey("usuarios.id") , nullable = False)
    dados_usuario = db.relationship("Usuario" , foreign_keys = [id_usuario])





