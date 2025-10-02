import csv
from os import environ
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from wtforms.validators import DataRequired, URL
from wtforms import StringField, SubmitField, URLField, SelectField

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = environ["SECRET_KEY"]
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening_time = StringField('Opening time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing time e.g. 8PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=[('✘', '✘'), ('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'),
                                         ('☕☕☕☕','☕☕☕☕'), ('☕☕☕☕☕','☕☕☕☕☕')],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating',
                              choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'),
                                       ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')],
                              validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Outlet Rating',
                                      choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'),
                                               ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')],
                                      validators=[DataRequired()])
    submit = SubmitField('Submit')

def read_csv_file() -> list[str]:
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return list_of_rows

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8') as file:
            file.write('\n')
            file.write(f"{form.cafe.data},{form.cafe_location.data},{form.opening_time.data},"
                           f"{form.closing_time.data},{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},{form.power_outlet_rating.data}")
        list_of_rows = read_csv_file()
        len_cafes = len(list_of_rows)
        return render_template('cafes.html', cafes=list_of_rows, len=len_cafes)
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    list_of_rows = read_csv_file()
    len_cafes = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, len=len_cafes)

if __name__ == '__main__':
    app.run(debug=True)