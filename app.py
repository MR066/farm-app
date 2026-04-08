from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Простая "база данных": список словарей
products = [
    {"name": "Яблоки", "quantity": 100, "price": 20},
    {"name": "Молоко", "quantity": 40, "price": 60},
]

# Главная страница
@app.route('/')
def index():
    return render_template_string('''
        <h1>Учёт продукции фермы</h1>
        <a href="{{ url_for('add') }}">Добавить продукцию</a><br><br>
        <table border=1 cellpadding=5>
        <tr><th>Название</th><th>Количество</th><th>Цена</th><th>Продажа</th></tr>
        {% for p in products %}
          <tr>
            <td>{{p.name}}</td>
            <td>{{p.quantity}}</td>
            <td>{{p.price}}</td>
            <td>
                <form action="{{ url_for('sell', idx=loop.index0) }}" method="post" style="display:inline">
                    <input type="number" name="amount" min=1 max={{p.quantity}} required>
                    <button type="submit">Продать</button>
                </form>
            </td>
          </tr>
        {% endfor %}
        </table>
    ''', products=products)

# Страница добавления продукции
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = int(request.form['price'])
        products.append({
            "name": name,
            "quantity": quantity,
            "price": price
        })
        return redirect(url_for('index'))
    return render_template_string('''
        <h2>Добавить продукцию</h2>
        <form method="post">
            Название: <input name="name" required><br>
            Количество: <input type="number" name="quantity" min=1 required><br>
            Цена: <input type="number" name="price" min=1 required><br>
            <button type="submit">Добавить</button>
        </form>
        <a href="{{ url_for('index') }}">Назад</a>
    ''')

# Продажа товара
@app.route('/sell/<int:idx>', methods=['POST'])
def sell(idx):
    amount = int(request.form['amount'])
    if 0 <= idx < len(products):
        if products[idx]['quantity'] >= amount:
            products[idx]['quantity'] -= amount
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)