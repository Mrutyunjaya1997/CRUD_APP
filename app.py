from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

# Route to the homepage
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return render_template('index.html', rows=rows)

# Route to add a new user
@app.route('/add/', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
                msg = "Record successfully added"
        except:
            conn.rollback()
            msg = "Error in insert operation"
        finally:
            return redirect(url_for('home'))
            conn.close()
    return render_template('add.html')

# Route to delete a user
@app.route('/delete/<int:id>/', methods=['GET'])
def delete_user(id):
    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            msg = "Record successfully deleted"
    except:
        conn.rollback()
        msg = "Error in delete operation"
    finally:
        return redirect(url_for('home'))
        conn.close()

# Route to update a user
@app.route('/update/<int:id>/', methods=['POST', 'GET'])
def update_user(id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, id))
                conn.commit()
                msg = "Record successfully updated"
        except:
            conn.rollback()
            msg = "Error in update operation"
        finally:
            return redirect(url_for('home'))
            conn.close()
    return render_template('update.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)
