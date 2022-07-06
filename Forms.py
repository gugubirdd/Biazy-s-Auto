from wtforms import Form, StringField, SelectField, validators, TextAreaField, FloatField, DateField, RadioField, TimeField, DecimalField
from wtforms.fields import EmailField, PasswordField, IntegerField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import ValidationError
import datetime


class Register(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    title = SelectField('Title', [validators.DataRequired(message='This is a required field.')], choices=['', 'Mr', 'Ms', 'Mrs'], default='')
    phone = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(message='This is a required field.')])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.'), validators.Email(message='Please enter a valid email')])
    password = PasswordField('Password', [validators.Length(min=8, max=20, message='Passwords must be between 8 to 20 characters'), validators.DataRequired(), validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message='Weak Password, must contain a mix of lowercase, uppercase, number and special character')])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.EqualTo('password', message='Passwords must match'), validators.DataRequired(message='This is a required field.')])


class CarRegister(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    title = SelectField('Title', [validators.DataRequired(message='This is a required field.')], choices=['', 'Mr', 'Ms', 'Mrs'], default='')
    phone = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(message='This is a required field.')])
    email = EmailField('Email', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.'), validators.Email(message='Please enter a valid email')])
    password = PasswordField('Password', [validators.Length(min=8, max=20, message='Passwords must be between 8 to 20 characters'), validators.DataRequired(message='This is a required field.'), validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message='Weak Password')])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.EqualTo('password', message='Passwords must match'), validators.DataRequired(message='This is a required field.')])
    make = StringField('Car Make', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    model = StringField('Car Model', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])


class Login(Form):
    email = StringField('Email', [validators.Length(min=1, max=50), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=50), validators.DataRequired()])


class Update(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    title = SelectField('Title', [validators.DataRequired(message='This is a required field.')], choices=['', 'Mr', 'Ms', 'Mrs'], default='')
    phone = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(message='This is a required field.')])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.'), validators.Email(message='Please enter a valid email')])


class CarUpdate(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])
    title = SelectField('Title', [validators.DataRequired(message='This is a required field.')], choices=['', 'Mr', 'Ms', 'Mrs'], default='')
    phone = StringField('Phone Number', [validators.Length(min=8, max=8), validators.DataRequired(message='This is a required field.')])
    email = EmailField('Email', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.'), validators.Email(message='Please enter a valid email')])
    make = StringField('Car Make', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    model = StringField('Car Model', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])


class ChangePassword(Form):
    old_password = PasswordField('Enter your Old Password', [validators.Length(min=1, max=50), validators.DataRequired()])
    new_password = PasswordField('Enter your New Password', [validators.Length(min=8, max=20, message='Passwords must be between 8 to 20 characters'), validators.DataRequired(message='This is a required field.'), validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message='Weak Password')])
    confirm_new_password = PasswordField('Confirm your New Password', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.')])


class ProfilePic(Form):
    profilepic = FileField(validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])


class ForgetPassword(Form):
    email = EmailField('Email Address', [validators.Length(min=1, max=150), validators.DataRequired(message='This is a required field.'), validators.Email(message='Please enter a valid email')])


