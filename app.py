from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products

@app.route('/ping')
def ping():
    return jsonify({'message':'Pong!'})


@app.route('/products')
def getProducts():
    return jsonify({'products':products, 'message':'Product list'})


@app.route('/products/<string:product_name>')
def get_product(product_name):
    product_found = [product for product in products if product['name'] == product_name]

    if len(product_found) > 0:
        return jsonify({'product':product_found[0], 'message':'Product'})
    return jsonify({'message':'Product not found'})


@app.route('/products', methods=['POST'])
def add_product():
    new_product = {
        'name' : request.json['name'],
        'price': request.json['price'],
        'quantity': request.json['quantity'],
    }
    products.append(new_product)
    return jsonify({'message': 'Product added successfully', 'products': products})


@app.route('/products/<string:product_name>', methods=['PUT'])
def edit_product(product_name):
    product_found = [product for product in products if product['name'] == product_name]
    if len(product_found) > 0:
        product_found[0]['name'] = request.json['name']
        product_found[0]['price'] = request.json['price']
        product_found[0]['quantity'] = request.json['quantity']
        return jsonify({
            'message': 'Product updated',
            'product': product_found[0]
        })
    return jsonify({'message': 'Product not found'})


@app.route('/products/<string:product_name>', methods=['DELETE'])
def delete_product(product_name):
    product_found = [product for product in products if product['name'] == product_name]
    if len(product_found) > 0:
        products.remove(product_found[0])
        return jsonify({'message': 'Product deleted', 'products': products})
    return jsonify({'message': ' Product not found'})


if __name__ == '__main__':
    app.run(debug=True, port=4000)