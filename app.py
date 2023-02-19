# Import statements:
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application:
app = Flask(__name__)

# Configure the database to store list entries:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# Instantiate SQLAlchemy:
db = SQLAlchemy(app)


# Create a class for the database model:
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)


# Create the database tables within the application context:
with app.app_context():
    db.create_all()


# Create a route for "index.html":
@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete,
                           complete=complete)


# Create a route for "add.html" which is where entries will be stored:
@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


# Create a route for 'complete.html' to collect completed entries:
@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))


# Run the Flask application:
if __name__ == '__main__':
    app.run(debug=True)