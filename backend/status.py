from flask import jsonify


def error(**kwargs):
    return jsonify({"is_ok": False, **kwargs})


def success(**kwargs):
    return jsonify({"is_ok": True, **kwargs})