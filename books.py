from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {'id': 1, 'name': 'Geeta', 'price': 100},
    {'id': 2, 'name': 'Quran', 'price': 5},
    {'id': 3, 'name': 'Bible', 'price': 50}
]
@app.route('/books')
def get_books():
    print("Books:", books)
    return jsonify(books)
@app.route('/')
def home():
    return 'Welcome to the Book Store!'
@app.route('/home')
def about():
    return 'This is the about page.'
@app.route('/getbook/<int:id>', methods=['GET'])
def get_book(id):
    book = [b for b in books if b['id'] == id]
    return jsonify(book[0])

@app.route('/addbook', methods=['POST'])
def add_book():
    data = request.get_json()
    if data['id'] in [b['id'] for b in books]:
        return jsonify({'error': 'Book with this ID already exists'}), 400
    else:
        books.append(data)

    return jsonify(books)
@app.route('/deletebook/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books

    book = next((b for b in books if b['id'] == id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    books = [b for b in books if b['id'] != id]
    return jsonify({'message': 'Book deleted', 'remaining_books': books})

@app.route('/updatebook/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()

    for book in books:
        if book['id'] == id:
            book['name'] = data['name']
            book['price'] = data['price']
            return jsonify(book)

    return jsonify({'error': 'Book not found'}), 404

@app.route('/patchbook/<int:id>', methods=['PATCH'])
def patch_book(id):
    data = request.get_json()

    for book in books:
        if book['id'] == id:
            if 'name' in data:
                book['name'] = data['name']
            if 'price' in data:
                book['price'] = data['price']
            return jsonify(book)

    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)