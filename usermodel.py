from peewee import *
import datetime

from eventmodel import Event

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
	attending_event=ForeignKeyField(Event, backref='users')
	is_admin=BooleanField(default=False)

	class Meta:
		database = DATABASE