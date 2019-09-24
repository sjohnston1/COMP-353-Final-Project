from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
	return Login.query.get(int(user_id))

class Login(db.Model, UserMixin):
	__table__ = db.Model.metadata.tables['login']

	def get_id(self):
		return(self.id)

class Items(db.Model):
	__table__ = db.Model.metadata.tables['items']

class ItemType(db.Model):
	__table__ = db.Model.metadata.tables['itemtype']

class Department(db.Model):
	__table__ = db.Model.metadata.tables['department']

class Employee(db.Model):
	__table__ = db.Model.metadata.tables['employee']

class History(db.Model):
	__table__ = db.Model.metadata.tables['history']

class StatusOf(db.Model):
	__table__ = db.Model.metadata.tables['statusof']

class Requests(db.Model):
	__table__ = db.Model.metadata.tables['requests']
