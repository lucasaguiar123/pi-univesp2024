from flask import Flask, render_template, render_template_string, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Initialize Firebase app (replace with your credentials)
cred = credentials.Certificate(json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT')))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://estoque-piunivesp2024.firebaseio.com'
})

app = Flask(__name__)
ref = db.reference('/')

# HTML for the stock page (similar to the original)

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
          <td>{{ item['id'] }}</td>
          <td>{{ item['nome'] }}</td>
          <td>{{ item['quantidade'] }}</td>
          <td>{{ item['preco'] }}</td>
          <td>
            <a href="{{ url_for('excluir_item', item_id=item['id']) }}" class="btn btn-danger">Excluir</a>
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

# HTML for the add item page (similar to the original)
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
    estoque_ref = ref.child('estoque')
    if not estoque_ref.get().exists():
      estoque_ref.set({})  # Create an empty dictionary for 'estoque'
    # Fetch all items from the 'estoque' node
    items = ref.child('estoque').get().val() or []
    return render_template_string(html_estoque, items=items)

@app.route('/adicionar_item', methods=['GET', 'POST'])
def adicionar_item():
  if request.method == 'POST':
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    # Create a new child node under 'estoque' with a unique key
    new_item_ref = ref.child('estoque').push()

    # Set the data for the new item using a dictionary
    new_item_data = {
      'nome': nome,
      'quantidade': quantidade,
      'preco': preco
    }

    new_item_ref.set(new_item_data)

    # Redirect to the stock page after adding the item
    return redirect(url_for('estoque'))
  return render_template_string(html_adicionar)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
