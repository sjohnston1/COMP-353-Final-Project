import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import LoginForm, RegistrationForm, NewAssetForm, CheckoutForm, OptionForm
from flaskDemo.models import Login, Employee, Department, Items, StatusOf, History, ItemType, Requests
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import mysql.connector
from mysql.connector import Error



@app.route("/")
def home2():
	return render_template('home2.html', title = 'Home')

@app.route("/home")
def home():
	try:
		mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
		if mydb.is_connected():
			mycursor = mydb.cursor()
			num = current_user.Employeenumber
			sql = "SELECT requests.Assetnumber, requests.Checkin, requests.Checkout, requests.Employeenumber FROM requests WHERE Employeenumber = " + num
			mycursor.execute(sql)
			results = mycursor.fetchall()
			print(results)
	finally:
		mydb.close()

	loginid = current_user.Employeenumber
	total = Employee.query.join(History, Employee.Employeenumber == History.Employeenumber) \
			.add_columns(History.Assetnumber, History.Checkin) \
			.filter(Employee.Employeenumber == loginid)

	try:
		mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
		if mydb.is_connected():
			mycursor = mydb.cursor()
			num = current_user.Employeenumber
			sql = "SELECT Employee.DepartmentID FROM Employee WHERE Employeenumber = " + num
			mycursor.execute(sql)
			depID = mycursor.fetchone()
	finally:
		mydb.close()
		
	depID = depID[0]
	info = Employee.query.filter(Employee.DepartmentID == depID).filter(Employee.Employeenumber != loginid) \
			.add_columns(Employee.EmployeeName)
	print('info')
	print(info)
			
	return render_template('home.html', title = 'Home', results = results, total = total, info = info)

@app.route("/instockinventory")
def instockinventory():
	results = Items.query.join(StatusOf, Items.StatusID == StatusOf.StatusID) \
				.add_columns(ItemType.Itemname, Items.Assetnumber, StatusOf.Statusof, Items.StatusID) \
				.join(ItemType, Items.ItemID == ItemType.ItemID)
	return render_template('instockinventory.html', title = 'In Stock Inventory', results=results)

@app.route("/addDevice", methods=['GET','POST'])
def addDevice():
	if current_user.is_authenticated:
		form = NewAssetForm()
		if form.validate_on_submit():
			asset = Items(Serialnumber = form.serialNumber.data,
				Assetnumber = form.assetNumber.data,
				Introductiondate = form.introductionDate.data,
				Orderdate = form.orderDate.data,
				StatusID = form.statusID.data,
				Modelnumber = form.modelNumber.data,
				Cost = form.cost.data,
				ItemID = form.itemID.data)
			db.session.add(asset)
			db.session.commit()
			flash('The item has been created!', 'success')
			return redirect(url_for('home'))
		return render_template('addDevice.html', title='Add Device', form=form)

