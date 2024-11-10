from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user='root',
        password=os.environ.get('DB_PASSWORD', 'password'),
        database='testdb'
    )

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
 <html>
 <head>
    <title>Input Form</title>
</head>
<body>
    <h1>Enter a Message</h1>
    <form action="/submit" method="post">
        <label for="message">Message:</label><br>
        <input type="text" id="message" name="message" required><br><br>
        <input type="submit" value="Submit">
        </form>
        </body>
        </html>
                                                                                                                    '''

@app.route('/submit', methods=['POST'])
def submit_message():
    try:
        message = request.form['message']
        connection = get_db_connection()
        cursor = connection.cursor()
# Create table if it doesn't exist
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        message TEXT NOT NULL
                        )
        ''' )
# Insert the message into the database
        cursor.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
        connection.commit()
        return redirect(url_for('home'))
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if connection.is_connected():
           cursor.close()              
           connection.close()

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM messages')
        rows = cursor.fetchall()
        response = '<h1>Saved Messages</h1><ul>'
        for row in rows:
            response += f'<li>Message ID {row[0]}: {row[1]}</li>'
        response += '</ul>'
        return response
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if connection.is_connected():
           cursor.close()
           connection.close()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
