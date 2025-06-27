from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['POST', 'GET'])
def home_login():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return f"<h2>Welcome {username}!</h2>"
        else:
            return "<h2>Login failed. User not found or wrong password.</h2>"

    return render_template('index.html')

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['user']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return "Passwords do not match!"

        # Prüfen ob Nutzername schon existiert
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists!"

        new_user = User(username=username, password=password1)
        db.session.add(new_user)
        db.session.commit()

        return "<h2>Registration successful! You can now <a href='/'>login</a>.</h2>"

    return render_template('sign-up.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
