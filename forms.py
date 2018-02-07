from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField, PasswordField, DateField, FileField, DecimalField, FormField, SelectMultipleField

from wtforms import validators, ValidationError

hexaPattern = r"^--[0-9a-fA-F]+(--)?\s"

class UserDataForm(FlaskForm):
    firstName = TextField("First Name",[validators.Required("First name cannot be blank")])
    lastName = TextField("Last Name",[validators.Required("Last name cannot be blank")])
    addressLine1 = TextField("Address line1:",[validators.Required("Address cannot be blank.")])
    addressLine2 = TextField("Address line2:",)
    city = TextField("City", [validators.Required("City cannot be blank")])
    state = SelectField("State", choices = [
('Alabama','AL'),
('Alaska','AK'),
('Arizona','AZ'),
('Arkansas','AR'),
('California','CA'),
('Colorado','CO'),
('Connecticut','CT'),
('Delaware','DE'),
('Florida','FL'),
('Georgia','GA'),
('Hawaii','HI'),
('Idaho','ID'),
('Illinois','IL'),
('Indiana','IN'),
('Iowa','IA'),
('Kansas','KS'),
('Kentucky','KY'),
('Louisiana','LA'),
('Maine','ME'),
('Maryland','MD'),
('Massachusetts','MA'),
('Michigan','MI'),
('Minnesota','MN'),
('Mississippi','MS'),
('Missouri','MO'),
('Montana','MT'),
('Nebraska','NE'),
('Nevada','NV'),
('NewHampshire','NH'),
('NewJersey','NJ'),
('NewMexico','NM'),
('NewYork','NY'),
('NorthCarolina','NC'),
('NorthDakota','ND'),
('Ohio','OH'),
('Oklahoma','OK'),
('Oregon','OR'),
('Pennsylvania','PA'),
('RhodeIsland','RI'),
('SouthCarolina','SC'),
('SouthDakota','SD'),
('Tennessee','TN'),
('Texas','TX'),
('Utah','UT'),
('Vermont','VT'),
('Virginia','VA'),
('Washington','WA'),
('WestVirginia','WV'),
('Wisconsin','WI'),
('Wyoming','WY')
])
    zipcode = TextField("PostalCode",[validators.Required("please enter postal code"), validators.regexp(u'^[0-9]{5}')])
    email = TextField("Email",[validators.Required("Please enter your email address"), validators.Email("Please enter a valid email address.")])

class DirectorForm(FlaskForm):
    email = TextField("Email",[validators.Required("Please enter your email address"), validators.Email("Please enter a valid email address.")])
    password = PasswordField("Enter Password",[validators.Required("password cannot be blank"), validators.Length(min=6, max=24, message="password must be at least 6 characters, not more than 24"), validators.EqualTo('password', message="password and confirmed password must match!")])
    confirm = PasswordField("Confirm Password",) 
    submit = SubmitField("Submit")

class AdminForm(FlaskForm):
    email = TextField("Email",[validators.Required("Please enter your email address"), validators.Email("Please enter a valid email address.")])
    update = SubmitField(u"Update Director Data")

class SettingsForm(FlaskForm):
    email = TextField("Email",[validators.Required("Please enter your email address"), validators.Email("Please enter a valid email address.")])
    pwChange = SubmitField(u"Change Password")

class PwForm(FlaskForm):
    oldPassword = PasswordField("Enter Old Password",)
    password = PasswordField("Enter Password",[validators.Required("password cannot be blank"), validators.Length(min=6, max=24, message="password must be at least 6 characters, not more than 24"), validators.EqualTo('password', message="password and confirmed password must match!")])
    confirm = PasswordField("Confirm Password",) 
    update = SubmitField(u"Update Password")
    cancel = SubmitField(u"Cancel")

class DirectorConfirmForm(FlaskForm):
    message = 'A confirmation email has been sent to' 
    
class DashboardForm(FlaskForm):
    message = ""

class ListForm(FlaskForm):
    message = ""

class DetailForm(FlaskForm):
    message = ""

class SlideForm(DetailForm):
    message = ""

class EditForm(FlaskForm):
    message = ""
    videoName = TextField("Video Name",[validators.Required("A video name is required")], default = 'A Video Named Nothing')
    imageName = TextField("Image Name",[validators.Required("An image name is required")], default = 'An Image Named Nothing')
    chooseVideo = FileField(u'Video File')
    chooseImage = FileField(u'Image File')
    timeTarget = DecimalField(u'Target time', [validators.required("duration must be specified"), validators.NumberRange(min = -0.02, max = 1000.00, message=u'values between 0.00 and - 10000.00 are allowed')], places = 2, rounding=None, default = 1.00)
    go =  SubmitField(u'Go to Time')
    imageOptions = SelectField("Image Operations", choices = [(u'0', "Crop"),(u'1', "Flip"), (u'2', "Resize"),(u'3', "Blur")])
    execute =  SubmitField(u'Execute')
    saveVideo =  SubmitField(u'SaveVideo')
    saveImage =  SubmitField(u'SaveImage')
    storeFrame = SubmitField(u'Store Frame')

