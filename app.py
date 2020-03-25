import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'paskaitos.db?check_same_thread=False')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

association_table = db.Table('association', db.metadata,
    db.Column('studentas_id', db.Integer, db.ForeignKey('studentas.id')),
    db.Column('paskaita_id', db.Integer, db.ForeignKey('paskaita.id'))
)

class Studentas(db.Model):
    __tablename__ = 'studentas'
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String)
    pavarde = db.Column("Pavardė", db.String)
    paskaitos = db.relationship("Paskaita", secondary=association_table,
                          back_populates="studentai")

class Paskaita(db.Model):
    __tablename__ = 'paskaita'
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column("Pavadinimas", db.String)
    studentai = db.relationship("Studentas", secondary=association_table,
                         back_populates="paskaitos")
    destytojas_id = db.Column(db.Integer, db.ForeignKey("destytojas.id"))
    destytojas = db.relationship("Destytojas")

class Destytojas(db.Model):
    __tablename__ = 'destytojas'
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String)
    pavarde = db.Column("Pavardė", db.String)
    paskaitos = db.relationship("Paskaita")


@app.route("/")
def index():
    return destytojai()

@app.route("/destytojai")
def destytojai():
    try:
        destytojai = Destytojas.query.all()
    except:
        destytojai = []
    return render_template("destytojai.html", destytojai=destytojai)


@app.route("/naujas_destytojas", methods=["GET", "POST"])
def naujas_destytojas():
    db.create_all()
    forma = forms.DestytojasForm()
    if forma.validate_on_submit():
        naujas_destytojas = Destytojas(vardas=forma.vardas.data, pavarde=forma.pavarde.data)
        for paskaita in forma.paskaitos.data:
            priskirta_paskaita = Paskaita.query.get(paskaita.id)
            naujas_destytojas.paskaitos.append(priskirta_paskaita)
        db.session.add(naujas_destytojas)
        db.session.commit()
        return redirect(url_for('destytojai'))
    return render_template("prideti_destytoja.html", form=forma)


@app.route("/studentai")
def studentai():
    try:
        visi_studentai = Studentas.query.all()
    except:
        visi_studentai = []
    return render_template("studentai.html", visi_studentai=visi_studentai)


@app.route("/naujas_studentas", methods=["GET", "POST"])
def naujas_studentas():
    db.create_all()
    forma = forms.StudentasForm()
    if forma.validate_on_submit():
        naujas_studentas = Studentas(vardas=forma.vardas.data,
                               pavarde=forma.pavarde.data)
        for paskaita in forma.paskaitos.data:
            priskirta_paskaita = Paskaita.query.get(paskaita.id)
            naujas_studentas.paskaitos.append(priskirta_paskaita)
        db.session.add(naujas_studentas)
        db.session.commit()
        return redirect(url_for('studentai'))
    return render_template("prideti_studenta.html", form=forma)

@app.route("/paskaitos")
def paskaitos():
    try:
        visos_paskaitos = Paskaita.query.all()
    except:
        visos_paskaitos = []
    return render_template("paskaitos.html", visos_paskaitos=visos_paskaitos)



@app.route("/nauja_paskaita", methods=["GET", "POST"])
def nauja_paskaita():
    db.create_all()
    forma = forms.PaskaitaForm()
    if forma.validate_on_submit():
        nauja_paskaita = Paskaita(pavadinimas=forma.pavadinimas.data, destytojas_id=forma.destytojas.data.id)
        for studentas in forma.studentai.data:
            priskirtas_studentas = Studentas.query.get(studentas.id)
            nauja_paskaita.studentai.append(priskirtas_studentas)
        db.session.add(nauja_paskaita)
        db.session.commit()
        return redirect(url_for('paskaitos'))
    return render_template("prideti_paskaita.html", form=forma)
#
# @app.route("/delete/<int:id>")
# def delete(id):
#     uzklausa = Tevas.query.get(id)
#     db.session.delete(uzklausa)
#     db.session.commit()
#     return redirect(url_for('parents'))
#
# @app.route("/update/<int:id>", methods=['GET', 'POST'])
# def update(id):
#     form = forms.TevasForm()
#     tevas = Tevas.query.get(id)
#     if form.validate_on_submit():
#         tevas.vardas = form.vardas.data
#         tevas.pavarde = form.pavarde.data
#         tevas.vaikai.clear()
#         for vaikas in form.vaikai.data:
#             priskirtas_vaikas = Vaikas.query.get(vaikas.id)
#             tevas.vaikai.append(priskirtas_vaikas)
#         db.session.commit()
#         return redirect(url_for('parents'))
#     return render_template("tevas_update.html", form=form, tevas=tevas)
#
# @app.route("/vaikas_delete/<int:id>")
# def vaikas_delete(id):
#     uzklausa = Vaikas.query.get(id)
#     db.session.delete(uzklausa)
#     db.session.commit()
#     return redirect(url_for('parents'))
#
# @app.route("/vaikas_update/<int:id>", methods=['GET', 'POST'])
# def vaikas_update(id):
#     form = forms.VaikasForm()
#     vaikas = Vaikas.query.get(id)
#     if form.validate_on_submit():
#         vaikas.vardas = form.vardas.data
#         vaikas.pavarde = form.pavarde.data
#         vaikas.tevai = []
#         for tevas in form.tevai.data:
#             priskirtas_tevas = Tevas.query.get(tevas.id)
#             tevas.vaikai.append(priskirtas_tevas)
#         db.session.commit()
#         return redirect(url_for('children'))
#     return render_template("vaikas_update.html", form=form, vaikas=vaikas)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()