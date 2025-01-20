"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import re

api = Blueprint('api', __name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
MSG_MISSING_DATA = "Todos los datos son necesarios"
MSG_INVALID_DATA = "Datos inválidos"
MSG_EMAIL_EXISTS = "El correo ya existe!"
MSG_SUCCESS = "Usuario registrado exitosamente"

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the Google Inspector to see the GET request."
    }
    return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def login_user():
    identifier = request.json.get('identifier', None)
    password = request.json.get('password', None)

    if not identifier or not password:
        return jsonify({"msg": MSG_MISSING_DATA}), 400

    try:
        user = User.query.filter(
            (User.email == identifier) | (User.user == identifier)
        ).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"msg": "Credenciales inválidas"}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({
            "msg": "Inicio de sesión exitoso",
            "token": token,
            "user_id": user.id
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Error de base de datos", "error": str(e)}), 500


@api.route('/register', methods=['POST'])
def register():
    user = request.json.get('user', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not user or not email or not password:
        return jsonify({"msg": MSG_MISSING_DATA}), 400

    if not isinstance(user, str) or not isinstance(email, str) or not isinstance(password, str) or not EMAIL_REGEX.match(email):
        return jsonify({"msg": MSG_INVALID_DATA}), 400

    existing_user = User.query.filter(
        (User.email == email) | (User.user == user)
    ).first()
    if existing_user:
        return jsonify({"msg": MSG_EMAIL_EXISTS}), 409

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(user=user, email=email, password=hashed_password, is_active=True)
        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=str(new_user.id))
        return jsonify({"msg": MSG_SUCCESS, "token": token}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@api.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({"msg": "No se encontraron usuarios"}), 404

        users_serialized = [user.serialize() for user in users]
        return jsonify({
            "msg": "Usuarios obtenidos correctamente",
            "payload": users_serialized
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Error al obtener los usuarios", "error": str(e)}), 500


@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404

        return jsonify({
            "msg": "Usuario obtenido correctamente",
            "payload": user.serialize()
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Error al obtener el usuario", "error": str(e)}), 500


@api.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    username = data.get("user")
    if username:
        user.user = username

    email = data.get("email")
    if email:
        if not EMAIL_REGEX.match(email):
            return jsonify({"error": "Formato de correo inválido"}), 400
        user.email = email

    password = data.get("password")
    if password:
        user.password = generate_password_hash(password)

    is_active = data.get("is_active")
    if is_active is not None:
        user.is_active = is_active

    try:
        db.session.commit()
        return jsonify({
            "msg": "Usuario actualizado correctamente",
            "user": user.serialize()
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error de base de datos", "details": str(e)}), 500


@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": f"Usuario {user.user} eliminado exitosamente"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": "Error al eliminar el usuario", "error": str(e)}), 500
