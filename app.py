from flask import Flask, json, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# MongoDB Atlas connection using .env variables
try:
    password = os.getenv('MONGO_PASSWORD')
    mongodb_uri = f"mongodb+srv://ambardarviresh18:{os.getenv('MONGO_PASSWORD')}@tutedude.dw5lcw2.mongodb.net/"
    
    db_name = os.getenv('MONGO_DB_NAME', 'TestDB') 
    collection_name = os.getenv('MONGO_COLLECTION_NAME', 'Sample')
    
    print(f"Attempting to connect to MongoDB Atlas...")
    print(f"Database: {db_name}")
    print(f"Collection: {collection_name}")
    
    client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=5000  # Timeout after 5 seconds
    )
    
    client.admin.command('ping')
    db = client[db_name]
    collection = db[collection_name]
    print("Connected to MongoDB Atlas successfully!")
    
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print(f"Please check your credentials and network connection")
    collection = None

@app.route('/')
def form_page():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    if collection is None:
        error_message = "Database connection failed. Please try again later."
        return render_template('form.html', error=error_message)
    
    try:
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        
        # Validate inputs
        if not name or not email or not age:
            error_message = "All fields are required"
            return render_template('form.html', error=error_message)
        
        data = {
            "name": name,
            "email": email,
            "age": int(age)
        }
        
        collection.insert_one(data)
        return redirect(url_for('success'))
        
    except ValueError:
        error_message = "Age must be a valid number"
        return render_template('form.html', error=error_message)
    except Exception as e:
        error_message = f"Error submitting data: {str(e)}"
        return render_template('form.html', error=error_message)
    

# NEW API ROUTE
@app.route('/api')
def api_endpoint():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, port=port)