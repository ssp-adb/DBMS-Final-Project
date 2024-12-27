from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector
import hashlib

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"


# Database Configuration
db_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'test',  # Change this to your MySQL username
    'password': '0000',  # Change this to your MySQL password
    'database': 'test'  # Change this to your MySQL database name
}


# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Render Home Page
@app.route("/")
def game_page():
    game_id = request.args.get('game_id', default=None, type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if game_id:
        # Filter comments for the specified game_id
        cursor.execute("SELECT * FROM comment_table WHERE game_id = %s", (game_id,))
    else:
        # Fetch all comments if no game_id is provided
        cursor.execute("SELECT * FROM comment_table")

    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("page.html", comments=comments, selected_game_id=game_id)


# Create comment
@app.route("/comment", methods=["POST"])
def comment():
    game_id = request.form['game_id']
    comment_text = request.form['comment_text']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # insert the comment into the database
    try:
        cursor.execute("INSERT INTO comment_table (game_id, comment_text) VALUES (%s, %s)", (game_id, comment_text))
        conn.commit()
        flash("Comment added successfully", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("game_page", game_id=game_id))


# Delete comment
@app.route("/delete_comment", methods=["POST"])
def delete():
    comment_id = request.form['comment_id']
    game_id = request.form['game_id']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # delete the comment from the database
    try:
        cursor.execute("DELETE FROM comment_table WHERE comment_id = %s", (comment_id,))
        conn.commit()
        flash("Comment deleted successfully", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("game_page", game_id=game_id))


# Edit comment
@app.route("/edit_comment", methods=["POST"])
def edit():
    comment_id = request.form['comment_id']
    game_id = request.form['game_id']
    new_comment_text = request.form['comment_text']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # update the comment in the database
    try:
        cursor.execute("UPDATE comment_table SET comment_text = %s WHERE comment_id = %s", (new_comment_text, comment_id))
        conn.commit()
        flash("Comment updated successfully", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for("game_page", game_id=game_id))


if __name__ == "__main__":
    app.run(debug=True)
