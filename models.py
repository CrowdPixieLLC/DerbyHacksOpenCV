#directorMain models.py

from mongoengine import *

#from djangotoolbox.fields import ListField


class SlideTest(Document):
	objectId = StringField()
	slideIndex = IntField()
	durationInSeconds = ListField(IntField())
	showName = StringField(max_length=120)
	pan = ListField(IntField())
	panSpeed = ListField(IntField())
	textInPixies = ListField(BooleanField())
	slideType = IntField()
	author = StringField(max_length=200)
	scroll = ListField(IntField())
	scrollSpeed = ListField(IntField())
	repetition = ListField(IntField())
	foregroundColors = ListField(IntField())
	backgroundColors = ListField(IntField())
	slideCount = ListField(IntField())
	slideText = StringField(max_length=10000)

	class Meta: 
		ordering = ["-showName"]

	def __str__(self):
		
		return ' '.join([
			self.showName
		])

class Event(Document):
	date = DateTimeField()
	location = GeoPointField()
	slideEvents = ListField(ReferenceField(SlideTest),blank=True)
	name = StringField(max_length=200)
	
	def __str__(self):
	
			return ' '.join([
					self.name,
					self.location
			])

class Director(Document):
	email = EmailField(max_length=100)
	password = StringField(max_length=16)
	username = StringField(max_length=30)
	verified = BooleanField(default=False, editable=False)
	firstName = StringField(max_length=60)
	lastName = StringField(max_length=60)
	companyName = StringField(max_length=60)
	addressLine1 = StringField(max_length=60)
	addressLine2 = StringField(max_length=60, blank=True)
	city = StringField(max_length=60)
	state = StringField(max_length=50)
	zipcode = StringField()
	verifiedName = StringField(max_length=60, blank=True)	
	events = ListField(ReferenceField(Event), blank=True, editable=False)
	deviceID = StringField(max_length=30, blank=True, editable=False)
	slideEvents = ListField(ReferenceField(Event),blank=True, editable=False)
	lastEvent = ReferenceField(Event, null=True, editable=False)
	accountFeatures = DictField(blank=True, editable=False)

	def __str__(self):

        	return ' '.join([
	            self.verifiedName, self.firstName, self.lastName
	        ])



class SubDirector(Document):
	email = EmailField()
	verified = BooleanField()
	verifiedName = StringField(max_length=60)	
	events = ListField(ReferenceField(Event))
	deviceID = StringField(max_length=30)
	slideEvents = ListField(ReferenceField(SlideTest))
	directors = ListField(ReferenceField(Director))
	lastEvent = DateTimeField()
	accountFeatures = DictField(blank=True, editable=False)

	def __str__(self):

        	return ' '.join([
	            self.verifiedName,
		    self.email
	        ])

class PixieIDObject(Document):
	email = EmailField(blank=True)
	verified = BooleanField(default=False)
	events = ListField(ReferenceField(Event))
	deviceIDSequence = StringField(max_length=30)
	deviceSequence = StringField(max_length=18, unique=True)
	directors = ListField(ReferenceField(Director))
	shows = ListField(ReferenceField(SlideTest))
	lastEvent = DateTimeField()
	userData = DictField(blank=True, editable=False)

	class Meta: 
		ordering = ["-lastEvent"]

	def __str__(self):

        	return ' '.join([
	            self.deviceID
	        ])



class User(Document):
	username = StringField(blank=True)
	password = StringField()
	is_staff = BooleanField()
	is_superuser = BooleanField()
	is_active = BooleanField()
	last_login = DateTimeField()
	date_joined = DateTimeField()
	user_permissions = DictField()
	email = EmailField(blank=True)
	verified = BooleanField(default=False)
	events = ListField(ReferenceField(Event))
	deviceId = StringField(max_length=30)
	directors = ListField(ReferenceField(Director))
	shows = ListField(ReferenceField(SlideTest))
	lastEvent = DateTimeField()
	userData = DictField(blank=True, editable=False)

	class Meta: 
		ordering = ["-lastEvent"]

	def event_names(self):
		return ', '.join([event.name for event in self.events.all()])
	event_names.short_description = "Event Names"

	def __str__(self):

        	return ' '.join([
	            self.deviceID
	        ])





	
	
	
	
