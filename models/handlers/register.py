from flask import Blueprint, request, jsonify

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing required fields!"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    insert_query = """
        INSERT INTO users (username, password, wins)
        VALUES (%s, %s, %s)
    """
    try:
        cur.execute(insert_query, (username, password, 0))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"message": "Username already exists!"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "An error occurred: " + str(e)}), 500
    finally:
        cur.close()
        conn.close()