from flask import Flask, render_template, redirect, url_for, request
import psycopg2
from psycopg2 import OperationalError, Error

app = Flask(__name__,template_folder='templates')

# Configuração da conexão com o banco de dados PostgreSQL
DATABASE = {
    'dbname': 'estoque',
    'user': 'postgres',
    'password': 'mudar123',
    'host': 'localhost',
    'port': '5432'
}
  
# Função para criar a tabela de estoque no PostgreSQL
def create_table():
    try:
        conn = psycopg2.connect(**DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (
                          id SERIAL PRIMARY KEY,
                          nome TEXT NOT NULL,
                          quantidade INTEGER NOT NULL,
                          preco REAL NOT NULL
                          )''')
        conn.commit()
        conn.close()
    except (OperationalError, Error) as e:
        print(f"Erro ao criar a tabela de estoque: {e}")

# Rota principal para exibir o estoque
@app.route('/',methods=['GET'])
def estoque():
    try:
        conn = psycopg2.connect(**DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque')
        items = cursor.fetchall()
        conn.close()
        return render_template('estoque.html', items=items)
    except (OperationalError, Error) as e:
        print(f"Erro ao buscar itens de estoque: {e}")
        return render_template('estoque.html', items=[])

# Rota para adicionar um novo item ao estoque
@app.route('/adicionar_item', methods=['GET', 'POST'])
def adicionar_item():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO estoque (nome, quantidade, preco) VALUES (%s, %s, %s)', (nome, quantidade, preco))
            conn.commit()
            conn.close()
            return redirect(url_for('/'))
        except (OperationalError, Error) as e:
            print(f"Erro ao adicionar item ao estoque: {e}")
            return redirect(url_for('/'))
    return render_template('adicionar_item.html')

# Rota para excluir um item do estoque
@app.route('/excluir/<int:item_id>')
def excluir_item(item_id):
    try:
        conn = psycopg2.connect(**DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM estoque WHERE id = %s', (item_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('estoque'))
    except (OperationalError, Error) as e:
        print(f"Erro ao excluir item do estoque: {e}")
        return redirect(url_for('estoque'))

if __name__ == '__main__':
    create_table()  # Garante que a tabela de estoque esteja criada antes de iniciar o servidor Flask
    app.run(debug=True)
