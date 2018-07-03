from flask import Flask, render_template
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask import flash, request
from wtforms import Form, TextField, TextAreaField, validators, SubmitField
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    ssid = StringField('WiFi SSID', validators=[DataRequired()])
    key = PasswordField('WiFi Key', validators=[DataRequired()])
    zoneid = StringField('Zone ID', validators=[DataRequired()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    import subprocess
    form = ReusableForm(request.form)
 

    if request.method == 'POST':
        ssid=request.form['ssid']
        key=request.form['key']
        zoneid=request.form['zoneid']
 
        if form.validate():
            # Save the comment here.

            target = '\nnetwork={\n\tssid=\"' +  ssid + '\"\n\tpsk=\"' + key + '\"\n\tpriority=10\n}\n'
            print(target)
            subprocess.call(["sudo", "systemctl", "stop", "hostapd"])
            subprocess.call(["sudo", "sh", "-c", "\"echo", "\'", target, "\'", ">>", "/etc/wpa_supplicant/wpa_supplicant.conf\""])
            subprocess.call(["sudo", "systemctl", "restart", "dhcpcd"])
            
        else:
            flash('All the form fields are required. ')
            print('All the form fields are required. ')
 
    return render_template('form.html', form=form)

if __name__ == "__main__":
    app.run()
