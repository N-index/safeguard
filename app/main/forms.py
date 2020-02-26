from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email, NumberRange, Regexp, Length

from app.models import User


class RegisterForm(FlaskForm):
    device_id = StringField('Device ID? *', validators=[DataRequired()], render_kw={'placeholder': 'xxxx--xxxx-xxxx'})
    username = StringField('What’s your name? *', validators=[DataRequired()])
    age = IntegerField('Age? *', validators=[DataRequired(), NumberRange(0, 150, 'You ghost?')])

    gender = RadioField('Gender? *',
                        choices=[('0', 'male'), ('1', 'female')],
                        validators=[DataRequired()],
                        render_kw={'class': 'radiobutton'})
    height = IntegerField('Height? (cm) *', validators=[DataRequired(), NumberRange(2, 300, 'Too short or too high.')])
    weight = FloatField('Weight? (kg) *', validators=[DataRequired(),
                                                      NumberRange(1, 600, 'Too light or too heavy. Go to the doctor.')])
    telephone = StringField('Phone number? * ',
                            validators=[DataRequired(), Length(0, 15, 'Too short or too long.'),
                                        Regexp('^[0-9][0-9]*$', 0, 'Invalid phone number.')])
    email = StringField('Email? * ', validators=[DataRequired(), Email()])
    submit = SubmitField('Activate device and Register user', render_kw={'class': 'btn btn-block'})

    def validate_device_id(self, field):
        if User.query.filter_by(device_id=field.data).first():
            raise ValidationError('This device has been registered.')

    # def validate_height(self, field):
    #     if int(field.data) < 5 or int(field.data) > 500:
    #         raise ValidationError('The height is abnormal.')
    #
    # def validate_weight(self, field):
    #     if int(field.data) < 1 or int(field.data) > 600:
    #         raise ValidationError('The weight is abnormal.')
