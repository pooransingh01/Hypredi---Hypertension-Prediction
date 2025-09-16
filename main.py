from flask import Flask, render_template, request,jsonify,send_from_directory
import psycopg2
import numpy as np
import pickle


# Load trained model
loaded_model = pickle.load(open('C:/Users/rbbha/OneDrive/Desktop/Hypredi/Hypredi/hypertension_model.sav', 'rb'))

app = Flask(__name__,static_folder='Static')
# Making connection to database

conn = psycopg2.connect(database="dhp2024",user = 'postgres', password ='Ram@0916', host='localhost')
cur = conn.cursor()
# Create a table to store the login credentials
cur.execute('''
    CREATE TABLE IF NOT EXISTS login_details(
        email TEXT,
        password VARCHAR(255))''')
conn.commit()

@app.route("/",methods=['GET', 'POST'])
def portal():
    return render_template("Hypredi.html")
@app.route('/signin')
def login():
    return render_template('signin.html')
@app.route('/about_us')
def About():
    return render_template('about_us.html')
@app.route('/contactus')
def Contact():
    return render_template('contactus.html')
@app.route('/Hypredi')
def Home():
    return render_template('Hypredi.html')
@app.route('/form')
def Form():
    return render_template('form.html')

# Signup endpoint
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cur = conn.cursor()
    cur.execute("INSERT INTO login_details (email_id, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Signup successful"}), 200

# Signin endpoint
@app.route("/signin", methods=["POST"])
def signin():
    data = request.json
    username = data.get('email')
    password = data.get('password')
    cur = conn.cursor()
    cur.execute("SELECT * FROM login_details WHERE email_id = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Prediction endpoint
@app.route("/prediction", methods=["POST"])
def prediction():
    data = request.json
    first_input = data.get("first_input")
    second_input = data.get("first_input")
    third_input = data.get("third_input")
    fourth_input = data.get("fourth_input")
    data = (first_input, second_input, third_input, fourth_input)
    data_array = np.asarray(data)
    input_data_reshape = data_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshape)
    if prediction[0] == 0:
        return jsonify({"prediction": "No Hypertension"}), 200
    else:
        return jsonify({"prediction": "Hypertension"}), 200

if __name__=='__main__':
    app.run(debug=True, port=8000)
    conn.close()
