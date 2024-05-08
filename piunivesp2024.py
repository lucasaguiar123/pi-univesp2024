from flask import Flask, render_template, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar a tabela de estoque
def create_table():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                      id INTEGER PRIMARY KEY,
                      nome TEXT NOT NULL,
                      quantidade INTEGER NOT NULL,
                      preco REAL NOT NULL
                      )''')
    conn.commit()
    conn.close()

# HTML para a página de estoque
html_estoque = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estoque</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Estoque Pádua</h1>
        <table>
            <thead>
                <tr>
                    <th>ID &nbsp</th>
                    <th>Nome &nbsp</th>
                    <th>Quantidade &nbsp</th>
                    <th>Preço &nbsp</th>
                    <th>Ações &nbsp</th>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                <tr>
                    <td>{{ item[0] }}</td>
                    <td>{{ item[1] }}</td>
                    <td>{{ item[2] }}</td>
                    <td>{{ item[3] }}</td>
                    <td>
                        <a href="{{ url_for('excluir_item', item_id=item[0]) }}" class="btn btn-danger">Excluir</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <br>
        <a href="{{ url_for('adicionar_item') }}" class="btn btn-primary">Adicionar novo item</a>
    </div>
</body>
</html>
"""

# HTML para a página de adicionar item
html_adicionar = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adicionar Item</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Adicionar Item ao Estoque</h1>
        <form action="{{ url_for('adicionar_item') }}" method="post">
            <div class="input-field">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required>
            </div>
            <div class="input-field">
                <label for="quantidade">Quantidade:</label>
                <input type="number" id="quantidade" name="quantidade" required>
            </div>
            <div class="input-field">
                <label for="preco">Preço:</label>
                <input type="number" id="preco" name="preco" step="0.01" required>
            </div>
            <input type="submit" value="Adicionar" class="btn btn-primary">
        </form>
        <br>
        <a href="/" class="btn btn-primary">Voltar para o estoque</a>
    </div>
</body>
</html>
"""

@app.route('/')
def estoque():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estoque')
    items = cursor.fetchall()
    conn.close()
    return render_template_string(html_estoque, items=items)

@app.route('/adicionar_item', methods=['GET', 'POST'])
def adicionar_item():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']

        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO estoque (nome, quantidade, preco) VALUES (?, ?, ?)', (nome, quantidade, preco))
        conn.commit()
        conn.close()

        return redirect(url_for('estoque'))
    return render_template_string(html_adicionar)

@app.route('/excluir/<int:item_id>')
def excluir_item(item_id):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estoque WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('estoque'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)