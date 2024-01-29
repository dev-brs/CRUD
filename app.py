from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:b2005@localhost/bd-alunos'
db = SQLAlchemy(app)


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/cadastrar")
def cadastrar():
    return render_template('cadastro.html')


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get("nome")

        ultimo_id = Aluno.query.order_by(Aluno.id_aluno.desc()).first()

        if ultimo_id:
            novo_id = ultimo_id.id_aluno + 1
        else:
            novo_id = 1

        nova_matricula = f"2024{str(novo_id).zfill(4)}"

        if nome:
            aluno = Aluno(nome, nova_matricula)
            db.session.add(aluno)
            db.session.commit()

    return redirect(url_for('index'))


@app.route("/consulta",methods=['GET'])
def consulta():
    alunos = Aluno.query.all()

    return render_template('consulta.html',alunos=alunos)


@app.route("/deletar/<int:id>")
def deletar(id):
    aluno = Aluno.query.filter_by(id_aluno=id).first()

    if aluno:
        db.session.delete(aluno)
        db.session.commit()

    alunos = Aluno.query.all()

    return render_template('consulta.html', alunos=alunos)


@app.route("/voltar")
def voltar():
    return redirect(url_for('index'))


@app.route("/atualizar/<int:id>", methods=['POST','GET'])
def atualizar(id):
    aluno = Aluno.query.filter_by(id_aluno=id).first()

    if request.method == 'POST':
        nome = request.form.get("nome")
        if nome:
            aluno.nome = nome

        db.session.commit()
        return redirect(url_for("consulta"))

    return render_template("atualizar.html", aluno = aluno)


if __name__ == '__main__':
    app.run(debug=True)
