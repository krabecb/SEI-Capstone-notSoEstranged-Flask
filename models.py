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
	emergency_contact=CharField()
	about_me=CharField()

	class Meta:
		database = DATABASE

class Admin(UserMixin, Model):
	email=CharField(unique=True)
	username=CharField(unique=True)
	password=CharField()
	date_of_birth=DateField()
	address=CharField()
	phone_number=CharField()
	emergency_contact=CharField()
	about_me=CharField()

	class Meta:
		database = DATABASE

class Event(Model):
	event_name=CharField()
	event_organizer=CharField()
	event_location=CharField()
	date_of_event=CharField()
	admin = ForeignKeyField(Admin, backref='events')

	class Meta:
		database = DATABASE

class AdminStatus(Model):
	status=CharField()
	date_posted=DateTimeField(default=datetime.datetime.now)
	admin = ForeignKeyField(Admin, backref='adminstatuses')

	class Meta:
		database = DATABASE

class Status(Model):
	status=CharField()
	date_posted=DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(User, backref='statuses')

	class Meta:
		database = DATABASE




def initialize():
	DATABASE.connect()

	DATABASE.create_tables([User, Admin, Event, AdminStatus, Status], safe=True)
	print("Connected to DB and created tables if they didn't already exist.")
	DATABASE.close()