class CreateAdmin(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    position = SelectField('Position', [validators.DataRequired(message='This is a required field.')], choices=['', 'Accounts', 'Events', 'Products', 'Services', 'Accessories'], default='')
    email = StringField('Email', [validators.Length(min=1, max=50), validators.DataRequired(message='This is a required field.')])
    password = PasswordField('Password', [validators.Length(min=8, max=20, message='Passwords must be between 8 to 20 characters'), validators.DataRequired(), validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", message='Weak Password')])
    confirm_password = PasswordField('Confirm Password', [validators.Length(min=1, max=150), validators.EqualTo('password', message='Passwords must match'), validators.DataRequired(message='This is a required field.')])


class CreateCarForm(Form):
    car_name = StringField('Car Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    car_model = StringField('Car Model', [validators.Length(min=1, max=150), validators.DataRequired()])
    car_description = TextAreaField('Car Description', [validators.DataRequired()])
    car_price = FloatField('Price (S$)', [validators.NumberRange(min=1, max=5000000), validators.DataRequired()])
    car_quantity = IntegerField('Quantity', [validators.NumberRange(min=0, max=500), validators.InputRequired()])
    car_availstartdate = DateField('Date', [validators.DataRequired()])
    car_availability = SelectField('Availability', [validators.DataRequired()], choices=[('Auto','Auto'), ('In Stock','In Stock'), ('Out-of-Stock','Out-of-Stock'), ('Unavailable','Unavailable')], default='Auto')
    def validate_car_availstartdate(form, field):
        if field.data < datetime.date.today():
            raise ValidationError('Date cannot be in the past')


class CreateElectricCarForm(Form):
    car_name = StringField('Car Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    car_model = StringField('Car Model', [validators.Length(min=1, max=150), validators.DataRequired()])
    car_description = TextAreaField('Car Description', [validators.DataRequired()])
    car_price = FloatField('Price (S$)', [validators.NumberRange(min=1, max=5000000), validators.DataRequired()])
    car_quantity = IntegerField('Quantity', [validators.NumberRange(min=0, max=500), validators.InputRequired()])
    car_availstartdate = DateField('Date', [validators.DataRequired()])
    car_availability = SelectField('Availability', [validators.DataRequired()], choices=[('Auto', 'Auto'), ('In Stock', 'In Stock'), ('Out-of-Stock', 'Out-of-Stock'), ('Unavailable', 'Unavailable')], default='Auto')
    car_battery_capacity = IntegerField('Battery Capacity (kWh)', [validators.NumberRange(min=1, max=120), validators.DataRequired()])
    car_charging_duration = IntegerField('Charging Duration (hr)', [validators.NumberRange(min=1, max=24), validators.DataRequired()])

    def validate_car_availstartdate(form, field):
        if field.data < datetime.date.today():
            raise ValidationError('Date cannot be in the past')


class CreateServiceForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    availability = RadioField('Availability', choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')],
                            default='A')


class CreateCarserviceForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    location = TextAreaField('Location')
    hotline = TextAreaField('Hotline', [validators.DataRequired()])
    starting_hour = TimeField('Starting hour')
    ending_hour = TimeField('Ending hour')
    opening_days = StringField('Opening days', [validators.DataRequired()])
    availability = RadioField('Availability', choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')],
                    default='A')


class createInternalEventForm(Form):
    startDate = DateField('Start Date', [validators.InputRequired()])
    endDate = DateField('End Date', [validators.InputRequired()])
    startTime = TimeField('Start Time', [validators.InputRequired()])
    endTime = TimeField('End Time', [validators.InputRequired()])
    venue = StringField('Venue', [validators.InputRequired()])
    cost = FloatField('Cost $', [validators.optional(), validators.NumberRange(min=0, message='Cost cannot be a negative value!')])
    capacity = IntegerField('Capacity', [validators.InputRequired(), validators.NumberRange(min=0, message='Capacity cannot be a negative value!')])
    title = StringField('Title', [validators.InputRequired()])
    fullname = StringField('In Charge', [validators.DataRequired()])
    attendance = SelectField('Department', [validators.DataRequired()], choices=[('All Departments', 'All Departments'), ('Production', 'Production'), ('R&D', 'R&D'), ('Marketing', 'Marketing'), ('HR', 'HR'), ('Accounting & Financial', 'Accounting & Financial'), ('IT', 'IT')])

    def validate_endDate(form, field):
        if field.data < form.startDate.data:
            raise ValidationError("End date must not be earlier than start date.")
        elif field.data < datetime.date.today():
            raise ValidationError('Date cannot be in the past.')



class createPublicEventForm(Form):
    startDate = DateField('Start Date', [validators.InputRequired()])
    endDate = DateField('End Date', [validators.InputRequired()])
    startTime = TimeField('Start Time', [validators.InputRequired()])
    endTime = TimeField('End Time', [validators.InputRequired()])
    venue = StringField('Venue', [validators.InputRequired()])
    cost = FloatField('Cost $', [validators.optional(), validators.NumberRange(min=0, message='Cost cannot be a negative value!')])
    capacity = IntegerField('Capacity', [validators.InputRequired(), validators.NumberRange(min=0, message='Capacity cannot be a negative value!')])
    title = StringField('Title', [validators.InputRequired()])

    def validate_endDate(form, field):
        if field.data < form.startDate.data:
            raise ValidationError("End date must not be earlier than start date.")
        elif field.data < datetime.date.today():
            raise ValidationError('Date cannot be in the past.')


Choices = "Auto", "In Stock", "Out of Stock", "Unavailable"
Choices2 = "AA", "AAA", "AAAA", "C", "D", "9V", "CR123A", "23A", "CR2032", "Solar"
Choices3 = "0", "1", "2", "3", "4"


class CreateAccessoryForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    price = DecimalField('Price', [validators.NumberRange(min=0.01, max=100000), validators.InputRequired()])
    quantity = IntegerField('Quantity', [validators.NumberRange(min=0, max=10000), validators.InputRequired()])
    start = DateField('Available After', [validators.DataRequired()])
    end = DateField('Not Available After (Optional)', validators=(validators.Optional(),))
    status = SelectField('Status', [validators.DataRequired()], choices=Choices)

    def validate_end(form, field):
        if field.data < form.start.data:
            raise ValidationError("End date must not be earlier than start date!")
        elif field.data < datetime.date.today():
            raise ValidationError("Date must not be in the past!")

    def validate_start(form, field):
        if field.data < datetime.date.today():
            raise ValidationError("Date must not be in the past!")


class CreateElectronicAccessoryForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    price = DecimalField('Price', [validators.NumberRange(min=0.01, max=100000), validators.InputRequired()])
    quantity = IntegerField('Quantity', [validators.NumberRange(min=0, max=10000), validators.InputRequired()])
    start = DateField('Available After', [validators.DataRequired()])
    end = DateField('Not Available After (Optional)', validators=(validators.Optional(),))
    status = SelectField('Status', [validators.DataRequired()], choices=Choices)
    battery_type = SelectField('Battery Type', [validators.DataRequired()], choices=Choices2)
    batteries_required = SelectField('Batteries Required', [validators.DataRequired()], choices=Choices3)

    def validate_end(form, field):
        if field.data < form.start.data:
            raise ValidationError("End date must not be earlier than start date!")
        elif field.data < datetime.date.today():
            raise ValidationError("Date must not be in the past!")

    def validate_start(form, field):
        if field.data < datetime.date.today():
            raise ValidationError("Date must not be in the past!")