@app.route("/inventory")
def inventory():
	results = Items.query.join(StatusOf, Items.StatusID == StatusOf.StatusID) \
				.add_columns(ItemType.Itemname, Items.Assetnumber, StatusOf.Statusof, Items.StatusID) \
				.join(ItemType, Items.ItemID == ItemType.ItemID)

	try:
		mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
		if mydb.is_connected():
			mycursor = mydb.cursor()
			sql = "SELECT ItemType.Itemname, COUNT(*) Total FROM ItemType JOIN Items ON ItemType.ItemID = Items.ItemID WHERE ItemType.Itemname = 'Laptop'"
			mycursor.execute(sql)
			results1 = mycursor.fetchall()
			print(results)
	finally:
		mydb.close()
	
	try:
		mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
		if mydb.is_connected():
			mycursor = mydb.cursor()
			sql = "SELECT ItemType.Itemname, COUNT(*) Total FROM ItemType JOIN Items ON ItemType.ItemID = Items.ItemID WHERE ItemType.Itemname = 'Monitor'"
			mycursor.execute(sql)
			results2 = mycursor.fetchall()
			print(results)
	finally:
		mydb.close()
	
	try:
		mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
		if mydb.is_connected():
			mycursor = mydb.cursor()
			sql = "SELECT ItemType.Itemname, COUNT(*) Total FROM ItemType JOIN Items ON ItemType.ItemID = Items.ItemID WHERE ItemType.Itemname = 'Cell Phone'"
			mycursor.execute(sql)
			results3 = mycursor.fetchall()
			print(results)
	finally:
		mydb.close()
	return render_template('inventory.html', title='Inventory', results=results, results1 = results1, results2 = results2, results3 = results3)

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Login.query.filter_by(LoginID = form.loginid.data).first()
		if user and bcrypt.check_password_hash(user.Password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check LoginID and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home2'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
    	employee = Employee(Employeenumber = form.employeeNumber.data,
    		EmployeeName = form.employeeName.data,
    		EmployeeAddress = form.employeeAddress.data,
    		EmployeeCity = form.employeeCity.data,
    		EmployeeState = form.employeeState.data,
    		EmployeeZip = form.employeeZip.data,
    		EmployeeBirthDate = form.employeeBirthDate.data,
    		DepartmentID = form.employeeDepartmentID.data)
    	db.session.add(employee)
    	db.session.commit()
    	hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    	print(hashed_password)
    	loginid = Login(LoginID=form.loginid.data, Employeenumber = form.employeeNumber.data, Password=hashed_password)
    	db.session.add(loginid)
    	db.session.commit()
    	flash('Your account has been created! You are now able to log in', 'success')
    	return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/view/<assetnumber>", methods=['GET', 'POST'])
@login_required
def view(assetnumber):
	form = CheckoutForm()
	requests = Requests(Checkin = form.checkinDate.data, Checkout = form.checkoutDate.data, Assetnumber = assetnumber, Employeenumber = form.employeeNumber.data)
	print("debug 1")
	if form.validate_on_submit():
		print("debug 2")
		db.session.add(requests)
		db.session.commit()
		flash('The request has been put in', 'success')
		return redirect(url_for('home'))
	return render_template('view.html', title = 'Request an Item', form = form, Legend = 'Request an Item')

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
	if current_user.Admin == 1:
		try:
			mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
			if mydb.is_connected():
				mycursor = mydb.cursor()
				sql = "SELECT requests.Checkin, requests.Checkout, requests.Assetnumber, Employee.employeeName, requests.employeeNumber, requests.Log FROM requests JOIN Employee ON requests.Employeenumber=Employee.Employeenumber"
				mycursor.execute(sql)
				results = mycursor.fetchall()
				print(results)
		finally:
			mydb.close()

		try:
			mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
			if mydb.is_connected():
				mycursor = mydb.cursor()
				sql = "SELECT ROUND(AVG(Cost),2) FROM Items"
				mycursor.execute(sql)
				results2 = mycursor.fetchall()
				print(results2)
		finally:
			mydb.close()

		try:
			mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
			if mydb.is_connected():
				mycursor = mydb.cursor()
				sql = "SELECT Cost, Assetnumber FROM Items WHERE Cost > (SELECT AVG(Cost) FROM Items)"
				mycursor.execute(sql)
				results1 = mycursor.fetchall()
				print(results1)
		finally:
			mydb.close()

		try:
			mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
			if mydb.is_connected():
				mycursor = mydb.cursor()
				sql = "SELECT Assetnumber FROM Items WHERE ItemID = 1 or ItemID = 2"
				mycursor.execute(sql)
				results3 = mycursor.fetchall()
				print(results1)
		finally:
			mydb.close()

	else:
		flash('You do not have Administration Rights.')

		return redirect(url_for('home'))
	return render_template('admin.html', results=results, results1 = results1, results2 = results2, results3 = results3)

@app.route("/admin/<Assetnumber>/<Checkin>/<Checkout>/<Employeenumber>/<Log>", methods=['GET', 'POST'])
@login_required
def admin_choice(Assetnumber, Checkin, Checkout, Employeenumber, Log):
	total = Requests.query.filter_by(Log = Log).first()
	print(total)
	form = OptionForm()
	accept = History(Checkout = Checkout, 
				Checkin = Checkin, 
				Assetnumber = Assetnumber, 
				Employeenumber = Employeenumber)
	itemValue = Assetnumber
	
	'''
	try:
		mydb = mysql.connector.connect(host = "localhost", user = "sjohnston1", password = "Alpha168123", database = "inventory")
		if mydb.is_connected():
			mycursor = mydb.cursor()
			sql = "UPDATE items SET StatusID = 3 WHERE Assetnumber = " + itemValue
			mycursor.execute(sql)
			mydb.commit()
	finally:
		mydb.close()
	'''

	update = Items.query.filter_by(Assetnumber = itemValue).first()
	update.StatusID = 3
	db.session.commit()
	
	if form.validate_on_submit():
		db.session.delete(total)
		db.session.add(accept)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('options.html', title = 'Options', form = form, Legend = 'Options')