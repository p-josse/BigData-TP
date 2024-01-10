from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection configuration
db_config = {
    'dbname': 'postgres',
    'user': 'admin',
    'password': 'adminadmin',
    'host': '172.17.0.2',
    'port': '5432'
}

@app.route('/films', methods=['GET'])
def get_films():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM film")
        films = cursor.fetchall()

        cursor.close()
        conn.close()

        film_list = [{"id": film[0], "title": film[1], "description": film[2]} for film in films]

        return jsonify({"films": film_list})

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/films', methods=['POST'])
def add_film():
    try:
        data = request.get_json()

        if not data or 'title' not in data or 'description' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        title = data['title']
        description = data['description']
        language_id = data.get('language_id', 1)

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO film (title, description, language_id) VALUES (%s, %s, %s) RETURNING film_id", (title, description, language_id))
        new_film_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Film added successfully", "film_id": new_film_id})

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM film WHERE film_id = %s", (film_id,))
        film = cursor.fetchone()

        cursor.close()
        conn.close()

        if film:
            return jsonify({"film": {"film_id": film[0], "title": film[1], "description": film[2]}})
        else:
            return jsonify({"error": "Film not found"}), 404

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')