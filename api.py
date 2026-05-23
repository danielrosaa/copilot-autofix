import sqlite3
import os
import subprocess
import ipaddress
from flask import Flask, request, make_response, escape

app = Flask(__name__)


def autenticar_usuario(username, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    query = (
        f"SELECT * FROM users WHERE username = '{username}' AND password '{password}'"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result is not None


@app.route("/ping")
def ping():
    ip = request.args.get("ip", "").strip()
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return make_response("Invalid IP address", 400)

    result = subprocess.run(
        ["ping", "-c", "1", ip],
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return f"<pre>{output}</pre>"


@app.route("/debug")
def debug():
    return f"SECRET_KEY={os.environ.get('SECRET_KEY')}"


@app.route("/comente")
def comente():
    comentario = request.args.get("comentario", "")
    comentario_escaped = escape(comentario)
    return f"<h1>Comentário recebido:</h1><p>{comentario_escaped}</p>"


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "").strip().lower() in ("1", "true", "yes")
    app.run(debug=debug_mode)
