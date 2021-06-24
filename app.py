from flask import Flask, jsonify, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test_rest_api'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/ping')
def ping():
    return jsonify({'message': 'Pong!'})


@app.route('/products')
def get_products():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    row_headers = [x[0] for x in cursor.description]
    products = cursor.fetchall()
    json_data=[]
    for product in products:
            json_data.append(dict(zip(row_headers, product)))
    return jsonify({'message':'Products successfully obtained', 'products':json_data})


@app.route('/products/<int:product_id>')
def get_product(product_id):
    
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM products WHERE product_id = {str(product_id)}")

    row_headers = [x[0] for x in cursor.description]
    product = cursor.fetchone()
    json_data=[]
    if product is not None:
        json_data.append(dict(zip(row_headers, product)))
        return jsonify({'message':'Product successfully obtained', 'product':json_data})
    else:
        return jsonify({'message':'Product not found'})


@app.route('/products', methods=['POST'])
def add_product():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)"
    val = (request.json['name'], request.json['description'], request.json['price'], request.json['quantity'])
    
    cursor.execute(sql, val)
    conn.commit()
    
    return jsonify({'message': 'Product added successfully'})


@app.route('/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "UPDATE products SET name = %s, description = %s, price = %s, quantity = %s WHERE product_id = %s"
    val = (request.json['name'], request.json['description'], request.json['price'], request.json['quantity'], product_id)
    
    cursor.execute(sql, val)
    conn.commit()
    
    return jsonify({'message': 'Product updated successfully'})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "DELETE FROM products WHERE product_id = %s"
    val = (product_id)
    
    cursor.execute(sql, val)
    conn.commit()
    
    return jsonify({'message': 'Product removed successfully'})