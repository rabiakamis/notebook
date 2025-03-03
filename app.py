from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notlar.db'
db = SQLAlchemy(app)

class Not(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def ana_sayfa():
    notlar = Not.query.order_by(Not.tarih.desc()).all()
    return render_template('index.html', notlar=notlar)

@app.route('/not/ekle', methods=['GET', 'POST'])
def not_ekle():
    if request.method == 'POST':
        baslik = request.form['baslik']
        icerik = request.form['icerik']
        yeni_not = Not(baslik=baslik, icerik=icerik)
        db.session.add(yeni_not)
        db.session.commit()
        return redirect(url_for('ana_sayfa'))
    return render_template('not_ekle.html')

@app.route('/not/<int:id>/duzenle', methods=['GET', 'POST'])
def not_duzenle(id):
    not_kaydi = Not.query.get_or_404(id)
    if request.method == 'POST':
        not_kaydi.baslik = request.form['baslik']
        not_kaydi.icerik = request.form['icerik']
        db.session.commit()
        return redirect(url_for('ana_sayfa'))
    return render_template('not_duzenle.html', not_kaydi=not_kaydi)

@app.route('/not/<int:id>/sil')
def not_sil(id):
    not_kaydi = Not.query.get_or_404(id)
    db.session.delete(not_kaydi)
    db.session.commit()
    return redirect(url_for('ana_sayfa'))

if __name__ == '__main__':
    app.run(debug=True) 