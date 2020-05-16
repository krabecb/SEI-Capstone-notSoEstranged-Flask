from peewee import *
import datetime

from flask_login import UserMixin

from playhouse.db_url import connect




DATABASE = SqliteDatabase('notSoEstranged.sqlite')




class User(UserMixin, Model):
	email=CharField(unique=True)
	username=CharField(unique=True)
	password=CharField()
	date_of_birth=DateField()
	address=CharField()
	phone_number=CharField()
	emergency_contact=CharField()
	about_me=CharField()
	is_admin=BooleanField(default=False)

	class Meta:
		database = DATABASE

class Event(Model):
	event_name=CharField()
	event_organizer=CharField()
	event_location=CharField()
	date_of_event=CharField()
	event_description=CharField()
	longitude=CharField()
	latitude=CharField()
	user = ForeignKeyField(User, backref='events')

	class Meta:
		database = DATABASE

class Status(Model):
	status=CharField()
	date_posted=DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(User, backref='statuses')
	event = ForeignKeyField(Event, backref='statuses')

	class Meta:
		database = DATABASE

class Attendance(Model):
	user = ForeignKeyField(User, backref='attendances')
	event = ForeignKeyField(Event, backref='attendances')

	class Meta:
		database = DATABASE




def initialize():
	DATABASE.connect()

	DATABASE.create_tables([User, Event, Status, Attendance], safe=True)
	print("Connected to DB and created tables if they didn't already exist.")
	DATABASE.close()