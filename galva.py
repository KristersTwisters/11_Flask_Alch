from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# --- VecaisKorpuss models ---
class VecaisKorpuss(db.Model):
    __tablename__ = 'vecais_korpuss'
    id = db.Column(db.Integer, primary_key=True)
    stavs1 = db.relationship('PirmaisStavs', backref='korpuss', lazy=True)
    stavs2 = db.relationship('OtraisStavs', backref='korpuss', lazy=True)
    stavs3 = db.relationship('TresaisStavs', backref='korpuss', lazy=True)

class PirmaisStavs(db.Model):
    __tablename__ = 'pirmais_stavs'
    klase = db.Column(db.Integer, primary_key=True)
    pieejams = db.Column(db.Boolean, nullable=False)
    idk = db.Column(db.String(50), nullable=False)
    korpuss_id = db.Column(db.Integer, db.ForeignKey('vecais_korpuss.id'), nullable=False)

class OtraisStavs(db.Model):
    __tablename__ = 'otrais_stavs'
    id = db.Column(db.Integer, primary_key=True)
    pieejams = db.Column(db.Boolean, nullable=False)
    idk = db.Column(db.String(50), nullable=False)
    korpuss_id = db.Column(db.Integer, db.ForeignKey('vecais_korpuss.id'), nullable=False)

class TresaisStavs(db.Model):
    __tablename__ = 'tresais_stavs'
    id = db.Column(db.Integer, primary_key=True)
    pieejams = db.Column(db.Boolean, nullable=False)
    idk = db.Column(db.String(50), nullable=False)
    korpuss_id = db.Column(db.Integer, db.ForeignKey('vecais_korpuss.id'), nullable=False)
# Definējam datubāzes modeļus
class Personas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vards = db.Column(db.String(50), nullable=False)
    uzvards = db.Column(db.String(50), nullable=False)
    piekluvesLimenis = db.Column(db.String(50), nullable=False)

class Pirmais_(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veids = db.Column(db.String(50), nullable=False)
    datums1 = db.Column(db.DateTime, default=datetime.utcnow)
    skaits = db.Column(db.Integer, nullable=False)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

class Tabula1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vards = db.Column(db.String(50), nullable=False)
    uzvards = db.Column(db.String(50), nullable=False)
    vecums = db.Column(db.Integer, nullable=False)

class Tabula2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veids = db.Column(db.String(50), nullable=False)
    skaits = db.Column(db.Integer, nullable=False)

# Izveidojam datubāzi
with app.app_context():
    db.create_all()
    # Create VecaisKorpuss with 3 floors if not exists
    if not VecaisKorpuss.query.first():
        korpuss = VecaisKorpuss()
        db.session.add(korpuss)
        db.session.commit()
        
        # Create each floor
        stavs1 = PirmaisStavs(pieejams=True, idk='1st Floor', korpuss_id=korpuss.id)
        stavs2 = OtraisStavs(pieejams=True, idk='2nd Floor', korpuss_id=korpuss.id)
        stavs3 = TresaisStavs(pieejams=True, idk='3rd Floor', korpuss_id=korpuss.id)
        
        db.session.add_all([stavs1, stavs2, stavs3])
        db.session.commit()

#Create an entry called vecaisKorpuss with 3 under entries that have 3 fields each: ID, pieejams, idk

def create_entry(data):
    new_entry = Tabula1(vards=data['vards'], uzvards=data['uzvards'], vecums=data['vecums'])

    try:
        db.session.add(new_entry)
        db.session.commit()
        return 'Ieraksts pievienots veiksmīgi.'
    except:
        return 'Kaut kas nogāja greizi.'

# Dekorācija uz ieraaksta izveidi Tabulā1
def create_entry_tabula1(data):
    new_entry = Tabula1(vards=data['vards'], uzvards=data['uzvards'], vecums=data['vecums'])

    try:
        db.session.add(new_entry)
        db.session.commit()
        return 'Ieraksts pievienots veiksmīgi.'
    except:
        return 'Kaut kas nogāja greizi.'

# Dekorācija uz ieraksta izveidi Tabulā2
def create_entry_tabula2(data):
    new_entry = Tabula2(veids=data['veids'], skaits=data['skaits'])

    try:
        db.session.add(new_entry)
        db.session.commit()
        return 'Ieraksts pievienots veiksmīgi.'
    except:
        return 'Kaut kas nogāja greizi.'

# Dekorācija uz datu izgūšanu no Tabulas2 ar nosacījumu
def fetch_data_conditionally():
    data = Tabula2.query.filter(Tabula2.skaits > 4).all()
    return data
def fetch_data_tabula1_visi():
    data_tabula1 = Tabula1.query.all()
    # Izveidojam vārdnīcu ar datiem
    result = []
    for entry in data_tabula1:
        result.append({
            'id': entry.id,
            'vards': entry.vards,
            'uzvards': entry.uzvards,
            'vecums': entry.vecums
        })
    return result

@app.route('/')
def index():
    data_tabula2 = fetch_data_conditionally()
    return render_template('index.html', data_tabula2=data_tabula2)

@app.route('/visi')
def visi():
    data_tabula1 = fetch_data_tabula1_visi()
    print("Tas ko saņem pirms lapas")
    print(data_tabula1)
    return render_template('personas.html', tasks=data_tabula1)

@app.route('/add_tabula1', methods=['POST'])
def add_tabula1():
    data = {
        'vards': request.form['vards'],
        'uzvards': request.form['uzvards'],
        'vecums': int(request.form['vecums'])
    }
    result = create_entry_tabula1(data)
    return result

@app.route('/add_tabula2', methods=['POST'])
def add_tabula2():
    data = {
        'veids': request.form['veids'],
        'skaits': int(request.form['skaits'])
    }
    result = create_entry_tabula2(data)
    return result

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_task = Task(content=content)

    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'Kaut kas nogāja greizi'
@app.route('/kalendars')
def kalendars():
    
    return render_template('kalendars.html')

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=5000)