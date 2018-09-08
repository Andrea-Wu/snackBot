from wtforms import Form, TextField, SelectField, validators

class requestForm(Form):
    name = TextField(u"name", validators=[validators.DataRequired("Please enter your name")])
    location = SelectField(u"location", choices=[('Hogwarts', 'Hogwarts'), 
                            ('Hell', 'Hell'), 
                            ('Henry\'s Diner', 'Henry\'s Diner')], validators=[validators.required()]) 
    snack = SelectField(u"snack", choices=[('Doritos', 'Doritos'),
                                        ('Lays', 'Lays'),
                                        ('Pretzels', 'Pretzels')], validators=[validators.required()])

# Heman's robot form
class roboForm(Form):
    l = TextField(u"l", validators=[validators.DataRequired("Please enter left ping sensor"), validators.NumberRange()])
    r = TextField(u"r", validators=[validators.DataRequired("Please enter right ping sensor"), validators.NumberRange()])
    ok = TextField(u"ok", validators=[validators.AnyOf('True', 'False')])
