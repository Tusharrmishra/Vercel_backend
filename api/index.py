from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ash@1234$#'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'medivance_db'  # Replace with your database name

mysql = MySQL(app)

@app.route('/')
def index():
    return "Welcome to the Medivance Healthcare Backend!"

@app.route('/create_contacts_table')
def create_contacts_table():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                inquiry_type VARCHAR(50) NOT NULL,
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        mysql.connection.commit()
        cur.close()
        return "Contacts table created successfully!"
    except Exception as e:
        return "Error creating table: {}".format(e)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # Required fields validation
        required_fields = ['name', 'email', 'subject', 'message', 'inquiryType']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'error': 'Missing required field: {}'.format(field)
                }), 400

        # Extract form data
        name = data['name']
        email = data['email']
        phone = data.get('phone', '')  # Optional field
        subject = data['subject']
        message = data['message']
        inquiry_type = data['inquiryType']

        # Insert data into database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO contacts 
            (name, email, phone, subject, message, inquiry_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, phone, subject, message, inquiry_type))
        
        mysql.connection.commit()
        cur.close()

        return jsonify({
            'message': 'Contact form submitted successfully!',
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)