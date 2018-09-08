from wtforms import Form, TextField, SelectField, validators

class requestForm(Form):
    name = TextField(u"name", validators=[validators.DataRequired("Please enter your name")])
    location = SelectField(u"location", choices=[('Hogwarts', 'Hogwarts'), 
                            ('Hell', 'Hell'), 
                            ('Henry\'s Diner', 'Henry\'s Diner')], validators=[validators.required()]) 
    snack = SelectField(u"snack", choices=[('Doritos', 'Doritos'),
                                        ('Lays', 'Lays'),
                                        ('Pretzels', 'Pretzels')], validators=[validators.required()])


