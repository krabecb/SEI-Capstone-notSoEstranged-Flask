from peewee import *
import datetime

from usermodel import User

from flask_login import UserMixin

from playhouse.db_url import connect




DATABASE = SqliteDatabase('notSoEstranged.sqlite')


class Event(Model):
	event_name=CharField()
	event_organizer=CharField()
	event_location=CharField()
	date_of_event=CharField()
	user = ForeignKeyField(User, backref='events')

	class Meta:
		database = DATABASE