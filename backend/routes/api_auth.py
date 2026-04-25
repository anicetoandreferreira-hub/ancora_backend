from flask import Blueprint, request, jsonify, make_response
from service.auth_service import AuthService
import os
import jwt
from datetime import datetime, timedelta

login_bp = Blueprint("login", __name__)

@login_bp.route("/Login", methods=["POST"])
def Login():
    try:
        dados = request.get_json()
        telefone = dados.get("telefone")
        senha = dados.get("senha")
        
        resultado = AuthService.validar_login(telefone, senha)
        
        if not resultado:
            return jsonify({"menssagem": "Telefone ou senha inválidos", "status": "False"}), 401
        
        usuario = resultado["usuario"]
        user_id = usuario["id"]
        
        # Access token: 15min
        access_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],  # USA TELEFONE
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        access_token = jwt.encode(access_payload, os.getenv('SECRET_KEY'), algorithm="HS256")
        
        # Refresh token: 7 dias
        refresh_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],  # USA TELEFONE
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        refresh_token = jwt.encode(refresh_payload, os.getenv('SECRET_KEY'), algorithm="HS256")
        
        resp = make_response(jsonify({
            "status": "True",
            "menssagem": "usuario logado!",
            "id": usuario["id"],
            "nome": usuario["nome"],
            "telefone": usuario["telefone"]
        }))
        
        resp.set_cookie(
            "token_sessao",
            value=access_token,
            max_age=60*15,
            httponly=True,
            secure=True,
            samesite="Lax",
            path='/'
        )
        
        resp.set_cookie(
            "refresh_token",
            value=refresh_token,
            max_age=60*60*24*7,
            httponly=True,
            secure=False,
            samesite="Lax",
            path='/'
        )
        return resp
        
    except Exception as erro:
        print(f"Erro no login: {erro}")
        return jsonify({"status": "False", "menssagem": "Erro interno"}), 500

@login_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get('refresh_token')
    
    if not refresh_token:
        print("❌ Refresh: cookie não chegou")
        return jsonify({"erro": "Sem refresh token"}), 401
    
    try:
        payload = jwt.decode(refresh_token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        
        if payload.get("type") != "refresh":
            return jsonify({"erro": "Token inválido"}), 401
            
        # Gera novo access token usando dados do refresh
        novo_access = jwt.encode({
            "id": payload["id"],
            "nome": payload["nome"],
            "telefone": payload["telefone"],  # USA TELEFONE
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }, os.getenv('SECRET_KEY'), algorithm="HS256")
        
        resp = jsonify({"mensagem": "Token renovado"})
        resp.set_cookie(
            "token_sessao",
            novo_access,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=15*60,
            path="/"
        )
        print(f"✅ Refresh OK para user {payload['id']}")
        return resp, 200
        
    except jwt.ExpiredSignatureError:
        print("❌ Refresh: token expirado")
        return jsonify({"erro": "Refresh expirado"}), 401
    except Exception as e:
        print(f"❌ Refresh erro: {e}")
        return jsonify({"erro": "Token inválido"}), 401