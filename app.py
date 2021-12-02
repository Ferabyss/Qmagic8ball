from flask import Flask, jsonify, render_template, request,redirect
from flask.helpers import flash
from qiskit import *
from config import Development
from forms import sign
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from wtforms.form import Form
from wtforms import StringField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config.from_object(Development)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    ibmid = db.Column(db.String(80))
    fecha = db.Column(db.DateTime, default= datetime.utcnow)
    def __repr__(self):
        return " {0} | {1} | {2}  | {3} | {4} | {5} |   ".format(self.id, self.email, self.password,self.ibmid ,self.fecha)
#app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/userdata'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/contacto')
def contacto():
    lista= ["http://instagram.com/airam.ref", "http://github.com/ferabyss","https://www.linkedin.com/in/mar%C3%ADa-fernanda-mart%C3%ADnez-v%C3%A1zquez-271b90208"]
    lista1= ["Instagram", "Github","Linkedln"]
    return render_template('contacto.html', lista=lista, lista1=lista1)

@app.route('/DecisionMaker')
def decision():
    return render_template('decision.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    print('hola')
    form = sign()
    if request.method== 'POST' and form.validate():
        #validate_on_submit
        print('hola2')
        #username=form.username.data,
        user = User( password = form.password.data, email = form.email.data, ibmid = form.ibmid.data)
        
        db.session.add(user)
        db.session.commit()
        #db.session.flush()
        print('Usuario registrado correctamente.')
        return redirect('/')
    return render_template('signup.html', form = form)
    

@app.route('/login',methods=['GET',"POST"])
def login():
    return render_template('login.html')

@app.route('/loged',methods=['GET',"POST"])
def loged():
    data =User.query.all()
    return render_template('loged.html')

@app.route('/prue',methods=['GET',"POST"])
def prue():
    pregunta = request.form.get("salida")
    if not pregunta:
        error= "Por favor inserte su pregunta."
        return render_template('decision.html',error=error)

    return render_template('prue.html', pregunta=pregunta)

@app.route('/send',methods=['GET',"POST"])
def send():
    pregunta = request.form.get("salida")
    if not pregunta:
        error= "Por favor inserte su pregunta."
        return render_template('decision.html',error=error)

    n=4
    circuit = QuantumCircuit(n, n)
    for i in range(n):
        circuit.h(i)
    for i in range(n):
        circuit.measure(i,i)
    #IBMQ.load_account()
    #provider = IBMQ.get_provider('ibm-q')
    #quantum_computer = provider.get_backend('ibmq_belem')
    IBMQ.save_account("156b72ed1ffacc888c2cd317f7332b31fa5265d4ee58795bb48d47f3b0394279a9866c44acaa628756bae77e43d37b3fd39edd974da0329d72c93230269e3dc6", overwrite=True)
    provider= IBMQ.load_account()
    quantum_computer = provider.get_backend("ibmq_bogota")
    job = execute(circuit, quantum_computer, shots=1)
    counts = job.result().get_counts()
    op=["https://i.ibb.co/1YN0554/En-mi-opini-n-si.png","https://i.ibb.co/FHj7CX8/respuesta-esno.png","https://i.ibb.co/ctkQfXR/Est-decidido-que-si.png","https://i.ibb.co/4Vrdh8q/fuentes.png","https://i.ibb.co/XVtcGFY/apunta-qeusi.png","https://i.ibb.co/mBkbYg5/dudoso.png","https://i.ibb.co/zGN98tq/no.png",  "https://i.ibb.co/8DBLZV8/seramejorque.png",
    "https://i.ibb.co/XVJWksV/concentarte.png","https://i.ibb.co/txtsPxX/no-cuentes.png","https://i.ibb.co/jyhhFtL/cuenta-con-ello.png","https://i.ibb.co/GMnGG7P/Pronostico.png","https://i.ibb.co/ThKtg0G/pronostico-no-bueno.png","https://i.ibb.co/xMSTJbm/Sinduda.png","https://i.ibb.co/JxPjvhM/si.png","https://i.ibb.co/ccGq7Kg/defno.png"]
    #"https://upload.wikimedia.org/wikipedia/commons/e/eb/Magic_eight_ball.png"
   
    list=["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"]
    for k in range(16):
        if next(iter(counts.keys())) == list[k]:
            result = op[k]
            break
    bola = f"{result}" 
    return render_template('send.html',bola=bola, pregunta = pregunta)
    # if request.method == 'POST':
        #    data1 = request.form ['data1']  
        # magicball8.medicion()
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    #app.run (port = 5000)