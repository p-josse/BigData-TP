from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection configuration
db_config = {
    'dbname': 'postgres',
    'user': 'admin',
    'password': 'adminadmin',
    'host': 'localhost',
    'port': '5432'
}

# Define endpoints

@app.route('/films', methods=['GET'])
def get_films():
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute the query to retrieve all films
        cursor.execute("SELECT * FROM film")

        # Fetch all rows as a list of dictionaries
        films = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Convert the result to a list of dictionaries for JSON serialization
        film_list = [{"id": film[0], "name": film[1], "description": film[2]} for film in films]

        return jsonify({"films": film_list})

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

@app.route('/films', methods=['POST'])
def add_film():
    data = request.get_json()
    movie_name = data.get('name')
    movie_description = data.get('description')

    # Implement logic to add a new film to the database
    # You should use psycopg2 to interact with the PostgreSQL database
    # Example:
    # conn = psycopg2.connect(**db_config)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO films (name, description) VALUES (%s, %s)", (movie_name, movie_description))
    # conn.commit()
    # cursor.close()
    # conn.close()

    return jsonify({"message": "Film added successfully"})

@app.route('/films/<film_id>', methods=['GET'])
def get_film(film_id):
    # Implement logic to retrieve and return the details of the specified film
    return jsonify({"film": {}})

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=8080)
