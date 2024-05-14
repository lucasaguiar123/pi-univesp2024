from flask import Flask, render_template, redirect, url_for, request
import psycopg2
from psycopg2 import OperationalError, Error

app = Flask(__name__,template_folder='templates')

# Configuração da conexão com o banco de dados PostgreSQL
DATABASE_URL = 'postgres://default:7Vxa6mIUDeop@ep-ancient-shape-a4mn5jxw-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
  
# Rota principal para exibir o estoque
@app.route('/',methods=['GET'])
def estoque():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estoque_padua')
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
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO estoque_padua (nome, quantidade, preco) VALUES ( %s, %s, %s)", (nome, quantidade, preco))
            conn.commit()
            conn.close()       
        except (OperationalError, Error) as e:
            print(f"Erro ao adicionar item ao estoque: {e}")
            return redirect(url_for('/estoque_padua'))
    return render_template('adicionar_item.html')

# Rota para excluir um item do estoque
@app.route('/excluir/<int:item_id>')
def excluir_item(item_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM estoque_padua WHERE id_produto = %s', (item_id,))
        conn.commit()
        conn.close()
        
    except (OperationalError, Error) as e:
        print(f"Erro ao excluir item do estoque: {e}")
        return redirect(url_for('/estoque_padua'))
    return render_template('adicionar_item.html')

if __name__ == '__main__':
    app.run(debug=True)
