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
    'database': 'final_project'  # Change this to your MySQL database name
}


# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Search Page
@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":

        game_name = request.args.get('game_name', default = None , type = str)
        year = request.args.get('year' , default = None , type = int)
        platform = request.args.get('platform', default = None , type = str)
        genre = request.args.get('genre', default = None , type = str)
        global_sales = request.args.get('global_sales', default = None , type = float)
        critic_score = request.args.get('critic_score', default = None , type = int)
        user_score = request.args.get('user_score', default = None , type = float)
        developer = request.args.get('developer', default = None , type = str)
        age = request.args.get('age', default = None , type = int)

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("DROP VIEW IF EXISTS temp")
        cursor.execute("""
                       CREATE VIEW temp as
                       SELECT * FROM game_table games """)
        
        # GAME_NAME
        cursor.execute("DROP VIEW IF EXISTS temp1")
        if game_name:
            game_name = game_name.upper()
            cursor.execute(f"""
                           CREATE VIEW temp1 as
                           SELECT * FROM temp t
                           WHERE Upper(t.game_name) LIKE '%{game_name}%'""")
        else:
            cursor.execute("""
                           CREATE VIEW temp1 as
                           SELECT * FROM temp t""")
            
        #YEAR
        cursor.execute("DROP VIEW IF EXISTS temp2")
        if year:
            cursor.execute("""
                           CREATE VIEW temp2 as
                           SELECT * FROM temp1 t1
                           WHERE t1.year = %s
                           ORDER BY t1.year DESC
                           """ , (year,))
        else:
            cursor.execute("""
                           CREATE VIEW temp2 as
                           SELECT * FROM temp1 t1
                           """)
            
        # PLATFORM
        cursor.execute("DROP VIEW IF EXISTS temp3")
        if platform:
            cursor.execute("""
                           CREATE VIEW temp3 as
                           SELECT t2.*, pt.platform
                           FROM temp2 t2
                           JOIN platform_table pt
                           ON t2.platform_id = pt.platform_id
                           WHERE Upper(pt.platform) = Upper(%s)""", (platform,))
        else:
            cursor.execute("""
                           CREATE VIEW temp3 as
                           SELECT t2.*, pt.platform
                           FROM temp2 t2
                           LEFT JOIN platform_table pt
                           ON t2.platform_id = pt.platform_id""")
            
        #GENRE
        cursor.execute("DROP VIEW IF EXISTS temp4")
        if genre:
            cursor.execute("""
                           CREATE VIEW temp4 as
                           SELECT * FROM temp3 t3
                           WHERE t3.genre = %s""" , (genre,))
        else:
            cursor.execute("""
                           CREATE VIEW temp4 as
                           SELECT * FROM temp3""")
            
        #GLOBAL_SALES
        cursor.execute("DROP VIEW IF EXISTS temp5")
        if global_sales:
            cursor.execute("""
                           CREATE VIEW temp5 as
                           SELECT t4.*, st.global_sales
                           FROM temp4 t4
                           JOIN sales_table st
                           ON t4.game_id = st.game_id
                           WHERE st.global_sales >= %s""" , (global_sales,))
        else:
            cursor.execute("""
                           CREATE VIEW temp5 as
                           SELECT t4.*, st.global_sales
                           FROM temp4 t4
                           LEFT JOIN sales_table st
                           ON t4.game_id = st.game_id""")
            
        #CRITIC_SCORE
        cursor.execute("DROP VIEW IF EXISTS temp6")
        if critic_score:
            cursor.execute("""
                           CREATE VIEW temp6 as
                           SELECT t5.*, sct.critic_score
                           FROM temp5 t5
                           JOIN score_table sct
                           ON t5.game_id = sct.game_id
                           WHERE sct.critic_score >= %s""" , (critic_score,))
        else:
            cursor.execute("""
                           CREATE VIEW temp6 as
                           SELECT t5.*, sct.critic_score
                           FROM temp5 t5
                           LEFT JOIN score_table sct
                           ON t5.game_id = sct.game_id""")
            
        # DEVELOPER
        cursor.execute("DROP VIEW IF EXISTS temp7") 
        if developer:
            cursor.execute("""
                           CREATE VIEW temp7 as
                           SELECT * FROM temp6 t6
                           WHERE Upper(t6.developer) = Upper(%s)""" , (developer,))
        else:
            cursor.execute("""
                           CREATE VIEW temp7 as
                           SELECT * FROM temp6 t6""")
        
        #USER_SCORE
        cursor.execute("DROP VIEW IF EXISTS temp8")
        if user_score:
            cursor.execute("""
                           CREATE VIEW temp8 as
                           SELECT t7.*, sct.user_score
                           FROM temp7 t7
                           JOIN score_table sct
                           ON t7.game_id = sct.game_id
                           WHERE sct.user_score >= %s""" , (user_score,))
        else:
            cursor.execute("""
                           CREATE VIEW temp8 as
                           SELECT t7.*, sct.user_score
                           FROM temp7 t7
                           LEFT JOIN score_table sct
                           ON t7.game_id = sct.game_id""")
            
        #AGE
        cursor.execute("DROP VIEW IF EXISTS temp9")
        if age:
            cursor.execute("""
                           CREATE VIEW temp9 as
                           SELECT t8.*, rt.age
                           FROM temp8 t8
                           JOIN rating_table rt
                           ON t8.rating = rt.rating
                           WHERE rt.age <= %s
                           """, (age,))
        else:
            cursor.execute("""
                           CREATE VIEW temp9 as
                           SELECT t8.*, rt.age
                           FROM temp8 t8
                           LEFT JOIN rating_table rt
                           ON t8.rating = rt.rating
                           """)

        
        cursor.execute("SELECT * FROM temp9")
        games = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

    return render_template("search.html" , games=games)


# Render Game Page
@app.route("/game_page/<int:game_id>", methods=["GET"])
def game_page(game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM comment_table WHERE game_id = %s", (game_id,))
    comments = cursor.fetchall()

    cursor.execute("SELECT game_id, game_name, year, platform FROM game_table JOIN platform_table ON game_table.platform_id = platform_table.platform_id WHERE game_id = %s", (game_id,))
    game = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("comment.html", comments=comments, game=game)


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
