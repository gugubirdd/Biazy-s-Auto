import os
import datetime
import os.path
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from Forms import Register, CarRegister, Login, Update, CarUpdate, ChangePassword, ProfilePic, ForgetPassword, CreateAdmin, CreateCarForm, CreateElectricCarForm, CreateServiceForm, CreateCarserviceForm, createPublicEventForm, createInternalEventForm, CreateAccessoryForm, CreateElectronicAccessoryForm
import shelve
import Account
import CarAccount
import Admin
import Car
import ElectricCar
import Service
import Carservice
import InternalEvent
import PublicEvent
import Accessory
import ElectronicAccessory

app = Flask(__name__)
app.secret_key = 'any_random_string'

path = 'static/assets/profiles/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = path
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'appdevresetpw@gmail.com'
app.config['MAIL_PASSWORD'] = 'iamgay1122@@'
mail = Mail(app)


@app.before_request
def get_current_user():
    accounts_dict = {}
    db = shelve.open('account.db', 'r')
    try:
        accounts_dict = db['Accounts']
    except:
        print("Error in retrieving accounts from account.db.")
    try:
        g.current_user = accounts_dict[session['current_user']]
    except KeyError:
        g.current_user = None


@app.route('/')
def home():
    date = datetime.date.today()
    current_date = datetime.date.today()
    cars_dict = {}
    dbfeatured = shelve.open('featured.db', 'r')
    featureditem = dbfeatured['Featured']
    print(featureditem)
    dbfeatured.close()
    db = shelve.open('car.db', 'r')
    cars_dict = db['cars']
    db.close()

    cars_list = []
    print(cars_list)
    for key in cars_dict:
        car = cars_dict.get(key)
        if car.get_car_availstartdate() <= date:
            if car.get_car_quantity() == 0:
                car.set_car_availability("Out-of-Stock")
            elif car.get_car_quantity() > 0:
                car.set_car_availability("In Stock")
        elif car.get_car_availstartdate() > date:
            car.set_car_availability("Unavailable")
        if car.get_car_availability() != 'Unavailable':
            cars_list.append(car)

    electric_cars_dict = {}
    db = shelve.open('electric_car.db', 'r')
    electric_cars_dict = db['electric_cars']
    db.close()

    electric_cars_list = []
    for key in electric_cars_dict:
        electric_car = electric_cars_dict.get(key)
        if electric_car.get_car_availstartdate() <= date:
            if electric_car.get_car_quantity() == 0:
                electric_car.set_car_availability("Out-of-Stock")
            elif electric_car.get_car_quantity() > 0:
                electric_car.set_car_availability("In Stock")
        elif electric_car.get_car_availstartdate() > date:
            electric_car.set_car_availability("Unavailable")
        if electric_car.get_car_availability() != 'Unavailable':
            electric_cars_list.append(electric_car)

    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    publicevent_dict = {}
    db = shelve.open('publicevent.db', 'r')
    publicevent_dict = db['publicevent']
    db.close()

    publicevent_list = []
    for key in publicevent_dict:
        publicevent = publicevent_dict.get(key)
        publicevent_list.append(publicevent)

    internalevent_dict = {}
    db = shelve.open('internalevent.db', 'r')
    internalevent_dict = db['internalevent']
    db.close()

    internalevent_list = []
    for key in internalevent_dict:
        internalevent = internalevent_dict.get(key)
        internalevent_list.append(internalevent)

    Apublicevent_list = []
    for key in publicevent_dict:
        publicevent = publicevent_dict.get(key)
        if publicevent.get_startDate() >= current_date:
            Apublicevent_list.append(publicevent)

    db = shelve.open('accessory.db', 'r')
    accessories_dict = db['Accessories']
    db.close()

    accessories_list = []
    for key in accessories_dict:
        accessory = accessories_dict.get(key)
        if not accessory.get_end() is None:
            if accessory.get_start() <= date < accessory.get_end():
                if accessory.get_quantity() == 0:
                    accessory.set_status("Out of Stock")
                elif accessory.get_quantity() > 0:
                    accessory.set_status("In Stock")
            elif accessory.get_start() > date:
                accessory.set_status("Unavailable")
            elif accessory.get_end() <= date:
                accessory.set_status("Unavailable")
            if not accessory.get_status() == "Unavailable" and accessory.get_start() <= date < accessory.get_end():
                accessories_list.append(accessory)
        else:
            if accessory.get_start() <= date:
                if accessory.get_quantity() == 0:
                    accessory.set_status("Out of Stock")
                elif accessory.get_quantity() > 0:
                    accessory.set_status("In Stock")
            else:
                accessory.set_status("Unavailable")
            if not accessory.get_status() == "Unavailable" and accessory.get_start() <= date:
                accessories_list.append(accessory)

    db = shelve.open('electronicaccessory.db', 'r')
    electronicaccessory_dict = db['ElectronicAccessories']
    db.close()

    electronicaccessory_list = []
    for key in electronicaccessory_dict:
        electronicaccessory = electronicaccessory_dict.get(key)
        if not electronicaccessory.get_end() is None:
            if electronicaccessory.get_start() <= date < electronicaccessory.get_end():
                if electronicaccessory.get_quantity() == 0:
                    electronicaccessory.set_status("Out of Stock")
                elif electronicaccessory.get_quantity() > 0:
                    electronicaccessory.set_status("In Stock")
            elif electronicaccessory.get_start() > date:
                electronicaccessory.set_status("Unavailable")
            elif electronicaccessory.get_end() <= date:
                electronicaccessory.set_status("Unavailable")
            if not electronicaccessory.get_status() == "Unavailable" and electronicaccessory.get_start() <= date < electronicaccessory.get_end():
                electronicaccessory_list.append(electronicaccessory)
        else:
            if electronicaccessory.get_start() <= date:
                if electronicaccessory.get_quantity() == 0:
                    electronicaccessory.set_status("Out of Stock")
                elif electronicaccessory.get_quantity() > 0:
                    electronicaccessory.set_status("In Stock")
            else:
                electronicaccessory.set_status("Unavailable")
            if not electronicaccessory.get_status() == "Unavailable" and electronicaccessory.get_start() <= date:
                electronicaccessory_list.append(electronicaccessory)

    return render_template('index.html', count=len(cars_list), cars_list=cars_list, electric_cars_list=electric_cars_list, services_list=services_list, carservices_list=carservices_list,  publicevent_list=publicevent_list, internalevent_list=internalevent_list, accessories_list=accessories_list, electronicaccessory_list=electronicaccessory_list, current_date=current_date, featureditem=featureditem)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login(request.form)
    if request.method == 'POST' and login_form.validate():
        accounts_dict = {}
        attempts_dict = {}
        db = shelve.open('account.db', 'c')
        session_dict = shelve.open('session.db', 'c')
        user_id_dict = {}
        try:
            if 'current_session' in session_dict:
                user_id_dict = session_dict['current_session']

            else:
                session_dict['current_session'] = user_id_dict

        except:
            print("Error in opening session")

        try:
            accounts_dict = db['Accounts']
        except:
            print("Error in retrieving accounts from account.db.")

        try:
            attempts_dict = db['Attempts']
        except:
            print("Error in retrieving accounts from account.db.")

        for key in accounts_dict:

            account = accounts_dict.get(key)
            email = account.get_email()
            password = account.get_password()
            userid = account.get_account_id()

            if login_form.email.data == email:
                if account.get_status() == "Locked":
                    session['password_wrong'] = "Your account is locked, please contact us for assistance."
                    return redirect(url_for('login'))
                elif login_form.password.data == password:
                    user_id_dict['user_id'] = userid
                    session_dict['current_session'] = user_id_dict

                    if email.split('@')[1] == 'admin.com':
                        session['current_user'] = account.get_account_id()
                        return redirect(url_for('accounts'))

                    else:
                        account.set_status(True)
                        attempts_dict[account.get_account_id()] = 0
                        accounts_dict[account.get_account_id()] = account
                        db['Attempts'] = attempts_dict
                        db['Accounts'] = accounts_dict
                        session['login_success'] = account.get_title() + ". " + account.get_first_name()
                        session['email'] = account.get_email()
                        db.close()
                        return redirect(url_for('home'))
                else:
                    if email.split('@')[1] == 'admin.com':
                        session['admin_password_wrong'] = "Invalid Password"
                    else:
                        attempts_dict = {}
                        try:
                            attempts_dict = db['Attempts']
                        except:
                            print("Error in retrieving accounts from account.db.")

                        wrong = attempts_dict.get(account.get_account_id())
                        if wrong is None:
                            wrong = 0
                        wrong += 1
                        attempts_dict[account.get_account_id()] = wrong

                        if wrong >= 5:
                            account.set_status("Locked")
                            accounts_dict[account.get_account_id()] = account
                            db['Accounts'] = accounts_dict
                            print(account.get_status())
                            print(wrong)
                            session['password_wrong'] = "Your account is locked, please contact us for assistance."
                            return redirect(url_for('login'))
                        session['password_wrong'] = f"Invalid Password, you have {5-wrong} attempts left."
                        db['Attempts'] = attempts_dict
                        db.close()
                    return redirect(url_for('login'))
        db.close()
        caraccounts_dict = {}
        db = shelve.open('caraccount.db', 'c')
        caraccounts_dict = db['carAccounts']
        for key in caraccounts_dict:

            account = caraccounts_dict.get(key)
            email = account.get_email()
            password = account.get_password()
            userid = account.get_account_id()

            if login_form.email.data == email:
                if login_form.password.data == password:
                    user_id_dict['user_id'] = userid
                    session_dict['current_session'] = user_id_dict

                    if email.split('@')[1] == 'admin.com':
                        return redirect(url_for('accounts'))
                    else:
                        account.set_status(True)
                        caraccounts_dict[account.get_account_id()] = account
                        db['carAccounts'] = caraccounts_dict
                        session['login_success'] = account.get_title() + ". " + account.get_first_name()
                        session['email'] = account.get_email()
                        db.close()
                        return redirect(url_for('home'))
                else:
                    session['password_wrong'] = "Invalid Password"
                    return redirect(url_for('login'))
        session['email_notfound'] = login_form.email.data

    return render_template('/login.html', form=login_form)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    update_account_form = Update(request.form)
    carupdate_account_form = CarUpdate(request.form)
    change_password_form = ChangePassword(request.form)
    add_profilepic = ProfilePic(request.files)
    accounts_dict = {}
    db = shelve.open('account.db', 'r')
    accounts_dict = db['Accounts']
    caraccounts_dict = {}
    db2 = shelve.open('caraccount.db', 'r')
    caraccounts_dict = db2['carAccounts']
    for key in accounts_dict:
        if session['email'] == accounts_dict.get(key).get_email():
            account = accounts_dict.get(key)
    else:
        for key in caraccounts_dict:
            if session['email'] == caraccounts_dict.get(key).get_email():
                account = caraccounts_dict.get(key)
    if request.method == "POST" and add_profilepic.validate():
        db = shelve.open('account.db', 'w')
        accounts_dict = db['Accounts']
        db2 = shelve.open('caraccount.db', 'w')
        caraccounts_dict = db2['carAccounts']
        for key in accounts_dict:
            if session['email'] == accounts_dict.get(key).get_email():
                account = accounts_dict.get(key)
                if add_profilepic.profilepic.data is not None:
                    filename = secure_filename(add_profilepic.profilepic.data.filename)
                    add_profilepic.profilepic.data.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                    account.set_image(filename)
                    db['Accounts'] = accounts_dict
                    db.close()
        else:
            for key in caraccounts_dict:
                if session['email'] == caraccounts_dict.get(key).get_email():
                    account = caraccounts_dict.get(key)
                    if add_profilepic.profilepic.data is not None:
                        filename = secure_filename(add_profilepic.profilepic.data.filename)
                        add_profilepic.profilepic.data.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                        account.set_image(filename)
                        db2['carAccounts'] = caraccounts_dict
                        db2.close()

    elif request.method == "POST":
        session['invalid_file_type'] = "png, jpg, and gif"

    update_account_form.title.data = account.get_title()
    carupdate_account_form.title.data = account.get_title()
    return render_template('/profile.html', account=account, accounts_dict=accounts_dict, caraccounts_dict=caraccounts_dict, form=change_password_form, form2=update_account_form, form3=add_profilepic, form4=carupdate_account_form)


