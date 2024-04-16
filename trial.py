from flask import Flask, redirect, url_for, render_template,request,session
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
app.secret_key = 'expensetracker'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change this to your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Change this to your MySQL password
app.config['MYSQL_DB'] = 'expense_tracker_app' 
mysql = MySQL(app)

import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'expense_tracker_app'
}

# Function to fetch user data from the database based on username
def userdata_database(username):
    try:

        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, username, email FROM users WHERE username = %s"

        cursor.execute(query, (username,))
        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

        return user_data

    except mysql.connector.Error as error:
        print("Error fetching user data from database:", error)
        return None

def userincome_database(username):
    try:

        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor(dictionary=True)

        query = "SELECT income FROM budget WHERE username = %s"

        cursor.execute(query, (username,))
        user_income = cursor.fetchone()

        cursor.close()
        connection.close()

        return user_income

    except mysql.connector.Error as error:
        print("Error fetching user data from database:", error)
        return None

# Route for registering a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('/login')
        except mysql.connector.Error as error:
            print("Error registering user:", error)
            return 'An error occurred during registration'
    return render_template('register.html')

# Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                session['username'] = username
                return redirect('/home')
            else:
                return 'Invalid username or password'
        except mysql.connector.Error as error:
            print("Error logging in:", error)
            return 'An error occurred during login'
    return render_template('login.html')

# Route for viewing the user profile
@app.route('/profile', methods=['GET'])
def profile():
    if 'username' in session:
        username = session['username']
        user_data = userdata_database(username)
        user_income = userincome_database(username)
        if user_data:
            return render_template('profile.html', user_data=user_data, user_income=user_income)
        else:
            return 'User data not found'
    else:
        return 'You are not logged in'

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/home")
def test():
    return render_template("temp.html")

@app.route("/setb", methods=["GET", "POST"])
def test1():
    if request.method == 'POST':
        income = request.form['income']
        budget = request.form['budget']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()        
            cursor.execute("INSERT INTO budget (income, budget, start_date, end_date) VALUES (%s, %s, %s, %s)", (income, budget, start_date, end_date))
            connection.commit()  # Use connection.commit() instead of mysql.connection.commit()
            cursor.close()
        except mysql.connector.Error as error:
            print("Error inserting data into database:", error)
        finally:
            if 'connection' in locals():
                connection.close()  # Close the connection in the finally block
    return render_template('new.html')


@app.route("/expense")
def test2():
    return render_template("addexp.html")


@app.route("/profile")
def test3():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