class SlideShowForm(DetailForm):
    message = ""
    showName = TextField("Show Name",[validators.Required("A show name is required")])
    slideCount = IntegerField(u'Total Slides', default = 1)
    slideIndex = IntegerField(u'Current Slide Number', default = 1)
    slideType = SelectField("Slide Show Type", choices = [(u'0', "Text"),(u'1', "Images in Pixies - Roulette"), (u'2', "Images in Pixies - Wave"),(u'3', "Images on Pixies")])
    slideImage = FileField(u'Image File')
    slideText = TextField(u'Slide Text')
    durationInSeconds = DecimalField(u'Slide Duration in Seconds', [validators.required("duration must be specified"), validators.NumberRange(min = -1.00, max = 50.00, message=u'values between 0.02 and - 50.00 are allowed')], places = 2, rounding=None, default = 0.5)
    panSpeed = IntegerField(u'Pan speed frames/sec', [validators.NumberRange(min = -50, max = 50, message="values between 50 and - 50 are allowed")], default = 1)
    pan = SelectField(u'Pan Type', choices = [(u'0', u'By columns'),(u'1', u'By character'), (u'2', u'By word')])    
    scrollSpeed = IntegerField(u'Scroll speed frames/sec', [validators.NumberRange(min = -50, max = 50, message="values between 50 and - 50 are allowed")], default = 1)
    scroll = SelectField(u'Scroll Type', choices = [(u'0', u'By rows'),(u'1', u'By character'), (u'2', u'By word')])
    foregroundColors = TextField(u'Color of the letters - (Hex(0 - FF) Red,Green,Blue)', [validators.Length(min=1, max = 6, message="Letter color must be 6 digits"), validators.regexp(u'^[0-9a-fA-F]{1,6}')], default = u'FFFFFF')
    backgroundColors = TextField(u'Color of the background - (Hex(0 - FF) Red,Green,Blue)', [validators.Length(min=1, max = 6, message="Letter color must be 6 digits"),validators.regexp(u'^[0-9a-fA-F]{1,6}')], default = u'000000')
    repetition = IntegerField(u'Repetitions of this slide', [validators.required("repetition must be specified"), validators.NumberRange(min = 1, max = 99, message=u'values between 0 -99 are allowed for repetitions')], default = 2)
    textInPixies = SelectField(u'Text displayed on pixies', choices=[(u'False', u'No'),(u'True', u'Yes')], default = u'False')
    prevSlide = SubmitField(u'<<')
    nextSlide = SubmitField(u'>>')
    showList = SubmitField(u'Open SlideShow List')
    storeShow = SubmitField(u'Save')
    newShow = SubmitField(u'Save New') 
    add = SubmitField(u'Add Slide')
    delete = SubmitField(u'Delete Slide')
    image = SubmitField(u'Change Image')


class CustomImageForm(FlaskForm):
    message = ""

class SlideShowImagesForm(SlideShowForm):
    message = ""

class SlideShowVideoForm(SlideShowForm):
    message = ""

class SlideShowPreviewForm(DetailForm):
    message = ""
    showName = TextField('ShowName',[validators.Required('SlideShow Identifier is Required')])

class EventForm(DetailForm):
    message = ""
    eventName = TextField('Event Name',[validators.Required('Event Name is required')], default = "")
    eventDate = DateField('Event Date', format='%Y-%m-%d', default ="")
    audienceRows = IntegerField(u'Rows in Audience', default = 10)
    audienceSeatsPerRow = IntegerField(u'Seats Per Row', default = 10)
    selectedSlideShows = SelectMultipleField('Selected Slide Shows', choices = [("create", "new")])
    availableSlideShows = SelectMultipleField('Available Slide Shows', choices=[("create","new")])
    add = SubmitField(u'>>')
    remove = SubmitField(u'<<')    
    eventList = SubmitField(u'Event List')
    saveEvent = SubmitField(u'Save')
    newEvent = SubmitField(u'Save As New')
    deleteEvent = SubmitField(u'Delete Event')

class SubDiectorForm(DetailForm):
    message = ""

class LoginForm(FlaskForm):
    username = TextField('User Name',[validators.Required('User Name is required')])
    password = PasswordField('password', [validators.DataRequired('Password is required')])
    submit = SubmitField("Login")
    create = SubmitField("Register")


