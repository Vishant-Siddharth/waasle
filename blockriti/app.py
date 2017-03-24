from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Subscribe, Base


engine = create_engine('sqlite:///blockriti.db')
Base.metadata.bind = engine
Data_session = sessionmaker(bind=engine)
session = Data_session()
app = Flask(__name__)


@app.route('/email_data_blockriti')
def database():
    tmp = ''
    t = []
    for i in session.query(Subscribe).all():
        tmp += '<br>' + i.email
        t.append(i.email)
    return tmp


@app.route('/', methods=['GET', 'POST'])
def coming_soon():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        new = Subscribe()
        new.email = request.form.get('email')
        try:
            session.add(new)
            session.commit()
        except:
            session.rollback()
    return redirect(url_for('coming_soon'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)
