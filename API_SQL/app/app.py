from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for films (initially empty)
films = []

@app.route('/films', methods=['GET'])
def get_films():
    return jsonify({'films': films})

@app.route('/films', methods=['POST'])
def add_film():
    data = request.get_json()
    if 'name' in data and 'description' in data:
        new_film = {
            'name': data['name'],
            'description': data['description']
        }
        films.append(new_film)
        return jsonify({'message': 'Film added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    if film_id < len(films):
        return jsonify(films[film_id])
    else:
        return jsonify({'error': 'Film not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
