from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)

# A secret key is required to use Flask sessions securely. 
# In a real app, this should be a random, hidden string.
app.secret_key = 'super_secret_key_for_testing'

# Dummy database for demonstration purposes
USER_DATA = {
    "admin": "password123",
    "user1": "hello_world"
}

@app.route('/')
@app.route('/home')
def home():
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