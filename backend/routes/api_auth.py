from flask import Blueprint, request, jsonify, make_response
from service.auth_service import AuthService
import os
import jwt
from datetime import datetime, timedelta

login_bp = Blueprint("login", __name__)

# ===========================
# 🔐 LOGIN
# ===========================
@login_bp.route("/Login", methods=["POST"])
def Login():
    try:
        dados = request.get_json()
        telefone = dados.get("telefone")
        senha = dados.get("senha")

        resultado = AuthService.validar_login(telefone, senha)

        if not resultado:
            return jsonify({
                "menssagem": "Telefone ou senha inválidos",
                "status": "False"
            }), 401

        usuario = resultado["usuario"]
        user_id = usuario["id"]

        # 🔥 ACCESS TOKEN
        access_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }

        access_token = jwt.encode(
            access_payload,
            os.getenv('SECRET_KEY'),
            algorithm="HS256"
        )

        # 🔥 REFRESH TOKEN
        refresh_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        refresh_token = jwt.encode(
            refresh_payload,
            os.getenv('SECRET_KEY'),
            algorithm="HS256"
        )

        resp = make_response(jsonify({
            "status": "True",
            "menssagem": "usuario logado!",
            "id": usuario["id"],
            "nome": usuario["nome"],
            "telefone": usuario["telefone"]
        }))

        # ===========================
        # 🍪 COOKIE FIX (CRÍTICO PARA NETLIFY + RENDER + SOCKET)
        # ===========================

        resp.set_cookie(
            "token_sessao",
            value=access_token,
            max_age=60 * 15,
            httponly=True,
            secure=True,        # HTTPS obrigatório no Render
            samesite="None",    # 🔥 ESSENCIAL para cross-domain
            path="/"
        )

        resp.set_cookie(
            "refresh_token",
            value=refresh_token,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            secure=True,
            samesite="None",    # 🔥 ESSENCIAL
            path="/"
        )

        return resp

    except Exception as erro:
        print(f"Erro no login: {erro}")
        return jsonify({
            "status": "False",
            "menssagem": "Erro interno"
        }), 500


# ===========================
# 🔄 REFRESH TOKEN
# ===========================
@login_bp.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        print("❌ Sem refresh token recebido")
        return jsonify({"erro": "Sem refresh token"}), 401

    try:
        payload = jwt.decode(
            refresh_token,
            os.getenv('SECRET_KEY'),
            algorithms=["HS256"]
        )

        if payload.get("type") != "refresh":
            return jsonify({"erro": "Token inválido"}), 401

        # 🔥 NOVO ACCESS TOKEN
        novo_access = jwt.encode({
            "id": payload["id"],
            "nome": payload["nome"],
            "telefone": payload["telefone"],
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }, os.getenv('SECRET_KEY'), algorithm="HS256")

        resp = jsonify({"mensagem": "Token renovado"})

        # ===========================
        # 🍪 REFRESH DO COOKIE
        # ===========================
        resp.set_cookie(
            "token_sessao",
            novo_access,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=15 * 60,
            path="/"
        )

        return resp, 200

    except jwt.ExpiredSignatureError:
        print("❌ Refresh expirado")
        return jsonify({"erro": "Refresh expirado"}), 401

    except Exception as e:
        print(f"Erro refresh: {e}")
        return jsonify({"erro": "Token inválido"}), 401
