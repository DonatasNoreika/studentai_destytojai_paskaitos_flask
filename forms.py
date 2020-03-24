from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import app


class StudentasForm(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    paskaitos = QuerySelectMultipleField(query_factory=app.Paskaita.query.all, get_label="pavadinimas",
                                         get_pk=lambda obj: str(obj))
    submit = SubmitField('Įvesti')


class PaskaitaForm(FlaskForm):
    pavadinimas = StringField('Pavadinimas', [DataRequired()])
    studentai = QuerySelectMultipleField(query_factory=app.Studentas.query.all, get_label="vardas",
                                         get_pk=lambda obj: str(obj))
    submit = SubmitField('Įvesti')


class DestytojasForm(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    pavarde = StringField('Pavardė', [DataRequired()])
    paskaitos = QuerySelectMultipleField(query_factory=app.Paskaita.query.all, get_label="pavadinimas",
                                         get_pk=lambda obj: str(obj))
    submit = SubmitField('Įvesti')
