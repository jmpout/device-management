"""
jwt.py
- creates the JWT manager and processes each request before being consumed by the endpoints
in the api.py file.
"""
from flask import jsonify
from flask_jwt_extended import JWTManager


jwt = JWTManager()
blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """Checks if a token has been blacklisted and will be called automatically when
    JWT_BLACKLIST_ENABLED is true. We add the token's unique identifier (jti) to the blacklist."""
    return jwt_payload["jti"] in blacklist


@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    """Checks if a token has been revoked."""
    return (
        jsonify({"message": "The token has been revoked.", "error": "token_revoked"}),
        401,
    )


# The following callbacks are used for customizing jwt response/error messages.
@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    """Checks if a token has expired."""
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token(message):
    """Checks if a token is invalid."""
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token(message):
    """Checks if a token is missing."""
    return (
        jsonify(
            {
                "message": "Request does not contain a token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh(jwt_header, jwt_payload):
    """Checks if a token is not fresh."""
    return (
        jsonify(
            {"message": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )
