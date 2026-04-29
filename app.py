import sqlite3
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('gamestore.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)')
    c.execute('DELETE FROM users')
    c.execute("INSERT INTO users VALUES ('admin@gamestore.com', 'admin123')")
    conn.commit()
    conn.close()

init_db()

JOGOS = [
    {"capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/1593500/header.jpg", "titulo": "God of War", "preco": "R$ 199,90"},
    {"capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/1888930/header.jpg", "titulo": "The Last of Us Part I", "preco": "R$ 249,90"},
    {"capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg", "titulo": "Cyberpunk 2077", "preco": "R$ 199,90"},
    {"capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/2669320/header.jpg", "titulo": "EA SPORTS FC™ 25", "preco": "R$ 299,00"},
    {"capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg", "titulo": "Red Dead Redemption 2", "preco": "R$ 299,90"},
    {"capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg", "titulo": "The Witcher 3: Wild Hunt", "preco": "R$ 139,90"}
]

TEMPLATE_BASE = """
<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GameStore</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #1a1a24; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar { background-color: #121218; border-bottom: 1px solid #2a2a35; }
        .navbar-brand { color: #ffffff !important; font-weight: bold; }
        .card-custom { background-color: #1a1a24; border: none; border-radius: 8px; }
        .form-control { background-color: #1a1a24; border: 1px solid #333344; color: #fff; }
        .form-control:focus { background-color: #1a1a24; color: #fff; border-color: #2ecc71; box-shadow: none; }
        .btn-green { background-color: #2ecc71; color: #121218; font-weight: bold; border: none; }
        .btn-green:hover { background-color: #27ae60; color: #121218; }
        .btn-outline-red { border: 1px solid #e74c3c; color: #e74c3c; background: transparent; }
        .btn-outline-red:hover { background-color: #e74c3c; color: #fff; }
        .btn-outline-yellow { border: 1px solid #f1c40f; color: #f1c40f; background: transparent; }
        .btn-outline-yellow:hover { background-color: #f1c40f; color: #121218; }
        .btn-outline-light-custom { border: 1px solid #ffffff; color: #ffffff; background: transparent; border-radius: 4px; padding: 5px 20px;}
        .btn-outline-light-custom:hover { background-color: #ffffff; color: #121218; }
        .table { color: #ffffff; --bs-table-bg: transparent; margin-bottom: 0; }
        .table th { border-bottom: 1px solid #333344; color: #888899; font-weight: 600; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; }
        .table td { border-bottom: 1px solid #2a2a35; vertical-align: middle; padding: 15px 0; }
        .img-game { width: 110px; border-radius: 4px; border: 1px solid #333344; }
    </style>
</head>
<body>
    <nav class="navbar py-3">
        <div class="container d-flex justify-content-between align-items-center">
            <a class="navbar-brand" href="/">GameStore</a>
            <div>
                <a href="/login" class="btn btn-outline-light-custom">Login</a>
                <a href="/download?arquivo=app.py" style="display:none;">Manual</a>
            </div>
        </div>
    </nav>
    <div class="container mt-5 pb-5">
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    linhas_tabela = ""
    for jogo in JOGOS:
        linhas_tabela += f"""
        <tr>
            <td style="width: 130px;"><img src="{jogo['capa']}" class="img-game" alt="Capa"></td>
            <td class="text-white fw-bold">{jogo['titulo']}</td>
            <td class="text-white fw-bold">{jogo['preco']}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-yellow me-2 px-3">Editar</button>
                <button class="btn btn-sm btn-outline-red px-3">Excluir</button>
            </td>
        </tr>
        """

    content = f"""
        <div class="d-flex justify-content-between align-items-end mb-4">
            <div>
                <h2 class="fw-bold mb-0">Gerenciar Games</h2>
                <small style="color: #888899;">Controle de inventário e catálogo da loja</small>
            </div>
            <div>
                <button class="btn btn-green px-4">+ Novo Game</button>
            </div>
        </div>
        <div class="card-custom">
            <table class="table">
                <thead>
                    <tr>
                        <th colspan="2">CAPA / TÍTULO DO JOGO</th>
                        <th>PREÇO</th>
                        <th class="text-end">AÇÕES</th>
                    </tr>
                </thead>
                <tbody>{linhas_tabela}</tbody>
            </table>
        </div>
    """
    return render_template_string(TEMPLATE_BASE, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem = ""
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')
        
        conn = sqlite3.connect('gamestore.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{senha}'"
        
        try:
            c.execute(query)
            user = c.fetchone()
            if user:
                return redirect("/")
            else:
                mensagem = f"<div class='alert alert-danger mt-4' style='background-color:#4a191e; color:#e74c3c; border:none;'>Credenciais incorretas para <b>{email}</b>.</div>"
        except Exception as e:
            mensagem = f"<div class='alert alert-warning mt-4' style='background-color:#504010; color:#f1c40f; border:none;'>Erro DB: {e}</div>"
        finally:
            conn.close()

    content = f"""
        <div class="row justify-content-center align-items-center" style="min-height: 60vh;">
            <div class="col-md-5 col-lg-4">
                <div class="card-custom p-5" style="background-color: #22222f; border: 1px solid #2a2a35;">
                    <div class="text-center mb-4">
                        <h2 class="fw-bold mb-1">Login</h2>
                        <small style="color: #888899;">Entre para gerenciar seus games</small>
                    </div>
                    <form method="POST" action="/login">
                        <div class="mb-3">
                            <label class="form-label small" style="color: #aaaabb;">E-mail</label>
                            <input type="text" class="form-control p-2" name="email" placeholder="nome@exemplo.com">
                        </div>
                        <div class="mb-4">
                            <label class="form-label small" style="color: #aaaabb;">Senha</label>
                            <input type="password" class="form-control p-2" name="senha" placeholder="********">
                        </div>
                        <button type="submit" class="btn btn-green w-100 py-2">Acessar</button>
                    </form>
                    {mensagem}
                </div>
            </div>
        </div>
    """
    return render_template_string(TEMPLATE_BASE, content=content)

@app.route('/download')
def download_manual():
    arquivo = request.args.get('arquivo', 'app.py')
    try:
        with open(arquivo, 'r') as f:
            return f"<pre style='color:white;'>{f.read()}</pre>"
    except:
        return "<p style='color:red;'>Ficheiro não encontrado.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)