@app.route('/logout')
def logout():
    session.pop('login_success', None)
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/admintables')
def admintables():
    accounts_dict = {}
    db = shelve.open('account.db', 'r')
    accounts_dict = db['Accounts']
    db.close()

    accounts_list = []
    for key in accounts_dict:
        account = accounts_dict.get(key)
        if account.get_email().split('@')[1] == 'admin.com':
            accounts_list.append(account)
    return render_template('/admintables.html', count=len(accounts_list), accounts_list=accounts_list, form=CreateAdmin())


@app.route('/newAdmin', methods=['GET', 'POST'])
def newAdmin():
    admin_form = CreateAdmin(request.form)
    if request.method == 'POST' and admin_form.validate():
        accounts_dict = {}
        db = shelve.open('account.db', 'c')
        try:
            accounts_dict = db['Accounts']
        except:
            print("Error in retrieving accounts from account.db.")
        account = Admin.Admin(admin_form.first_name.data,
                              admin_form.last_name.data,
                              admin_form.email.data + '@admin.com',
                              admin_form.password.data,
                              admin_form.position.data)
        print(account.get_email())
        if len(accounts_dict) > 0:
            account.set_account_id(list(accounts_dict)[-1]+1)
        accounts_dict[account.get_account_id()] = account
        db['Accounts'] = accounts_dict
    else:
        session['password_weak'] = "Password is too weak or does not match, failed to create new admin."
        return redirect(url_for('admintables'))

    db.close()
    session['account_created'] = account.get_first_name() + ' ' + account.get_last_name()

    return redirect(url_for('admintables'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = Register(request.form)
    if request.method == 'POST' and register_form.validate():
        emails = []
        accounts_dict = {}
        caraccounts_dict = {}
        db = shelve.open('account.db', 'c')
        dbcar = shelve.open('caraccount.db', 'c')

        try:
            accounts_dict = db['Accounts']
        except:
            print("Error in retrieving accounts from account.db.")

        try:
            caraccounts_dict = dbcar['carAccounts']
        except:
            print("Error in retrieving accounts from account.db.")

        for key in accounts_dict:
            account = accounts_dict.get(key)
            emails.append(account.get_email())

        for key in caraccounts_dict:
            caraccount = caraccounts_dict.get(key)
            emails.append(caraccount.get_email())

        if register_form.email.data.split('@')[1] == 'admin.com':
            session['invalid_email'] = "Emails cannot end with '@admin.com'."
            return redirect(url_for('register'))
        elif register_form.email.data in emails:
            session['email_exists'] = register_form.email.data
            return redirect(url_for('register'))
        else:
            account = Account.Account(register_form.first_name.data,
                                      register_form.last_name.data,
                                      register_form.title.data,
                                      register_form.phone.data,
                                      register_form.email.data,
                                      register_form.password.data)

        if len(accounts_dict) > 0:
            account.set_account_id(list(accounts_dict)[-1]+1)
        accounts_dict[account.get_account_id()] = account
        db['Accounts'] = accounts_dict

        db.close()
        dbcar.close()
        session['account_created'] = account.get_first_name() + ' ' + account.get_last_name()

    return render_template('/register.html', form=register_form)


@app.route('/carregister', methods=['GET', 'POST'])
def carregister():
    carregister_form = CarRegister(request.form)
    if request.method == 'POST' and carregister_form.validate():
        emails = []
        accounts_dict = {}
        caraccounts_dict = {}
        db = shelve.open('caraccount.db', 'c')
        db2 = shelve.open('account.db', 'c')

        try:
            caraccounts_dict = db['carAccounts']
        except:
            print("Error in retrieving accounts from account.db.")

        try:
            accounts_dict = db2['Accounts']
        except:
            print("Error in retrieving accounts from account.db.")

        for key in accounts_dict:
            account = accounts_dict.get(key)
            emails.append(account.get_email())

        for key in caraccounts_dict:
            caraccount = caraccounts_dict.get(key)
            emails.append(caraccount.get_email())

        if carregister_form.email.data in emails:
            session['caremail_exists'] = carregister_form.email.data
            return redirect(url_for('carregister'))
        else:
            caraccount = CarAccount.CarAccount(carregister_form.first_name.data,
                                               carregister_form.last_name.data,
                                               carregister_form.title.data,
                                               carregister_form.phone.data,
                                               carregister_form.email.data,
                                               carregister_form.password.data,
                                               carregister_form.make.data,
                                               carregister_form.model.data)
        if len(caraccounts_dict) > 0:
            caraccount.set_account_id(list(caraccounts_dict)[-1]+1)
        caraccounts_dict[caraccount.get_account_id()] = caraccount
        db['carAccounts'] = caraccounts_dict

        db.close()
        db2.close()
        session['caraccount_created'] = caraccount.get_first_name() + ' ' + caraccount.get_last_name()

    return render_template('/carregister.html', form=carregister_form)


@app.route('/accounts')
def accounts():
    return render_template('/accounts.html')

@app.route('/wishlist')
def wishlist():
    db = shelve.open('car.db', 'r')
    cars_dict = db['cars']
    db.close()
    db = shelve.open('electric_car.db', 'r')
    electric_cars_dict = db['electric_cars']
    db.close()
    db = shelve.open('accessory.db', 'r')
    accessories_dict = db['Accessories']
    db.close()
    db = shelve.open('electronicaccessory.db', 'r')
    electronicaccessory_dict = db['ElectronicAccessories']
    db.close()
    accounts_dict = {}
    db = shelve.open('account.db', 'r')
    accounts_dict = db['Accounts']
    caraccounts_dict = {}
    db2 = shelve.open('caraccount.db', 'r')
    caraccounts_dict = db2['carAccounts']
    for key in accounts_dict:
        if session['email'] == accounts_dict.get(key).get_email():
            account = accounts_dict.get(key)
    else:
        for key in caraccounts_dict:
            if session['email'] == caraccounts_dict.get(key).get_email():
                account = caraccounts_dict.get(key)
    db3 = shelve.open('wishlist.db', 'r')
    wishlist = db3['Wishlist']
    wishes = []
    for item in wishlist.get(session['email']):
        wish = []
        if isinstance(item, Car.Car):
            wish.append(item.get_car_model() + " " + item.get_car_name())
            wish.append(item.get_car_model())
            wish.append(item.get_car_availability())
            wish.append(item.get_car_price())
            wish.append(item.get_car_description())
            wish.append(item.get_car_image())
            wish.append(None)
            wish.append(None)
            wish.append(item.get_car_id())
        elif isinstance(item, ElectricCar.ElectricCar):
            wish.append(item.get_car_model() + " " + item.get_car_name())
            wish.append(item.get_car_model())
            wish.append(item.get_car_availability())
            wish.append(item.get_car_price())
            wish.append(item.get_car_description())
            wish.append(item.get_car_image())
            wish.append(item.get_car_battery_capacity())
            wish.append(item.get_car_charging_duration())
            wish.append(item.get_electric_car_id())
        elif isinstance(item, Accessory.Accessory):
            wish.append(item.get_name())
            wish.append(None)
            wish.append(item.get_quantity())
            wish.append(item.get_price())
            wish.append(item.get_description())
            wish.append(item.get_image())
            wish.append(None)
            wish.append(None)
            wish.append(item.get_accessory_id())
        elif isinstance(item, ElectronicAccessory.ElectronicAccessory):
            wish.append(item.get_name())
            wish.append(None)
            wish.append(item.get_quantity())
            wish.append(item.get_price())
            wish.append(item.get_description())
            wish.append(item.get_image())
            wish.append(item.get_battery_type())
            wish.append(item.get_batteries_required())
            wish.append(wishes.index)
        wishes.append(wish)
    print(wishes)



    return render_template('/wishlist.html', account=account, wishes=wishes, cars_dict=cars_dict, electric_cars_dict=electric_cars_dict, accessories_dict=accessories_dict, electronicaccessory_dict=electronicaccessory_dict)


@app.route('/tables')
def tables():
    update_account_form = Update(request.form)
    update_caraccount_form = CarUpdate(request.form)
    accounts_dict = {}
    db = shelve.open('account.db', 'r')
    accounts_dict = db['Accounts']
    db.close()

    accounts_list = []
    for key in accounts_dict:
        account = accounts_dict.get(key)
        if account.get_email().split('@')[1] != 'admin.com':
            accounts_list.append(account)

    caraccounts_dict = {}
    db = shelve.open('caraccount.db', 'r')

    try:
        caraccounts_dict = db['carAccounts']
    except:
        print("Error in retrieving accounts from account.db.")
    db.close()

    caraccounts_list = []
    for key in caraccounts_dict:
        caraccount = caraccounts_dict.get(key)
        caraccounts_list.append(caraccount)

    return render_template('/tables.html', count=len(accounts_list), accounts_list=accounts_list, caraccounts_list=caraccounts_list, form=update_account_form, form2=update_caraccount_form)


@app.route('/update/<int:id>/', methods=['POST'])
def update_account(id):
    update_account_form = Update(request.form)
    if request.method == 'POST' and update_account_form.validate():
        accounts_dict = {}
        db = shelve.open('account.db', 'w')
        accounts_dict = db['Accounts']

        account = accounts_dict.get(id)
        account.set_first_name(update_account_form.first_name.data)
        account.set_last_name(update_account_form.last_name.data)
        account.set_title(update_account_form.title.data)
        account.set_phone(update_account_form.phone.data)
        account.set_email(update_account_form.email.data)

        db['Accounts'] = accounts_dict
        db.close()
        session['account_updated'] = account.get_first_name() + ' ' + account.get_last_name()

        return redirect(url_for('tables'))


@app.route('/selfupdate/<int:id>/', methods=['POST'])
def selfupdate_account(id):
    update_account_form = Update(request.form)
    if request.method == 'POST' and update_account_form.validate():
        accounts_dict = {}
        db = shelve.open('account.db', 'w')
        accounts_dict = db['Accounts']

        account = accounts_dict.get(id)
        account.set_first_name(update_account_form.first_name.data)
        account.set_last_name(update_account_form.last_name.data)
        account.set_title(update_account_form.title.data)
        account.set_phone(update_account_form.phone.data)
        account.set_email(update_account_form.email.data)
        session['email'] = update_account_form.email.data

        session['login_success'] = account.get_title() + ". " + account.get_first_name()
        db['Accounts'] = accounts_dict
        db.close()
        session['selfaccount_updated'] = "Your account has been updated successfully!"

        return redirect(url_for('profile'))


@app.route('/carselfupdate/<int:id>/', methods=['POST'])
def carselfupdate_account(id):
    carupdate_account_form = CarUpdate(request.form)
    if request.method == 'POST' and carupdate_account_form.validate():
        caraccounts_dict = {}
        db = shelve.open('caraccount.db', 'w')
        caraccounts_dict = db['carAccounts']

        caraccount = caraccounts_dict.get(id)
        caraccount.set_first_name(carupdate_account_form.first_name.data)
        caraccount.set_last_name(carupdate_account_form.last_name.data)
        caraccount.set_title(carupdate_account_form.title.data)
        caraccount.set_phone(carupdate_account_form.phone.data)
        caraccount.set_email(carupdate_account_form.email.data)
        caraccount.set_make(carupdate_account_form.make.data)
        caraccount.set_model(carupdate_account_form.model.data)
        session['email'] = carupdate_account_form.email.data

        session['login_success'] = caraccount.get_title() + ". " + caraccount.get_first_name()
        db['carAccounts'] = caraccounts_dict
        db.close()
        session['selfaccount_updated'] = "Your account has been updated successfully!"

        return redirect(url_for('profile'))


@app.route('/carupdate/<int:id>/', methods=['POST'])
def update_caraccount(id):
    update_caraccount_form = CarUpdate(request.form)
    if request.method == 'POST' and update_caraccount_form.validate():
        caraccounts_dict = {}
        db = shelve.open('caraccount.db', 'w')
        caraccounts_dict = db['carAccounts']

        caraccount = caraccounts_dict.get(id)
        caraccount.set_first_name(update_caraccount_form.first_name.data)
        caraccount.set_last_name(update_caraccount_form.last_name.data)
        caraccount.set_title(update_caraccount_form.title.data)
        caraccount.set_phone(update_caraccount_form.phone.data)
        caraccount.set_email(update_caraccount_form.email.data)
        caraccount.set_make(update_caraccount_form.make.data)
        caraccount.set_model(update_caraccount_form.model.data)

        db['carAccounts'] = caraccounts_dict
        db.close()
        session['caraccount_updated'] = caraccount.get_first_name() + ' ' + caraccount.get_last_name()

        return redirect(url_for('tables'))


@app.route('/deleteAccount/<int:id>', methods=['POST'])
def delete_account(id):
    accounts_dict = {}
    db = shelve.open('account.db', 'w')
    accounts_dict = db['Accounts']

    account = accounts_dict.pop(id)

    db['Accounts'] = accounts_dict
    db.close()
    session['account_deleted'] = account.get_first_name() + ' ' + account.get_last_name()

    return redirect(url_for('tables'))

@app.route('/deleteAccountAdmin/<int:id>', methods=['POST'])
def delete_accountAdmin(id):
    accounts_dict = {}
    db = shelve.open('account.db', 'w')
    accounts_dict = db['Accounts']

    account = accounts_dict.pop(id)

    db['Accounts'] = accounts_dict
    db.close()
    session['adminaccount_deleted'] = account.get_first_name() + ' ' + account.get_last_name()

    return redirect(url_for('admintables'))


@app.route('/selfdeleteAccount/<int:id>', methods=['POST'])
def selfdelete_account(id):
    accounts_dict = {}
    db = shelve.open('account.db', 'w')
    accounts_dict = db['Accounts']

    account = accounts_dict.pop(id)

    db['Accounts'] = accounts_dict
    db.close()

    return redirect(url_for('logout'))

@app.route('/selfdeletecarAccount/<int:id>', methods=['POST'])
def selfdelete_caraccount(id):
    caraccounts_dict = {}
    db = shelve.open('caraccount.db', 'w')
    caraccounts_dict = db['carAccounts']

    caraccount = caraccounts_dict.pop(id)

    db['carAccounts'] = caraccounts_dict
    db.close()

    return redirect(url_for('logout'))


@app.route('/deletecarAccount/<int:id>', methods=['POST'])
def delete_caraccount(id):
    caraccounts_dict = {}
    db = shelve.open('caraccount.db', 'w')
    caraccounts_dict = db['carAccounts']

    caraccount = caraccounts_dict.pop(id)

    db['carAccounts'] = caraccounts_dict
    db.close()
    session['caraccount_deleted'] = caraccount.get_first_name() + ' ' + caraccount.get_last_name()

    return redirect(url_for('tables'))


@app.route('/password', methods=['GET', 'POST'])
def password():
    forget_password_form = ForgetPassword(request.form)
    if request.method == 'POST' and forget_password_form.validate():
        accounts = []
        accounts_dict = {}
        caraccounts_dict = {}
        db = shelve.open('account.db', 'c')
        dbcar = shelve.open('caraccount.db', 'c')

        try:
            accounts_dict = db['Accounts']
        except:
            print("Error in retrieving accounts from account.db.")

        try:
            caraccounts_dict = dbcar['carAccounts']
        except:
            print("Error in retrieving accounts from account.db.")

        for key in accounts_dict:
            account = accounts_dict.get(key)
            accounts.append(account)

        for key in caraccounts_dict:
            caraccount = caraccounts_dict.get(key)
            accounts.append(caraccount)

        for account in accounts:
            if forget_password_form.email.data == account.get_email():
                temporary_password = str(uuid4())[:8]
                account.set_password(temporary_password)
                if account.get_account_id() in accounts_dict:
                    accounts_dict[account.get_account_id()] = account
                    db["Accounts"] = accounts_dict
                    db.close()
                elif account.get_account_id() in caraccounts_dict:
                    caraccounts_dict[account.get_account_id()] = account
                    dbcar["carAccounts"] = caraccounts_dict
                    dbcar.close()
                msg = Message('Your New Password ', sender='appdevprojectsss@gmail.com', recipients=[forget_password_form.email.data])
                msg.html = render_template('email.html', temporary_password=temporary_password)
                mail.send(msg)
                session['email_sent'] = forget_password_form.email.data
                return redirect(url_for('login'))
        session['email_not_found'] = forget_password_form.email.data
        return redirect(url_for('password'))

    else:
        print('error')
    return render_template('/password.html', form=forget_password_form)


@app.route('/deactivate/<id>')
def deactivate(id):
    accounts_dict = {}
    db = shelve.open('account.db', 'c')
    accounts_dict = db['Accounts']

    account = accounts_dict[int(id)]
    account.set_status(False)
    accounts_dict[account.get_account_id()] = account
    db['Accounts'] = accounts_dict
    db.close()
    return redirect(url_for('logout'))

@app.route('/deactivatecar/<id>')
def deactivatecar(id):
    caraccounts_dict = {}
    db = shelve.open('caraccount.db', 'c')
    caraccounts_dict = db['carAccounts']

    caraccount = caraccounts_dict[int(id)]
    caraccount.set_status(False)
    caraccounts_dict[caraccount.get_account_id()] = caraccount
    db['carAccounts'] = caraccounts_dict
    db.close()
    return redirect(url_for('logout'))


@app.route('/unlock/<id>')
def unlock(id):
    accounts_dict = {}
    attempts_dict = {}
    db = shelve.open('account.db', 'c')
    accounts_dict = db['Accounts']
    attempts_dict = db['Attempts']

    account = accounts_dict[int(id)]
    account.set_status(True)
    temporary_password = str(uuid4())[:8]
    account.set_password(temporary_password)
    msg = Message('Account Unlocked', sender='appdevprojectsss@gmail.com', recipients=[account.get_email()])
    msg.html = render_template('unlockemail.html', temporary_password=temporary_password)
    mail.send(msg)
    session['unlock_success'] = account.get_first_name() + ' ' + account.get_last_name()
    attempts_dict[account.get_account_id()] = 0
    accounts_dict[account.get_account_id()] = account
    db['Accounts'] = accounts_dict
    db['Attempts'] = attempts_dict
    db.close()
    return redirect(url_for('tables'))


@app.route('/resetpassword/<id>', methods=['GET', 'POST'])
def resetpassword(id):
    change_password_form = ChangePassword(request.form)
    if request.method == 'POST' and change_password_form.validate():
        db = shelve.open('account.db', 'c')
        accounts_dict = db['Accounts']
        account = accounts_dict[int(id)]
        password = account.get_password()

        if change_password_form.old_password.data == password:
            if change_password_form.confirm_new_password.data == change_password_form.new_password.data:
                account.set_password(change_password_form.new_password.data)
                session['password_changed'] = "Your password has successfully been changed!"
                db['Accounts'] = accounts_dict
                db.close()
                return redirect(url_for('profile'))
            else:
                session['new_password_diff'] = "New passwords do not match, password change failed."
                return redirect(url_for('profile'))
        else:
            session['old_password_wrong'] = "Old password does not match, password change failed."
            return redirect(url_for('profile'))
    else:
        session['password_invalid'] = "New password is too weak, password change failed."
        return redirect(url_for('profile'))


@app.route('/resetpasswordcar/<id>', methods=['GET', 'POST'])
def resetpasswordcar(id):
    change_password_form = ChangePassword(request.form)
    if request.method == 'POST' and change_password_form.validate():
        db = shelve.open('caraccount.db', 'c')
        caraccounts_dict = db['carAccounts']
        caraccount = caraccounts_dict[int(id)]
        password = caraccount.get_password()

        if change_password_form.old_password.data == password:
            if change_password_form.confirm_new_password.data == change_password_form.new_password.data:
                caraccount.set_password(change_password_form.new_password.data)
                session['password_changed'] = "Your password has successfully been changed!"
                db['carAccounts'] = caraccounts_dict
                db.close()
                return redirect(url_for('profile'))
            else:
                session['new_password_diff'] = "New passwords do not match, password change failed."
                return redirect(url_for('profile'))
        else:
            session['old_password_wrong'] = "Old password does not match, password change failed."
            return redirect(url_for('profile'))
    else:
        session['password_invalid'] = "New password is too weak, password change failed."
        return redirect(url_for('profile'))


# YANWEN


@app.route('/createCar', methods=['GET', 'POST'])
def create_car():
    create_car_form = CreateCarForm(request.form)
    if request.method == 'POST' and create_car_form.validate():

        target = os.path.join(APP_ROOT, 'static/assets/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            filename = file.filename
            print(filename)
            if filename == "=":
                flash("No image selected!")
                return redirect(request.url)
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

            cars_dict = {}
            db = shelve.open('car.db', 'c')

            try:
                cars_dict = db['cars']

            except:
                print("Error in retrieving Cars from car.db")

            car = Car.Car(create_car_form.car_name.data, create_car_form.car_model.data,
                          create_car_form.car_description.data, create_car_form.car_price.data,
                          create_car_form.car_quantity.data, create_car_form.car_availstartdate.data, create_car_form.car_availability.data, filename)
            if len(cars_dict)>0:
                car.set_car_id(list(cars_dict)[-1]+1)
            cars_dict[car.get_car_id()] = car
            db['cars'] = cars_dict

            db.close()

            session['car_created'] = car.get_car_model() + ' ' + car.get_car_name()

        return redirect(url_for('retrieve_admin_cars'))

    return render_template('createCar.html', form=create_car_form)


@app.route('/createElectricCar', methods=['GET', 'POST'])
def create_electric_car():
    create_electric_car_form = CreateElectricCarForm(request.form)
    if request.method == 'POST' and create_electric_car_form.validate():

        target = os.path.join(APP_ROOT, 'static/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            filename = file.filename
            print(filename)
            if filename == "=":
                flash("No image selected!")
                return redirect(request.url)
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)


            electric_cars_dict = {}
            db = shelve.open('electric_car.db', 'c')


            try:
                electric_cars_dict = db['electric_cars']

            except:
                print("Error in retrieving Electric Cars from electric_car.db")

            electric_car = ElectricCar.ElectricCar(create_electric_car_form.car_name.data, create_electric_car_form.car_model.data, create_electric_car_form.car_description.data, create_electric_car_form.car_price.data, create_electric_car_form.car_quantity.data,create_electric_car_form.car_availstartdate.data, create_electric_car_form.car_availability.data, create_electric_car_form.car_battery_capacity.data, create_electric_car_form.car_charging_duration.data, filename)
            if len(electric_cars_dict)>0:
                electric_car.set_electric_car_id(list(electric_cars_dict)[-1]+1)
            electric_cars_dict[electric_car.get_electric_car_id()] = electric_car
            db['electric_cars'] = electric_cars_dict

            db.close()

            session['car_created'] = electric_car.get_car_model() + ' ' + electric_car.get_car_name()

        return redirect(url_for('retrieve_admin_cars'))
    return render_template('createElectricCar.html', form=create_electric_car_form)


@app.route('/retrieveCarAdmin')
def retrieve_admin_cars():
    try:
        date = datetime.date.today()

        cars_dict = {}
        db = shelve.open('car.db', 'r')
        cars_dict = db['cars']
        db.close()

        electric_cars_dict = {}
        db = shelve.open('electric_car.db', 'r')
        electric_cars_dict = db['electric_cars']
        db.close()

        cars_list = []
        for key in cars_dict:
            car = cars_dict.get(key)
            if car.get_car_availstartdate() <= date:
                if car.get_car_quantity() == 0:
                    car.set_car_availability("Out-of-Stock")
                elif car.get_car_quantity() > 0:
                    car.set_car_availability("In Stock")
            elif car.get_car_availstartdate() > date:
                car.set_car_availability("Unavailable")

            cars_list.append(car)

        electric_cars_list = []
        for key in electric_cars_dict:
            electric_car = electric_cars_dict.get(key)
            if electric_car.get_car_availstartdate() <= date:
                if electric_car.get_car_quantity() == 0:
                    electric_car.set_car_availability("Out-of-Stock")
                elif electric_car.get_car_quantity() > 0:
                    electric_car.set_car_availability("In Stock")
            elif electric_car.get_car_availstartdate() > date:
                electric_car.set_car_availability("Unavailable")

            electric_cars_list.append(electric_car)

        return render_template('ManageAdminCar.html', count=len(cars_list), cars_list=cars_list, electric_cars_list=electric_cars_list)
    except:
        cars_list = []
        electric_cars_list = []
        return render_template('ManageAdminCar.html', count=len(cars_list), cars_list=cars_list, electric_cars_list=electric_cars_list)


@app.route('/updatecar/<int:id>/', methods=['GET', 'POST'])
def update_car(id):
    update_car_form = CreateCarForm(request.form)
    if request.method == 'POST' and update_car_form.validate():

        target = os.path.join(APP_ROOT, 'static/assets/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            filename = file.filename
            print(filename)
            if filename == "":
                cars_dict = {}
                db = shelve.open('car.db', 'w')
                cars_dict = db['cars']

                car = cars_dict.get(id)
                car.set_car_name(update_car_form.car_name.data)
                car.set_car_model(update_car_form.car_model.data)
                car.set_car_description(update_car_form.car_description.data)
                car.set_car_price(update_car_form.car_price.data)
                car.set_car_quantity(update_car_form.car_quantity.data)
                car.set_car_availstartdate(update_car_form.car_availstartdate.data)
                car.set_car_availability(update_car_form.car_availability.data)
                db['cars'] = cars_dict
                db.close()

            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                print(destination)
                file.save(destination)

                cars_dict = {}
                db = shelve.open('car.db', 'w')
                cars_dict = db['cars']

                car = cars_dict.get(id)
                car.set_car_name(update_car_form.car_name.data)
                car.set_car_model(update_car_form.car_model.data)
                car.set_car_description(update_car_form.car_description.data)
                car.set_car_price(update_car_form.car_price.data)
                car.set_car_quantity(update_car_form.car_quantity.data)
                car.set_car_availstartdate(update_car_form.car_availstartdate.data)
                car.set_car_availability(update_car_form.car_availability.data)
                car.set_car_image(filename)

                db['cars'] = cars_dict
                db.close()

        session['car_updated'] = car.get_car_model() + ' ' + car.get_car_name()

        return redirect(url_for('retrieve_admin_cars'))
    else:

        cars_dict = {}
        db = shelve.open('car.db', 'r')
        cars_dict = db['cars']
        db.close()

        car = cars_dict.get(id)
        update_car_form.car_name.data = car.get_car_name()
        update_car_form.car_model.data = car.get_car_model()
        update_car_form.car_description.data = car.get_car_description()
        update_car_form.car_price.data = car.get_car_price()
        update_car_form.car_quantity.data = car.get_car_quantity()
        update_car_form.car_availstartdate.data = car.get_car_availstartdate()
        update_car_form.car_availability.data = car.get_car_availability()
        update_car_form.filename = car.get_car_image()

        return render_template('updateCar.html', form=update_car_form, image=car.get_car_image())


@app.route('/updateElectricCar/<int:id>/', methods=['GET', 'POST'])
def update_electric_car(id):
    update_electric_car_form = CreateElectricCarForm(request.form)
    if request.method == 'POST' and update_electric_car_form.validate():

        target = os.path.join(APP_ROOT, 'static/assets/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            filename = file.filename
            print(filename)
            if filename == "":
                electric_cars_dict = {}
                db = shelve.open('electric_car.db', 'w')
                electric_cars_dict = db['electric_cars']

                electric_car = electric_cars_dict.get(id)
                electric_car.set_car_name(update_electric_car_form.car_name.data)
                electric_car.set_car_model(update_electric_car_form.car_model.data)
                electric_car.set_car_description(update_electric_car_form.car_description.data)
                electric_car.set_car_price(update_electric_car_form.car_price.data)
                electric_car.set_car_quantity(update_electric_car_form.car_quantity.data)
                electric_car.set_car_availstartdate(update_electric_car_form.car_availstartdate.data)
                electric_car.set_car_availability(update_electric_car_form.car_availability.data)
                electric_car.set_car_battery_capacity(update_electric_car_form.car_battery_capacity.data)
                electric_car.set_car_charging_duration(update_electric_car_form.car_charging_duration.data)

                db['electric_cars'] = electric_cars_dict
                db.close()
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                print(destination)
                file.save(destination)

                electric_cars_dict = {}
                db = shelve.open('electric_car.db', 'w')
                electric_cars_dict = db['electric_cars']

                electric_car = electric_cars_dict.get(id)
                electric_car.set_car_name(update_electric_car_form.car_name.data)
                electric_car.set_car_model(update_electric_car_form.car_model.data)
                electric_car.set_car_description(update_electric_car_form.car_description.data)
                electric_car.set_car_price(update_electric_car_form.car_price.data)
                electric_car.set_car_quantity(update_electric_car_form.car_quantity.data)
                electric_car.set_car_availstartdate(update_electric_car_form.car_availstartdate.data)
                electric_car.set_car_availability(update_electric_car_form.car_availability.data)
                electric_car.set_car_battery_capacity(update_electric_car_form.car_battery_capacity.data)
                electric_car.set_car_charging_duration(update_electric_car_form.car_charging_duration.data)
                electric_car.set_car_image(filename)

                db['electric_cars'] = electric_cars_dict
                db.close()

        session['car_updated'] = electric_car.get_car_model() + ' ' + electric_car.get_car_name()

        return redirect(url_for('retrieve_admin_cars'))
    else:
        electric_cars_dict = {}
        db = shelve.open('electric_car.db', 'r')
        electric_cars_dict = db['electric_cars']
        db.close()

        electric_car = electric_cars_dict.get(id)
        update_electric_car_form.car_name.data = electric_car.get_car_name()
        update_electric_car_form.car_model.data = electric_car.get_car_model()
        update_electric_car_form.car_description.data = electric_car.get_car_description()
        update_electric_car_form.car_price.data = electric_car.get_car_price()
        update_electric_car_form.car_quantity.data = electric_car.get_car_quantity()
        update_electric_car_form.car_availstartdate.data = electric_car.get_car_availstartdate()
        update_electric_car_form.car_availability.data = electric_car.get_car_availability()
        update_electric_car_form.car_battery_capacity.data = electric_car.get_car_battery_capacity()
        update_electric_car_form.car_charging_duration.data = electric_car.get_car_charging_duration()
        update_electric_car_form.filename = electric_car.get_car_image()

        return render_template('updateElectricCar.html', form=update_electric_car_form, image=electric_car.get_car_image())

# ZACHARY


@app.route('/createService', methods=['GET', 'POST'])
def create_service():
    create_service_form = CreateServiceForm(request.form)
    if request.method == 'POST' and create_service_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)

            services_dict = {}
            db = shelve.open('service.db', 'c')

            try:
                services_dict = db['Services']
            except:
                print("Error in creating Service from service.db.")

            service = Service.Service(create_service_form.name.data,
                                      filename,
                                      create_service_form.description.data,
                                      create_service_form.availability.data)

            if len(services_dict) > 0:
                service.set_service_id(list(services_dict)[-1] + 1)
            services_dict[service.get_service_id()] = service
            db['Services'] = services_dict

            db.close()

        return redirect(url_for('retrieve_service1'))
    return render_template('createService.html', form=create_service_form)


@app.route('/createCarservice', methods=['GET', 'POST'])
def create_carservice():
    create_carservice_form = CreateCarserviceForm(request.form)
    carservices_dict = {}
    db = shelve.open('carservice.db', 'c')
    if request.method == 'POST' and create_carservice_form.validate():

        target = os.path.join(APP_ROOT, 'static/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

            try:
                carservices_dict = db['Carservices']
            except:
                print("Error in creating Car Service from carservice.db.")

            carservice = Carservice.Carservice(create_carservice_form.name.data,
                                               filename,
                                               create_carservice_form.description.data,
                                               create_carservice_form.location.data,
                                               create_carservice_form.hotline.data,
                                               create_carservice_form.starting_hour.data,
                                               create_carservice_form.ending_hour.data,
                                               create_carservice_form.opening_days.data,
                                               create_carservice_form.availability.data)
            if len(carservices_dict) > 0:
                carservice.set_carservice_id(list(carservices_dict)[-1] + 1)
            carservices_dict[carservice.get_carservice_id()] = carservice
            db['Carservices'] = carservices_dict

            db.close()
        return redirect(url_for('retrieve_service1'))
    return render_template('createCarservice.html', form=create_carservice_form)


@app.route('/retrieveService1')
def retrieve_service1():
    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    return render_template('retrieveService1.html', count1=len(services_list), count2=len(carservices_list),
                           services_list=services_list, carservices_list=carservices_list, )


@app.route('/retrieveService')
def retrieve_service():
    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    return render_template('retrieveService.html', count1=len(services_list), services_list=services_list)


@app.route('/retrieveCarservice')
def retrieve_carservice():
    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    return render_template('retrieveCarservice.html', count2=len(carservices_list), carservices_list=carservices_list)


@app.route('/updateService/<int:id>/', methods=['GET', 'POST'])
def update_service(id):
    update_service_form = CreateServiceForm(request.form)
    if request.method == 'POST' and update_service_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                services_dict = {}
                db = shelve.open('service.db', 'w')
                services_dict = db['Services']

                service = services_dict.get(id)
                service.set_name(update_service_form.name.data)
                service.set_description(update_service_form.description.data)
                service.set_availability(update_service_form.availability.data)

                db['Services'] = services_dict
                db.close()
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)

                services_dict = {}
                db = shelve.open('service.db', 'w')
                services_dict = db['Services']

                service = services_dict.get(id)
                service.set_name(update_service_form.name.data)
                service.set_image(filename)
                service.set_description(update_service_form.description.data)
                service.set_availability(update_service_form.availability.data)

                db['Services'] = services_dict
                db.close()

        return redirect(url_for('retrieve_service1'))
    else:
        services_dict = {}
        db = shelve.open('service.db', 'r')
        services_dict = db['Services']
        db.close()

        service = services_dict.get(id)
        update_service_form.name.data = service.get_name()
        filename = service.get_image()
        update_service_form.description.data = service.get_description()
        update_service_form.availability.data = service.get_availability()

        return render_template('updateService.html', form=update_service_form)


@app.route('/updateCarservice/<int:id>/', methods=['GET', 'POST'])
def update_carservice(id):
    update_carservice_form = CreateCarserviceForm(request.form)
    if request.method == 'POST' and update_carservice_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                carservices_dict = {}
                db = shelve.open('carservice.db', 'w')
                carservices_dict = db['Carservices']

                carservice = carservices_dict.get(id)
                carservice.set_name(update_carservice_form.name.data)
                carservice.set_description(update_carservice_form.description.data)
                carservice.set_location(update_carservice_form.location.data)
                carservice.set_hotline(update_carservice_form.hotline.data)
                carservice.set_starting_hour(update_carservice_form.starting_hour.data)
                carservice.set_ending_hour(update_carservice_form.ending_hour.data)
                carservice.set_opening_days(update_carservice_form.opening_days.data)
                carservice.set_availability(update_carservice_form.availability.data)

                db['Carservices'] = carservices_dict
                db.close()
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)

                carservices_dict = {}
                db = shelve.open('carservice.db', 'w')
                carservices_dict = db['Carservices']

                carservice = carservices_dict.get(id)
                carservice.set_name(update_carservice_form.name.data)
                carservice.set_image(filename)
                carservice.set_description(update_carservice_form.description.data)
                carservice.set_location(update_carservice_form.location.data)
                carservice.set_hotline(update_carservice_form.hotline.data)
                carservice.set_starting_hour(update_carservice_form.starting_hour.data)
                carservice.set_ending_hour(update_carservice_form.ending_hour.data)
                carservice.set_opening_days(update_carservice_form.opening_days.data)
                carservice.set_availability(update_carservice_form.availability.data)

                db['Carservices'] = carservices_dict
                db.close()

        return redirect(url_for('retrieve_service1'))
    else:
        carservices_dict = {}
        db = shelve.open('carservice.db', 'r')
        carservices_dict = db['Carservices']
        db.close()

        carservice = carservices_dict.get(id)
        update_carservice_form.name.data = carservice.get_name()
        filename = carservice.get_image()
        update_carservice_form.description.data = carservice.get_description()
        update_carservice_form.location.data = carservice.get_location()
        update_carservice_form.hotline.data = carservice.get_hotline()
        update_carservice_form.starting_hour.data = carservice.get_starting_hour()
        update_carservice_form.ending_hour.data = carservice.get_ending_hour()
        update_carservice_form.opening_days.data = carservice.get_opening_days()
        update_carservice_form.availability.data = carservice.get_availability()

        return render_template('updateCarservice.html', form=update_carservice_form)


@app.route('/deleteService/<int:id>', methods=['POST'])
def delete_service(id):
    services_dict = {}
    db = shelve.open('service.db', 'w')
    services_dict = db['Services']

    services_dict.pop(id)

    db['Services'] = services_dict
    db.close()

    return redirect(url_for('retrieve_service1'))


@app.route('/deleteCarservice/<int:id>', methods=['POST'])
def delete_carservice(id):
    carservices_dict = {}
    db = shelve.open('carservice.db', 'w')
    carservices_dict = db['Carservices']

    carservices_dict.pop(id)

    db['Carservices'] = carservices_dict
    db.close()

    return redirect(url_for('retrieve_service1'))

# BRANDON


@app.route('/createPublicEvent', methods=['GET', 'POST'])
def create_PublicEvent():
    create_publicevent_form = createPublicEventForm(request.form)
    if request.method == 'POST' and create_publicevent_form.validate():

        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)

            publicevent_dict = {}
            db = shelve.open('publicevent.db', 'c')

            try:
                publicevent_dict = db['publicevent']
            except:
                print("Error in retrieving publicevent from publicevent.db")

            publicevent = PublicEvent.PublicEvent(create_publicevent_form.startDate.data,
                                                  create_publicevent_form.endDate.data,
                                                  create_publicevent_form.startTime.data,
                                                  create_publicevent_form.endTime.data,
                                                  create_publicevent_form.venue.data, create_publicevent_form.cost.data,
                                                  create_publicevent_form.capacity.data,
                                                  create_publicevent_form.title.data, filename)

            if len(publicevent_dict) > 0:
                publicevent.set_publiceventid(list(publicevent_dict)[-1] + 1)
            publicevent_dict[publicevent.get_publiceventid()] = publicevent
            db['publicevent'] = publicevent_dict

            db.close()

        return redirect('/retrieveAllEvent')
    return render_template('createPublicEvent.html', form=create_publicevent_form)


@app.route('/createInternalEvent', methods=['GET', 'POST'])
def create_InternalEvent():
    create_internalevent_form = createInternalEventForm(request.form)
    if request.method == 'POST' and create_internalevent_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)

            internalevent_dict = {}
            db = shelve.open('internalevent.db', 'c')
            try:
                internalevent_dict = db['internalevent']
            except:
                print("Error in retrieving internalevent from internalevent.db.")

            internalevent = InternalEvent.InternalEvent(create_internalevent_form.startDate.data,
                                                        create_internalevent_form.endDate.data,
                                                        create_internalevent_form.startTime.data,
                                                        create_internalevent_form.endTime.data,
                                                        create_internalevent_form.venue.data,
                                                        create_internalevent_form.cost.data,
                                                        create_internalevent_form.capacity.data,
                                                        create_internalevent_form.title.data, filename,
                                                        create_internalevent_form.fullname.data,
                                                        create_internalevent_form.attendance.data)

            if len(internalevent_dict) > 0:
                internalevent.set_internalEventId(list(internalevent_dict)[-1] + 1)
            internalevent_dict[internalevent.get_internaleventid()] = internalevent
            db['internalevent'] = internalevent_dict

            db.close()

        return redirect('/retrieveAllEvent')
    return render_template('createInternalEvent.html', form=create_internalevent_form)


@app.route('/retrieveAllEvent')
def retrieve_AllEvent():
    publicevent_dict = {}
    db = shelve.open('publicevent.db', 'r')
    publicevent_dict = db['publicevent']
    db.close()

    publicevent_list = []
    for key in publicevent_dict:
        publicevent = publicevent_dict.get(key)
        publicevent_list.append(publicevent)

    internalevent_dict = {}
    db = shelve.open('internalevent.db', 'r')
    internalevent_dict = db['internalevent']
    db.close()

    internalevent_list = []
    for key in internalevent_dict:
        internalevent = internalevent_dict.get(key)
        internalevent_list.append(internalevent)

    current_date = datetime.date.today()

    return render_template('retrieveAllEvent.html', count1=len(publicevent_list), publicevent_list=publicevent_list,
                           count2=len(internalevent_list), internalevent_list=internalevent_list, current_date=current_date)


@app.route('/retrievePublicEvent')
def retrieve_PublicEvent():
    publicevent_dict = {}
    db = shelve.open('publicevent.db', 'r')
    publicevent_dict = db['publicevent']
    db.close()

    publicevent_list = []
    for key in publicevent_dict:
        publicevent = publicevent_dict.get(key)
        publicevent_list.append(publicevent)


    current_date = datetime.date.today()

    return render_template('retrievePublicEvent.html', count1=len(publicevent_list), publicevent_list=publicevent_list, current_date=current_date)


@app.route('/retrieveInternalEvent')
def retrieve_InternalEvent():
    internalevent_dict = {}
    db = shelve.open('internalevent.db', 'r')
    internalevent_dict = db['internalevent']
    db.close()

    internalevent_list = []
    for key in internalevent_dict:
        internalevent = internalevent_dict.get(key)
        internalevent_list.append(internalevent)

    current_date = datetime.date.today()

    return render_template('retrieveInternalEvent.html', count2=len(internalevent_list), internalevent_list=internalevent_list, current_date=current_date)


@app.route('/updatePublicEvent/<int:id>/', methods=['GET', 'POST'])
def update_PublicEvent(id):
    publicevent_dict = {}
    db = shelve.open('publicevent.db', 'r')
    publicevent_dict = db['publicevent']
    db.close()

    publicevent_list = []
    for key in publicevent_dict:
        publicevent = publicevent_dict.get(key)
        publicevent_list.append(publicevent)

    update_publicevent_form = createPublicEventForm(request.form)
    if request.method == 'POST' and update_publicevent_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                publicevent_dict = {}
                db = shelve.open('publicevent.db', 'w')
                publicevent_dict = db['publicevent']

                publicevent = publicevent_dict.get(id)
                publicevent.set_startDate(update_publicevent_form.startDate.data)
                publicevent.set_endDate(update_publicevent_form.endDate.data)
                publicevent.set_startTime(update_publicevent_form.startTime.data)
                publicevent.set_endTime(update_publicevent_form.endTime.data)
                publicevent.set_venue(update_publicevent_form.venue.data)
                publicevent.set_cost(update_publicevent_form.cost.data)
                publicevent.set_capacity(update_publicevent_form.capacity.data)
                publicevent.set_title(update_publicevent_form.title.data)
                publicevent.get_image()

                db['publicevent'] = publicevent_dict
                db.close()

            else:
                destination = "/".join([target, filename])
                file.save(destination)

                publicevent_dict = {}
                db = shelve.open('publicevent.db', 'w')
                publicevent_dict = db['publicevent']

                publicevent = publicevent_dict.get(id)
                publicevent.set_startDate(update_publicevent_form.startDate.data)
                publicevent.set_endDate(update_publicevent_form.endDate.data)
                publicevent.set_startTime(update_publicevent_form.startTime.data)
                publicevent.set_endTime(update_publicevent_form.endTime.data)
                publicevent.set_venue(update_publicevent_form.venue.data)
                publicevent.set_cost(update_publicevent_form.cost.data)
                publicevent.set_capacity(update_publicevent_form.capacity.data)
                publicevent.set_title(update_publicevent_form.title.data)
                publicevent.set_image(filename)

                db['publicevent'] = publicevent_dict
                db.close()

        return redirect(url_for('retrieve_AllEvent'))
    else:
        publicevent_dict = {}
        db = shelve.open('publicevent.db', 'r')
        publicevent_dict = db['publicevent']
        db.close()

        publicevent = publicevent_dict.get(id)
        update_publicevent_form.startDate.data = publicevent.get_startDate()
        update_publicevent_form.endDate.data = publicevent.get_endDate()
        update_publicevent_form.startTime.data = publicevent.get_startTime()
        update_publicevent_form.endTime.data = publicevent.get_endTime()
        update_publicevent_form.venue.data = publicevent.get_venue()
        update_publicevent_form.cost.data = publicevent.get_cost()
        update_publicevent_form.capacity.data = publicevent.get_capacity()
        update_publicevent_form.title.data = publicevent.get_title()
        filename = publicevent.get_image()


        return render_template('updatePublicEvent.html', form=update_publicevent_form, publicevent_list=publicevent_list, publicevent=publicevent)


@app.route('/updateInternalEvent/<int:id>/', methods=['GET', 'POST'])
def update_InternalEvent(id):
    update_internalevent_form = createInternalEventForm(request.form)
    if request.method == 'POST' and update_internalevent_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == '':

                internalevent_dict = {}
                db = shelve.open('internalevent.db', 'w')
                internalevent_dict = db['internalevent']

                internalevent = internalevent_dict.get(id)
                internalevent.set_startDate(update_internalevent_form.startDate.data)
                internalevent.set_endDate(update_internalevent_form.endDate.data)
                internalevent.set_startTime(update_internalevent_form.startTime.data)
                internalevent.set_endTime(update_internalevent_form.endTime.data)
                internalevent.set_venue(update_internalevent_form.venue.data)
                internalevent.set_cost(update_internalevent_form.cost.data)
                internalevent.set_capacity(update_internalevent_form.capacity.data)
                internalevent.set_title(update_internalevent_form.title.data)
                internalevent.set_fullname(update_internalevent_form.fullname.data)
                internalevent.set_attendance(update_internalevent_form.attendance.data)
                internalevent.get_image()

                db['internalevent'] = internalevent_dict
                db.close()
            else:
                destination = "/".join([target, filename])
                file.save(destination)

                internalevent_dict = {}
                db = shelve.open('internalevent.db', 'w')
                internalevent_dict = db['internalevent']

                internalevent = internalevent_dict.get(id)
                internalevent.set_startDate(update_internalevent_form.startDate.data)
                internalevent.set_endDate(update_internalevent_form.endDate.data)
                internalevent.set_startTime(update_internalevent_form.startTime.data)
                internalevent.set_endTime(update_internalevent_form.endTime.data)
                internalevent.set_venue(update_internalevent_form.venue.data)
                internalevent.set_cost(update_internalevent_form.cost.data)
                internalevent.set_capacity(update_internalevent_form.capacity.data)
                internalevent.set_title(update_internalevent_form.title.data)
                internalevent.set_fullname(update_internalevent_form.fullname.data)
                internalevent.set_attendance(update_internalevent_form.attendance.data)
                internalevent.set_image(filename)

                db['internalevent'] = internalevent_dict
                db.close()

        return redirect(url_for('retrieve_AllEvent'))
    else:
        internalevent_dict = {}
        db = shelve.open('internalevent.db', 'r')
        internalevent_dict = db['internalevent']
        db.close()

        internalevent = internalevent_dict.get(id)
        update_internalevent_form.startDate.data = internalevent.get_startDate()
        update_internalevent_form.endDate.data = internalevent.get_endDate()
        update_internalevent_form.startTime.data = internalevent.get_startTime()
        update_internalevent_form.endTime.data = internalevent.get_endTime()
        update_internalevent_form.venue.data = internalevent.get_venue()
        update_internalevent_form.cost.data = internalevent.get_cost()
        update_internalevent_form.capacity.data = internalevent.get_capacity()
        update_internalevent_form.title.data = internalevent.get_title()
        update_internalevent_form.fullname.data = internalevent.get_fullname()
        update_internalevent_form.attendance.data = internalevent.get_attendance()
        filename = internalevent.get_image()

        return render_template('updateinternalevent.html', form=update_internalevent_form, internalevent=internalevent)

# ALVIN


@app.route('/createAccessory', methods=['GET', 'POST'])
def create_accessory():
    create_accessory_form = CreateAccessoryForm(request.form)
    if request.method == 'POST' and create_accessory_form.validate():
        date = datetime.date.today()
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                flash("No image selected!")
                return redirect(request.url)
            elif not filename.lower().endswith(('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tif, tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)
                db = shelve.open('accessory.db', 'c')
                accessories_dict = db['Accessories']

                accessory = Accessory.Accessory(filename,
                                                create_accessory_form.name.data,
                                                create_accessory_form.description.data,
                                                create_accessory_form.price.data,
                                                create_accessory_form.quantity.data,
                                                create_accessory_form.start.data,
                                                date,
                                                create_accessory_form.end.data,
                                                create_accessory_form.status.data)
                if len(accessories_dict) > 0:
                    accessory.set_accessory_id(list(accessories_dict)[-1] + 1)
                accessories_dict[accessory.get_accessory_id()] = accessory
                db['Accessories'] = accessories_dict

                db.close()

        return redirect(url_for('retrieve_accessory'))
    return render_template('createAccessory.html', form=create_accessory_form)


@app.route('/createElectronicAccessory', methods=['GET', 'POST'])
def create_electronicaccessory():
    create_electronicaccessory_form = CreateElectronicAccessoryForm(request.form)
    if request.method == 'POST' and create_electronicaccessory_form.validate():
        date = datetime.date.today()
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                flash("No image selected!")
                return redirect(request.url)
            elif not filename.lower().endswith(('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tif, tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)
                db = shelve.open('electronicaccessory.db', 'c')
                electronicaccessory_dict = db['ElectronicAccessories']

                electronicaccessory = ElectronicAccessory.ElectronicAccessory(filename,
                                                                              create_electronicaccessory_form.name.data,
                                                                              create_electronicaccessory_form.description.data,
                                                                              create_electronicaccessory_form.price.data,
                                                                              create_electronicaccessory_form.quantity.data,
                                                                              create_electronicaccessory_form.battery_type.data,
                                                                              create_electronicaccessory_form.batteries_required.data,
                                                                              create_electronicaccessory_form.start.data,
                                                                              date,
                                                                              create_electronicaccessory_form.end.data,
                                                                              create_electronicaccessory_form.status.data)
                if len(electronicaccessory_dict) > 0:
                    electronicaccessory.set_electronicaccessory_id(list(electronicaccessory_dict)[-1] + 1)
                electronicaccessory_dict[electronicaccessory.get_electronicaccessory_id()] = electronicaccessory
                db['ElectronicAccessories'] = electronicaccessory_dict

                db.close()
        return redirect(url_for('retrieve_electronicaccessory'))
    return render_template('createElectronicAccessory.html', form=create_electronicaccessory_form)


@app.route('/retrieveAccessory')
def retrieve_accessory():
    date = datetime.date.today()
    db = shelve.open('accessory.db', 'r')
    accessories_dict = db['Accessories']
    db.close()

    accessories_list = []
    for key in accessories_dict:
        accessory = accessories_dict.get(key)
        if not accessory.get_end() is None:
            if accessory.get_start() <= date < accessory.get_end():
                if accessory.get_quantity() == 0:
                    accessory.set_status("Out of Stock")
                elif accessory.get_quantity() > 0:
                    accessory.set_status("In Stock")
            elif accessory.get_start() > date:
                accessory.set_status("Unavailable")
            elif accessory.get_end() <= date:
                accessory.set_status("Unavailable")
            accessories_list.append(accessory)
        else:
            if accessory.get_start() <= date:
                if accessory.get_quantity() == 0:
                    accessory.set_status("Out of Stock")
                elif accessory.get_quantity() > 0:
                    accessory.set_status("In Stock")
            else:
                accessory.set_status("Unavailable")
            accessories_list.append(accessory)

    return render_template('retrieveAccessory.html', count=len(accessories_list), accessories_list=accessories_list)


@app.route('/retrieveElectronicAccessory')
def retrieve_electronicaccessory():
    date = datetime.date.today()
    db = shelve.open('electronicaccessory.db', 'r')
    electronicaccessory_dict = db['ElectronicAccessories']
    db.close()

    electronicaccessory_list = []
    for key in electronicaccessory_dict:
        electronicaccessory = electronicaccessory_dict.get(key)
        if not electronicaccessory.get_end() is None:
            if electronicaccessory.get_start() <= date < electronicaccessory.get_end():
                if electronicaccessory.get_quantity() == 0:
                    electronicaccessory.set_status("Out of Stock")
                elif electronicaccessory.get_quantity() > 0:
                    electronicaccessory.set_status("In Stock")
            elif electronicaccessory.get_start() > date:
                electronicaccessory.set_status("Unavailable")
            elif electronicaccessory.get_end() <= date:
                electronicaccessory.set_status("Unavailable")
            electronicaccessory_list.append(electronicaccessory)
        else:
            if electronicaccessory.get_start() <= date:
                if electronicaccessory.get_quantity() == 0:
                    electronicaccessory.set_status("Out of Stock")
                elif electronicaccessory.get_quantity() > 0:
                    electronicaccessory.set_status("In Stock")
            else:
                electronicaccessory.set_status("Unavailable")
            electronicaccessory_list.append(electronicaccessory)

    return render_template('retrieveElectronicAccessory.html', count=len(electronicaccessory_list),
                           electronicaccessory_list=electronicaccessory_list)


@app.route('/updateAccessory/<int:accessory_id>/', methods=['GET', 'POST'])
def update_accessory(accessory_id):
    update_accessory_form = CreateAccessoryForm(request.form)
    if request.method == 'POST' and update_accessory_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                db = shelve.open('accessory.db', 'w')
                accessories_dict = db['Accessories']

                accessory = accessories_dict.get(accessory_id)
                accessory.set_name(update_accessory_form.name.data)
                accessory.set_name(update_accessory_form.name.data)
                accessory.set_description(update_accessory_form.description.data)
                accessory.set_price(update_accessory_form.price.data)
                accessory.set_quantity(update_accessory_form.quantity.data)
                accessory.set_start(update_accessory_form.start.data)
                accessory.set_end(update_accessory_form.end.data)
                accessory.set_status(update_accessory_form.status.data)
                db['Accessories'] = accessories_dict
                db.close()
            elif not filename.lower().endswith(('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tif, tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)
                db = shelve.open('accessory.db', 'w')
                accessories_dict = db['Accessories']

                accessory = accessories_dict.get(accessory_id)
                accessory.set_image(filename)
                accessory.set_name(update_accessory_form.name.data)
                accessory.set_description(update_accessory_form.description.data)
                accessory.set_price(update_accessory_form.price.data)
                accessory.set_quantity(update_accessory_form.quantity.data)
                accessory.set_start(update_accessory_form.start.data)
                accessory.set_end(update_accessory_form.end.data)
                accessory.set_status(update_accessory_form.status.data)
                db['Accessories'] = accessories_dict
                db.close()

        return redirect(url_for('retrieve_accessory'))
    else:
        db = shelve.open('accessory.db', 'r')
        accessories_dict = db['Accessories']
        db.close()

        accessory = accessories_dict.get(accessory_id)
        update_accessory_form.name.data = accessory.get_name()
        update_accessory_form.filename = accessory.get_image()
        update_accessory_form.description.data = accessory.get_description()
        update_accessory_form.price.data = accessory.get_price()
        update_accessory_form.quantity.data = accessory.get_quantity()
        update_accessory_form.start.data = accessory.get_start()
        update_accessory_form.end.data = accessory.get_end()
        update_accessory_form.status.data = accessory.get_status()

        return render_template('updateAccessory.html', form=update_accessory_form, image=accessory.get_image())


@app.route('/updateElectronicAccessory/<int:electronic_accessory_id>/', methods=['GET', 'POST'])
def update_electronicaccessory(electronic_accessory_id):
    update_electronicaccessory_form = CreateElectronicAccessoryForm(request.form)
    if request.method == 'POST' and update_electronicaccessory_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                db = shelve.open('electronicaccessory.db', 'w')
                electronicaccessory_dict = db['ElectronicAccessories']

                electronicaccessory = electronicaccessory_dict.get(electronic_accessory_id)
                electronicaccessory.set_name(update_electronicaccessory_form.name.data)
                electronicaccessory.set_description(update_electronicaccessory_form.description.data)
                electronicaccessory.set_price(update_electronicaccessory_form.price.data)
                electronicaccessory.set_quantity(update_electronicaccessory_form.quantity.data)
                electronicaccessory.set_battery_type(update_electronicaccessory_form.battery_type.data)
                electronicaccessory.set_batteries_required(update_electronicaccessory_form.batteries_required.data)
                electronicaccessory.set_start(update_electronicaccessory_form.start.data)
                electronicaccessory.set_end(update_electronicaccessory_form.end.data)
                electronicaccessory.set_status(update_electronicaccessory_form.status.data)
                db['Accessories'] = electronicaccessory_dict

                db['ElectronicAccessories'] = electronicaccessory_dict
                db.close()
            elif not filename.lower().endswith(('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tif, tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)
                db = shelve.open('electronicaccessory.db', 'w')
                electronicaccessory_dict = db['ElectronicAccessories']

                electronicaccessory = electronicaccessory_dict.get(electronic_accessory_id)
                electronicaccessory.set_image(filename)
                electronicaccessory.set_name(update_electronicaccessory_form.name.data)
                electronicaccessory.set_description(update_electronicaccessory_form.description.data)
                electronicaccessory.set_price(update_electronicaccessory_form.price.data)
                electronicaccessory.set_quantity(update_electronicaccessory_form.quantity.data)
                electronicaccessory.set_battery_type(update_electronicaccessory_form.battery_type.data)
                electronicaccessory.set_batteries_required(update_electronicaccessory_form.batteries_required.data)
                electronicaccessory.set_start(update_electronicaccessory_form.start.data)
                electronicaccessory.set_end(update_electronicaccessory_form.end.data)
                electronicaccessory.set_status(update_electronicaccessory_form.status.data)
                db['Accessories'] = electronicaccessory_dict

                db['ElectronicAccessories'] = electronicaccessory_dict
                db.close()

        return redirect(url_for('retrieve_electronicaccessory'))
    else:
        db = shelve.open('electronicaccessory.db', 'r')
        electronicaccessory_dict = db['ElectronicAccessories']
        db.close()

        electronicaccessory = electronicaccessory_dict.get(electronic_accessory_id)
        update_electronicaccessory_form.name.data = electronicaccessory.get_name()
        update_electronicaccessory_form.filename = electronicaccessory.get_image()
        update_electronicaccessory_form.description.data = electronicaccessory.get_description()
        update_electronicaccessory_form.price.data = electronicaccessory.get_price()
        update_electronicaccessory_form.quantity.data = electronicaccessory.get_quantity()
        update_electronicaccessory_form.battery_type.data = electronicaccessory.get_battery_type()
        update_electronicaccessory_form.batteries_required.data = electronicaccessory.get_batteries_required()
        update_electronicaccessory_form.start.data = electronicaccessory.get_start()
        update_electronicaccessory_form.end.data = electronicaccessory.get_end()
        update_electronicaccessory_form.status.data = electronicaccessory.get_status()

        return render_template('updateElectronicAccessory.html', form=update_electronicaccessory_form,
                               image=electronicaccessory.get_image())


@app.route('/deleteAccessory/<int:accessory_id>', methods=['POST'])
def delete_accessory(accessory_id):
    db = shelve.open('accessory.db', 'w')
    accessories_dict = db['Accessories']

    accessories_dict.pop(accessory_id)

    db['Accessories'] = accessories_dict
    db.close()

    return redirect(url_for('retrieve_accessory'))


@app.route('/deleteElectronicAccessory/<int:electronic_accessory_id>', methods=['POST'])
def delete_electronicaccessory(electronic_accessory_id):
    db = shelve.open('electronicaccessory.db', 'w')
    electronicaccessory_dict = db['ElectronicAccessories']

    electronicaccessory_dict.pop(electronic_accessory_id)

    db['ElectronicAccessories'] = electronicaccessory_dict
    db.close()

    return redirect(url_for('retrieve_electronicaccessory'))


@app.route('/featured')
def featured():
    date = datetime.date.today()
    dbfeatured = shelve.open('featured.db', 'r')
    featureditem = dbfeatured['Featured']
    print(featureditem)
    dbfeatured.close()
    db = shelve.open('accessory.db', 'r')
    accessories_dict = db['Accessories']
    db.close()
    db = shelve.open('electronicaccessory.db', 'r')
    electronicaccessory_dict = db['ElectronicAccessories']
    db.close()
    db = shelve.open('car.db', 'r')
    cars_dict = db['cars']
    db.close()
    db = shelve.open('electric_car.db', 'r')
    electric_cars_dict = db['electric_cars']
    db.close()

    accessory_list = []
    electronicaccessory_list = []
    car_list = []
    electriccar_list = []
    for key in accessories_dict:
        accessory = accessories_dict.get(key)
        if not accessory.get_end() is None:
            if accessory.get_start() <= date < accessory.get_end():
                if accessory.get_quantity() == 0:
                    accessory.set_status("Out of Stock")
                elif accessory.get_quantity() > 0:
                    accessory.set_status("In Stock")
                    accessory_list.append(accessory)
            elif accessory.get_start() > date:
                accessory.set_status("Unavailable")
            elif accessory.get_end() <= date:
                accessory.set_status("Unavailable")

        else:
            if accessory.get_start() <= date:
                if accessory.get_quantity() == 0:
                    accessory.set_status("Out of Stock")
                elif accessory.get_quantity() > 0:
                    accessory.set_status("In Stock")
                    accessory_list.append(accessory)
            else:
                accessory.set_status("Unavailable")


    for key in electronicaccessory_dict:
        electronicaccessory = electronicaccessory_dict.get(key)
        if not electronicaccessory.get_end() is None:
            if electronicaccessory.get_start() <= date < electronicaccessory.get_end():
                if electronicaccessory.get_quantity() == 0:
                    electronicaccessory.set_status("Out of Stock")
                elif electronicaccessory.get_quantity() > 0:
                    electronicaccessory.set_status("In Stock")
                    electronicaccessory_list.append(electronicaccessory)
            elif electronicaccessory.get_start() > date:
                electronicaccessory.set_status("Unavailable")
            elif electronicaccessory.get_end() <= date:
                electronicaccessory.set_status("Unavailable")

        else:
            if electronicaccessory.get_start() <= date:
                if electronicaccessory.get_quantity() == 0:
                    electronicaccessory.set_status("Out of Stock")
                elif electronicaccessory.get_quantity() > 0:
                    electronicaccessory.set_status("In Stock")
                    electronicaccessory_list.append(electronicaccessory)
            else:
                electronicaccessory.set_status("Unavailable")


    for key in cars_dict:
        car = cars_dict.get(key)
        if car.get_car_availstartdate() <= date:
            if car.get_car_quantity() == 0:
                car.set_car_availability("Out-of-Stock")
            elif car.get_car_quantity() > 0:
                car.set_car_availability("In Stock")
                car_list.append(car)
        elif car.get_car_availstartdate() > date:
            car.set_car_availability("Unavailable")


    for key in electric_cars_dict:
        electric_car = electric_cars_dict.get(key)
        if electric_car.get_car_availstartdate() <= date:
            if electric_car.get_car_quantity() == 0:
                electric_car.set_car_availability("Out-of-Stock")
            elif electric_car.get_car_quantity() > 0:
                electric_car.set_car_availability("In Stock")
                electriccar_list.append(electric_car)
        elif electric_car.get_car_availstartdate() > date:
            electric_car.set_car_availability("Unavailable")


    return render_template('Featured.html', accessory_list=accessory_list, electronicaccessory_list=electronicaccessory_list, car_list=car_list, electriccar_list=electriccar_list, featureditem=featureditem)

@app.route('/addfeatured1/<int:accessory_id>/')
def addfeatured1(accessory_id):
    db = shelve.open('featured.db', 'c')
    db2 = shelve.open('accessory.db', 'r')
    accessory_dict = db2['Accessories']
    accessory = accessory_dict.get(accessory_id)
    featuredaccessory = {}
    featuredaccessory['featured'] = accessory.get_image()
    featuredaccessory['car'] = False
    featured_dict = featuredaccessory
    db['Featured'] = featured_dict
    db.close()
    db2.close()
    return redirect(url_for('featured'))


@app.route('/addwishlist1/<int:accessory_id>/')
def addwishlist1(accessory_id):
    db = shelve.open('wishlist.db', 'c')
    db2 = shelve.open('accessory.db', 'r')
    accessory_dict = db2['Accessories']
    accessory = accessory_dict.get(accessory_id)
    wishlist = {}
    try:
        wishlist = db['Wishlist']
    except:
        print("Error in retrieving wishlist.db")

    if wishlist.get(session['email']) is None:
        wishlist[session['email']] = []
    print(accessory)
    print(wishlist.get(session['email']))
    if accessory not in wishlist.get(session['email']):
        wishlist[session['email']].append(accessory)

    else:
        session['wish_exists'] = "hello"
        print("hello")
    db['Wishlist'] = wishlist
    print(wishlist)
    db.close()
    db2.close()
    return redirect(url_for('home'))


@app.route('/addfeatured2/<int:electronic_accessory_id>/')
def addfeatured2(electronic_accessory_id):
    db = shelve.open('featured.db', 'c')
    db2 = shelve.open('electronicaccessory.db', 'r')
    accessory_dict = db2['ElectronicAccessories']
    accessory = accessory_dict.get(electronic_accessory_id)
    featuredaccessory = {}
    featuredaccessory['featured'] = accessory.get_image()
    featuredaccessory['car'] = False
    featured_dict = featuredaccessory
    db['Featured'] = featured_dict
    db.close()
    db2.close()
    return redirect(url_for('featured'))

@app.route('/addwishlist2/<int:electronic_accessory_id>/')
def addwishlist2(electronic_accessory_id):
    db = shelve.open('wishlist.db', 'c')
    db2 = shelve.open('electronicaccessory.db', 'r')
    accessory_dict = db2['ElectronicAccessories']
    accessory = accessory_dict.get(electronic_accessory_id)
    wishlist = {}
    try:
        wishlist = db['Wishlist']
    except:
        print("Error in retrieving wishlist.db")

    if wishlist.get(session['email']) is None:
        wishlist[session['email']] = []
    wishlist[session['email']].append(accessory)
    db['Wishlist'] = wishlist
    print(wishlist)
    db.close()
    db2.close()
    return redirect(url_for('home'))

@app.route('/addfeatured3/<int:id>/')
def addfeatured3(id):
    db = shelve.open('featured.db', 'c')
    db2 = shelve.open('car.db', 'r')
    accessory_dict = db2['cars']
    accessory = accessory_dict.get(id)
    featuredaccessory = {}
    featuredaccessory['featured'] = accessory.get_car_image()
    featuredaccessory['car'] = True
    featured_dict = featuredaccessory
    db['Featured'] = featured_dict
    db.close()
    db2.close()
    return redirect(url_for('featured'))

@app.route('/addwishlist3/<int:id>/')
def addwishlist3(id):
    db = shelve.open('wishlist.db', 'c')
    db2 = shelve.open('car.db', 'r')
    accessory_dict = db2['cars']
    accessory = accessory_dict.get(id)
    wishlist = {}
    try:
        wishlist = db['Wishlist']
    except:
        print("Error in retrieving wishlist.db")

    if wishlist.get(session['email']) is None:
        wishlist[session['email']] = []
    wishlist[session['email']].append(accessory)
    db['Wishlist'] = wishlist
    print(wishlist)
    db.close()
    db2.close()
    return redirect(url_for('home'))

@app.route('/addfeatured4/<int:id>/')
def addfeatured4(id):
    db = shelve.open('featured.db', 'c')
    db2 = shelve.open('electric_car.db', 'r')
    accessory_dict = db2['electric_cars']
    accessory = accessory_dict.get(id)
    featuredaccessory = {}
    featuredaccessory['featured'] = accessory.get_car_image()
    featuredaccessory['car'] = True
    featured_dict = featuredaccessory
    db['Featured'] = featured_dict
    db.close()
    db2.close()
    return redirect(url_for('featured'))

@app.route('/addwishlist4/<int:id>/')
def addwishlist4(id):
    db = shelve.open('wishlist.db', 'c')
    db2 = shelve.open('electric_car.db', 'r')
    accessory_dict = db2['electric_cars']
    accessory = accessory_dict.get(id)
    wishlist = {}
    try:
        wishlist = db['Wishlist']
    except:
        print("Error in retrieving wishlist.db")

    if wishlist.get(session['email']) is None:
        wishlist[session['email']] = []
    wishlist[session['email']].append(accessory)
    db['Wishlist'] = wishlist
    print(wishlist)
    db.close()
    db2.close()
    return redirect(url_for('home'))


@app.route('/removewishlist/<index>/')
def removewishlist(index):
    db = shelve.open('wishlist.db', 'c')
    wishlist = {}
    wishlist = db['Wishlist']
    wishes = wishlist.get(session['email'])
    wishes.pop(int(index))
    session['wish_removed'] = "An item has been removed from your wishlist"
    wishlist[session['email']] = wishes
    db['Wishlist'] = wishlist
    db.close()

    return redirect(url_for('wishlist'))

if __name__ == '__main__':
    app.run(debug=True)
