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


# Search Page
@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":

        name = request.args.get('name', default = None , type = str)
        year = request.args.get('year')
        platform = request.args.get('platform', default = None , type = str)
        genre = request.args.get('genre', default = None , type = str)
        global_sales = request.args.get('global_sales', default = None , type = int)
        critic_score = request.args.get('critic_score', default = None , type = int)
        developer = request.args.get('developer', default = None , type = str)

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE VIEW temp as
                       SELECT * FROM Game_table games """)
        if name:
            cursor.execute("""
                           CREATE VIEW temp1 as
                           SELECT * FROM temp t
                           WHERE t.Name = %s""" , (name,))
        else:
            cursor.execute("""
                           CREATE VIEW temp1 as
                           SELECT * FROM temp t""")
            
        # YEAR
        # if year:
        #     cursor.execute("""
        #                    CREATE VIEW temp2 as
        #                    SELECT * FROM temp1 t1
        #                    WHERE temp1.year = %s""" , (year,))
        # else:
        #     cursor.execute("""
        #                    CREATE VIEW temp2 as
        #                    SELECT * FROM temp1""")
            
        # PLATFORM
        if platform:
            cursor.execute("""
                           CREATE VIEW temp3 as
                           SELECT * FROM temp2 t2 , Platform_table pt
                           WHERE t2.Platform_ID = pt.Platform_ID AND pt.platform = %s""" , (platform,))
        else:
            cursor.execute("""
                           CREATE VIEW temp3 as
                           SELECT * FROM temp2 t2""")
            
        # GENRE
        # if genre:
        #     cursor.execute("""
        #                    CREATE VIEW temp4 as
        #                    SELECT * FROM temp3
        #                    WHERE temp3.genre = %s""" , (genre,))
        # else:
        #     cursor.execute("""
        #                    CREATE VIEW temp4 as
        #                    SELECT * FROM temp3""")
            
        #GLOBAL_SALES
        if global_sales:
            cursor.execute("""
                           CREATE VIEW temp5 as
                           SELECT * FROM temp4 t4 , Sales_table st
                           WHERE t4.Game_ID = st.Game_ID AND st.Global_sales >= %d""" , (global_sales,))
        else:
            cursor.execute("""
                           CREATE VIEW temp5 as
                           SELECT * FROM temp4" t4""")
            
        
        #CRITIC_SCORE
        if critic_score:
            cursor.execute("""
                           CREATE VIEW temp6 as
                           SELECT * FROM temp5 t5 , Score_table sct
                           WHERE t5.Game_ID = sct.Game_ID AND sct.Critic_score >= %d""" , (critic_score,))
        else:
            cursor.execute("""
                           CREATE VIEW temp6 as
                           SELECT * FROM temp5 t5""")
            
        # DEVELOPER
        if developer:
            cursor.execute("""
                           CREATE VIEW temp7 as
                           SELECT * FROM temp6 t6
                           WHERE t6.Developer = %s""" , (developer,))
        else:
            cursor.execute("""
                           CREATE VIEW temp7 as
                           SELECT * FROM temp6 t6""")

        
        cursor.execute("SELECT * FROM temp7")

        games = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

    return render_template("search.html" , games = games)


# Render Game Page
@app.route("/game_page/<int:game_id>", methods=["GET"])
def game_page(game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM comment_table WHERE game_id = %s", (game_id,))

    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("comment.html", comments=comments, selected_game_id=game_id)


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
