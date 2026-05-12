import sys
from flask import Flask, redirect, url_for, render_template, request, session
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# A secret key is required to use Flask sessions securely. 
# In a real app, this should be a random, hidden string.
app.secret_key = 'super_secret_key_for_testing'




load_dotenv()  # Load environment variables from .env file





def check_postgres_connection():
    print(f"Attempting to connect to {os.getenv('DB_HOST')}...")
    
    try:
        # connect_timeout prevents the script from hanging if blocked by a firewall
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            connect_timeout=5 
        )
        cursor = conn.cursor()
        
        # Execute a lightweight ping
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        
        print("✅ Success: Connected to the PostgreSQL database and executed ping.")
        
        # Clean up
        cursor.close()
        conn.close()
        return True

    except psycopg2.OperationalError as e:
        print("❌ Error: Connection failed. Verify your credentials, host URL, and AWS Security Group inbound rules.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        return False










@app.route('/')
@app.route('/home')
def home():
    check_postgres_connection()

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    # If the user submits the form, it will be a POST request
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verify credentials against our "database"
        if username in USER_DATA and USER_DATA[username] == password:
            # Success! Store the username in the session
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
            
    # If it's a GET request (just visiting the page), or if there was an error, render the login page
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # Remove the username from the session to log out
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)