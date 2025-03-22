from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:anuja@localhost/wastewise_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Bin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    waste_level = db.Column(db.Float, default=0.0)

# Create database tables
with app.app_context():
    db.create_all()

# API to fetch bin data
@app.route('/bins', methods=['GET'])
def get_bins():
    bins = Bin.query.all()
    return jsonify([{'id': b.id, 'location': b.location, 'waste_level': b.waste_level} for b in bins])

# API to add a new bin
@app.route('/bins', methods=['POST'])
def add_bin():
    data = request.json
    new_bin = Bin(location=data['location'], waste_level=data.get('waste_level', 0.0))
    db.session.add(new_bin)
    db.session.commit()
    return jsonify({'message': 'Bin added successfully!'})


# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        login_user(user)
        return jsonify({'message': 'Login successful!'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out!'})

if __name__ == '__main__':
    app.run(debug=True)
