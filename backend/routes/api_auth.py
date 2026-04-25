from flask import Blueprint, request, jsonify, make_response
from service.auth_service import AuthService
import os
import jwt
from datetime import datetime, timedelta

login_bp = Blueprint("login", __name__)

FRONTEND_URL = "https://ancora-oficial-ao.netlify.app"

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

        # =========================
        # ACCESS TOKEN
        # =========================
        access_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }

        access_token = jwt.encode(
            access_payload,
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        # =========================
        # REFRESH TOKEN
        # =========================
        refresh_payload = {
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"],
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        }

        refresh_token = jwt.encode(
            refresh_payload,
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        resp = make_response(jsonify({
            "status": "True",
            "menssagem": "usuario logado!",
            "id": user_id,
            "nome": usuario["nome"],
            "telefone": usuario["telefone"]
        }))

        # =========================
        # 🔥 COOKIE ACCESS (FIXED)
        # =========================
        resp.set_cookie(
            "token_sessao",
            access_token,
            max_age=60 * 15,
            httponly=True,
            secure=True,        # obrigatório em HTTPS (Render)
            samesite="None",    # 🔥 CRÍTICO para Netlify ↔ Render
            path="/"
        )

        # =========================
        # 🔥 COOKIE REFRESH (FIXED)
        # =========================
        resp.set_cookie(
            "refresh_token",
            refresh_token,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            secure=True,        # 🔥 TEM QUE SER TRUE também
            samesite="None",    # 🔥 CRÍTICO
            path="/"
        )

        return resp

    except Exception as erro:
        print(f"Erro no login: {erro}")
        return jsonify({
            "status": "False",
            "menssagem": "Erro interno"
        }), 500
