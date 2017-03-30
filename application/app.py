from flask import request, jsonify, g
from .models import User
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, auth_required, verify_token


@app.route("/api/user", methods=["GET"])
@auth_required
def get_user():
    return jsonify(result=g.current_user)


@app.route("/api/users", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    ), 201


@app.route("/api/token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_credentials(
        incoming["email"], incoming["password"]
    )
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403
