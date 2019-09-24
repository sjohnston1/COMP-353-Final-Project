from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Login, Employee, Department, StatusOf, Items, ItemType
from wtforms.fields.html5 import DateField

#used to display the choices for deparment number
depChoice = Department.query.with_entities(Department.DepartmentID, Department.Departmentname).distinct()
myDepChoices2 = [(row[0], row[0]) for row in depChoice]
results=list()
for row in depChoice:
    rowDict = row._asdict()
    results.append(rowDict)
myDepChoices = [(row['DepartmentID'],row['Departmentname']) for row in results]

statusChoice = StatusOf.query.with_entities(StatusOf.StatusID, StatusOf.Statusof).distinct()
myStatusChoices2 = [(row[0], row[0]) for row in statusChoice]
results=list()
for row in statusChoice:
    rowDict = row._asdict()
    results.append(rowDict)
myStatusChoices = [(row['StatusID'],row['Statusof']) for row in results]

typeChoice = ItemType.query.with_entities(ItemType.ItemID, ItemType.Itemname).distinct()
myTypeChoices2 = [(row[0], row[0]) for row in typeChoice]
results=list()
for row in typeChoice:
    rowDict = row._asdict()
    results.append(rowDict)
myTypeChoices = [(row['ItemID'],row['Itemname']) for row in results]

'''numChoice = Employee.query.with_entities(Employee.Employeenumber).distinct()
myNumChoices2 = [(row[0], row[0]) for row in numChoice]
results=list()
for row in numChoice:
    rowDict = row._asdict()
    results.append(rowDict)
myNumChoices = [(row['Employeenumber'],row['Employeenumber']) for row in results]'''

class RegistrationForm(FlaskForm):
    employeeNumber = IntegerField('Employee Number', validators=[DataRequired()])
    employeeName = StringField('Employee Name', validators=[DataRequired()])
    employeeAddress = StringField('Employee Address', validators=[DataRequired()])
    employeeCity = StringField('Employee City', validators=[DataRequired()])
    employeeState = StringField('Employee State', validators=[DataRequired()])
    employeeZip = IntegerField('Employee Zip', validators=[DataRequired()])
    employeeBirthDate = DateField('Employee Birth Date', validators=[DataRequired()])
    employeeDepartmentID = SelectField('Department ID', choices=myDepChoices, coerce=int)
    loginid = StringField('LoginID',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_employeeNumber(self, employeeNumber):
        user = Employee.query.filter_by(Employeenumber=employeeNumber.data).first()
        if user:
            raise ValidationError('That Employee Number has already been registered. Please choose a different one.')

    def validate_employeeLoginID(self, loginid):
        user = Login.query.filter_by(LoginID=loginid.data).first()
        if user:
            raise ValidationError('That LoginID has already been used. Please choose a different one.')

class LoginForm(FlaskForm):
    loginid = StringField('LoginID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NewAssetForm(FlaskForm):
    serialNumber = StringField('Serial Number', validators=[DataRequired()])
    assetNumber = IntegerField('Asset Number', validators=[DataRequired()])
    introductionDate = DateField('Date of Introduction', validators=[DataRequired()])
    orderDate = DateField('Order Date', validators=[DataRequired()])
    statusID = SelectField('StatusID', choices=myStatusChoices)
    modelNumber = StringField('Model Number', validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    itemID = SelectField('Item Type', choices=myTypeChoices, coerce=int)
    submit = SubmitField('Add New Item')

    def validate_assetNumber(self, assetNumber):
        item = Items.query.filter_by(Assetnumber=assetNumber.data).first()
        if item:
            raise ValidationError('That Asset Number has already been registered. Please choose a different one.')

class CheckoutForm(FlaskForm):
    checkoutDate = DateField('Date Requested', validators=[DataRequired()])
    checkinDate = DateField('Date to Return By', validators=[DataRequired()])
    assetNumber = HiddenField('')
    employeeNumber = IntegerField('Your employee number', validators=[DataRequired()])
    submit = SubmitField('Put in request for item!')

    def validate_check(self, employeeNumber):
        check = 1

class OptionForm(FlaskForm):
    checkoutDate = HiddenField('')
    checkinDate = HiddenField('')
    assetNumber = HiddenField('')
    employeeNumber = HiddenField('')
    submit = SubmitField('Approve this request!')

    def validate_options(self):
        check = 1