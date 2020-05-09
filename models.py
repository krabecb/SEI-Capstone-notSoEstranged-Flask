from peewee import *
import datetime

from flask_login import UserMixin

from playhouse.db_url import connect




DATABASE = SqliteDatabase('notSoEstranged.sqlite')




class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()
	date_of_birth=DateField()
	emergency_contact=CharField()
	about_me=CharField()

	class Meta:
		database = DATABASE




def initialize():
	DATABASE.connect()

	DATABASE.create_tables([User], safe=True)
	print("Connected to DB and created tables if they didn't already exist.")
	DATABASE.close()