from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates")
app.secret_key = 'pi2023_ihm_parte2'


# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdpi2.db'
db = SQLAlchemy(app)

# Modelo de dados


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nf = db.Column(db.String(20))
    motorista = db.Column(db.String(50))
    veiculo = db.Column(db.String(20))
    placa = db.Column(db.String(10))
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    uf = db.Column(db.String(20))


# Rota para página de início
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')


# Rota para a página de inserção


@app.route('/', methods=['GET', 'POST'])
def insert_data():
    if request.method == 'POST':
        nf = request.form['nf']
        motorista = request.form['motorista']
        veiculo = request.form['veiculo']
        placa = request.form['placa']
        cep = request.form['cep']
        logradouro = request.form['logradouro']
        numero = request.form['numero']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        uf = request.form['uf']

        data = Data(nf=nf, motorista=motorista, veiculo=veiculo, placa=placa, cep=cep,
                    logradouro=logradouro, numero=numero, bairro=bairro, cidade=cidade, uf=uf)
        db.session.add(data)
        db.session.commit()
        flash('Registro feito com sucesso', 'success')
    return render_template('index.html')

# Rota para a página de consulta


@app.route('/search', methods=['GET', 'POST'])
def search_data():
    if request.method == 'POST':
        query_param = request.form.get('query_param')
        search_value = request.form.get('search_value')

        if query_param and search_value:
            data = Data.query.filter(
                getattr(Data, query_param).contains(search_value)).all()
        else:
            data = Data.query.all()

        return render_template('search.html', data=data)

    return render_template('search.html')


if __name__ == '__main__':
    with app.app_context():  # Cria o contexto da aplicação
        db.create_all()
    app.run(debug=True)
