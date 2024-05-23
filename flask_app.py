from flask import Flask, render_template, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import qrcode
import io
import base64

class URLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Generovat QR kód')

app = Flask(__name__)
app.debug = True
app.secret_key = 'be fe le me pes se veze' 

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return img_base64

@app.route('/zadej', methods=['GET', 'POST'])
def start():
    url = session.get('url')
    qr_code_img = None
    if url:
        qr_code_img = generate_qr_code(url)
    return render_template('index.html', finalURL=url, qr_code_img=qr_code_img)

@app.route('/', methods=['GET', 'POST'])
def zadejurl():
    form = URLForm()
    if form.validate_on_submit():
        session['url'] = form.url.data
        return redirect(url_for('start'))
    return render_template('zadejURL.html', form=form)

if __name__ == '__main__':
    app.run()
