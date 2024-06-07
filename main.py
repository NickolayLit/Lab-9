from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steps.db'
db = SQLAlchemy(app)

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'Step(id={self.id}, steps={self.steps}, date={self.date})'

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add' in request.form:
            steps = request.form['steps']
            date = request.form['date']
            new_step = Step(steps=steps, date=datetime.strptime(date, '%Y-%m-%d'))
            db.session.add(new_step)
            db.session.commit()
        elif 'clear' in request.form:
            db.session.query(Step).delete()
            db.session.commit()
        return redirect(url_for('index'))
    
    steps = Step.query.all()
    total_steps = sum(step.steps for step in steps)
    return render_template('index.html', steps=steps, total_steps=total_steps)

@app.route('/add_step', methods=['POST'])
def add_step():
    data = request.get_json()
    new_step = Step(steps=data['steps'], date=datetime.strptime(data['date'], '%Y-%m-%d'))
    db.session.add(new_step)
    db.session.commit()
    return jsonify({'status': 'success'}), 201

@app.route('/clear_steps', methods=['POST'])
def clear_steps():
    db.session.query(Step).delete()
    db.session.commit()
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
