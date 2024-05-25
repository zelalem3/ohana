import requests
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import bleach
import datetime
from datetime import timedelta
from flask import abort, jsonify


current_year = datetime.datetime.now().year
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key_here"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = timedelta(seconds=28800)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    books = db.relationship('Book', backref='user', lazy=True)
    password = db.Column(db.String(30), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    access_level = db.Column(db.String, default="normal")

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    event_description = db.Column(db.String(30), nullable=False)
    detailed_description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Event {self.event_description}>'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    specfic_request = db.Column(db.String)
    booked_date = db.Column(db.String, default=datetime.date.today().strftime("%B %d, %Y"))
    booked_for = db.Column(db.String, nullable=False)
    event_type = db.Column(db.String)
    event = db.relationship('Event', backref='bookings')

    def __repr__(self):
        return f'<Book {self.id}>'


class Previous(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)
    Location = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    photo1 = db.Column(db.String)
    photo2 = db.Column(db.String)
    photo3 = db.Column(db.String)
    video = db.Column(db.String)


    def __repr__(self):
        return f'<Previous {self.id}>'


class Testimonials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String,)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    company_name = db.Column(db.String, nullable=False)




class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    Date = db.Column(db.String, default=datetime.date.today().strftime("%B %d, %Y"))


class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    logo = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    message = db.Column(db.String)




with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def admin_required(view_func):
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.access_level != 'admin':
            return redirect(url_for('error'))
        return view_func(*args, **kwargs)
    decorated_view.__name__ = view_func.__name__
    return decorated_view




@app.route("/")
def home():
    is_logged_in = current_user.is_authenticated

    return render_template("index.html", is_logged_in=is_logged_in, year=current_year)


@app.route("/event")
def event():
    is_logged_in = current_user.is_authenticated
    events = Event.query.all()
    return render_template("event.html", is_logged_in=is_logged_in, events=events, year=current_year)


@app.route("/book/<id>", methods=["GET", "POST"])
def bookid():
    return redirect(url_for('booked'))


@app.route("/youbooked")
def booked():
    is_logged_in = current_user.is_authenticated
    id = current_user.id
    book = Book.query.filter_by(user_id=id)
    return render_template("yourbooked.html", is_logged_in=is_logged_in, books=book, year=current_year)


@app.route("/event/<int:eventid>")
def specficevent(eventid):
    is_logged_in = current_user.is_authenticated
    event = Event.query.filter_by(id=eventid).first()
    return render_template("Specficevent.html", event=event, year=current_year, is_logged_in=is_logged_in)



@app.route("/bookfromlink/<int:id>", methods=["POST", "GET"])
@login_required
def bookfromlink(id):
    if request.method == "POST":
        event = Event.query.filter_by(id=id).first()
        date = request.form.get("eventDate")
        specfic_request = request.form.get("specialRequest")

        new_book = Book(
            user_id=current_user.id,
            event_id=id,
            specfic_request=specfic_request,
            booked_for=date,
            price=event.price
        )



        db.session.add(new_book)
        db.session.commit()

        # key = "Bearer CHASECK_TEST-d0r12ujLpJSs6TuCGYxr4fJ6ME1vZll4"
        # url = "https://api.chapa.co/v1/transaction/initialize"
        # payload = {
        #     "amount": amount,
        #     "currency": "ETB",
        #     "email": email,
        #     "first_name": first_name,
        #     "last_name": last_name,
        #     "phone_number": phone_number,
        #     "tx_ref": "chewatatest-"+str(uuid.uuid4()),
        #     "callback_url": "https://www.google.com",
        #     "return_url": "https://www.google.com/",
        #     "customization": {
        #         "title": "Payment for nt",
        #         "description": "I love online payments"
        #     }
        # }
        # headers = {
        #     'Authorization': key,
        #     'Content-Type': 'application/json'
        # }
        #
        # response = requests.post(url, json=payload, headers=headers)
        # # data = response.text
        # data = response.json()
        #
        # if data["status"] == "success":
        #     return redirect(data["data"]["checkout_url"])
        #
        # else:
        #     return render_template("failure.html")

    else:
        event = Event.query.filter_by(id=id).first()
        return render_template("bookfromlink.html", event=event)

@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    is_logged_in = current_user.is_authenticated

    current_date = datetime.date.today().isoformat()
    allevent = Event.query.all()

    if request.method == "POST":
        date = request.form.get("eventDate")
        specfic_request = request.form.get("specialRequest")
        event_type = request.form.get("selectedevent")
        event = Event.query.filter_by(id=event_type).first()
        if event:
            event_id = event.id
        else:
            flash("Event could not be found")
            return redirect(url_for('book'))

        user_id = current_user.id

        if event_type == " ":
            flash("You did not enter the event type")
            return redirect(url_for('book'))


        if date <= current_date:
            flash("You did not enter a valid date.")
            return redirect(url_for('book'))
        key = "Bearer CHASECK_TEST-d0r12ujLpJSs6TuCGYxr4fJ6ME1vZll4"
        url = "https://api.chapa.co/v1/transaction/initialize"
        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "tx_ref": "chewatatest-" + str(uuid.uuid4()),
            "callback_url": "https://www.google.com",
            "return_url": "https://www.google.com/",
            "customization": {
                "title": "Payment for nt",
                "description": "I love online payments"
            }
        }
        headers = {
            'Authorization': key,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)
        # data = response.text
        data = response.json()

        if data["status"] == "success":
            return redirect(data["data"]["checkout_url"])

        else:
            return render_template("failure.html")

        book = Book(
            user_id=user_id,
            event_id=event_id,
            specfic_request=specfic_request,
            booked_for=date,
            event_type=event_type,

        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('booked'))


    else:
        return render_template("book.html", is_logged_in=is_logged_in, events=allevent, year=current_year)


@app.route("/error")
def error():
    abort(404)



@app.route("/login", methods=["GET", "POST"])
def login():
    is_logged_in = current_user.is_authenticated
    if request.method == "POST":
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("That email does not exist, please try again.")

            return redirect(url_for('login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password, please try again.')

            return redirect(url_for('login'))
        login_user(user)

        if email == "zgetnet24@gmail.com" and check_password_hash(user.password, password):
            admin_user = User.query.filter_by(id=current_user.id).first()
            admin_user.access_level = "admin"
            db.session.commit()

            book = Book.query.all()


            return redirect(url_for('allbooked'))
        else:

            return redirect(url_for('home'))

    return render_template("login.html", year=current_year, is_logged_in=is_logged_in)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    is_logged_in = current_user.is_authenticated
    if request.method == "POST":

        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])
        confirm_password = bleach.clean(request.form['confirm-password'])
        first_name = bleach.clean(request.form['first_name'])
        last_name = bleach.clean(request.form['last_name'])
        phone_number = bleach.clean(request.form['phone_number'])

        if confirm_password != password:
            flash("yout confirmation password does not match the password")
            return redirect(url_for('signup'))

        if User.query.filter_by(email=request.form.get('email')).first() is not None:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        if not email or not password or not first_name or not last_name or not phone_number:
            flash("Please fill in all the required fields.")
            return redirect(url_for('signup'))

        if len(password) < 5:
            flash("Password should be at least 5 characters long.")
            return redirect(url_for('signup'))

        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        user = User(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=hash_and_salted_password
        )

        db.session.add(user)
        db.session.commit()


        login_user(user)

        return redirect(url_for("home"))

    return render_template("signup.html", is_logged_in=is_logged_in)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = bleach.clean(request.form["name"])
        email = bleach.clean(request.form["email"])
        phone = bleach.clean(request.form["phone"])
        message = bleach.clean(request.form["message"])
        new_message = Message(
            name=name,
            phone=phone,
            email=email,
            message=message,
        )

        db.session.add(new_message)
        db.session.commit()
        flash("your message has been recieved")
        return redirect(url_for('contact'))

    else:
        is_logged_in = current_user.is_authenticated
        return render_template("contact.html", is_logged_in=is_logged_in, year=current_year)


@app.route("/about", methods=["GET"])
def about():
    is_logged_in = current_user.is_authenticated
    return render_template("about.html", is_logged_in=is_logged_in, year=current_year)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/delete/<int:deleteid>', methods=['POST'])
@admin_required
def delete(deleteid):
    booked = Book.query.get(deleteid)
    if booked:
        db.session.delete(booked)
        db.session.commit()
    else:
        abort(404)
    return render_template("allbooked.html")


@app.route('/deleteevent/<int:deleteid>', methods=['POST'])
@admin_required
def deleteevent(deleteid):
    event = Event.query.filter_by(id=deleteid).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for("allevent"))
    else:
        abort(404)


@app.route('/addevent', methods=['GET', 'POST'])
@admin_required
def addevent():

        if request.method == "POST":
            name = request.form.get("eventname")
            price = request.form.get("price")
            description = request.form.get("description")
            detaildescription = request.form.get("detaileddescription")
            price = request.form.get("price")
            image = request.files['image']


            destination_folder = os.path.join('static', 'images')


            image_path = os.path.join(app.root_path, destination_folder, image.filename)
            image.save(image_path)


            relative_path = os.path.relpath(image_path, app.root_path)

            new_event = Event(
                name=name,
                event_description=description,
                price=price,
                detailed_description=detaildescription,
                image=relative_path
            )
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('allevent'))
        else:
            return render_template("addevent.html")

@app.route("/allbooked", methods=["GET", "POST"])
@admin_required
def allbooked():


    book = Book.query.all();
    if request.method == "GET":
        return render_template("allbooked.html", books=book)


@app.route("/allevent", methods=["POST", "GET"])
@admin_required
def allevent():
    is_logged_in = current_user.is_authenticated
    events = Event.query.all()
    return render_template("allevent.html", events=events, is_logged_in=is_logged_in)


@app.route("/deleteaccount", methods=["GET", "POST"])
@login_required
def deleteaccount():
    if request.method == "POST":
        email = current_user.email
        check_user = User.query.filter_by(email=email)
        if email:
            db.session.delete(check_user)
            db.session.commit()

        return render_template("index.html")
    else:
        return render_template("delete.html")

@app.route("/testimonials", methods=["GET", "POST"])
def testimonials():
    is_logged_in = current_user.is_authenticated
    testimonials = Testimonials.query.all()
    return render_template("Testimonial.html", is_logged_in=is_logged_in, testimonials=testimonials)



@app.route("/whatwedid", methods=["GET", "POST"])
def whatwedid():
    is_logged_in = current_user.is_authenticated
    previous = Previous.query.all()
    return render_template("Whatwedid.html", is_logged_in=is_logged_in, previous=previous)
@app.route("/whatwedid/<int:id>", methods=["GET", "POST"])
def whatwedidspecfic(id):
    is_logged_in = current_user.is_authenticated
    previous = Previous.query.filter_by(id=id)
    return render_template("whatwedidspecfic.html", is_logged_in=is_logged_in, previous=previous)

@app.route("/allprevious", methods=["GET", "POST"])
@admin_required
def allprevious():
    previous = Previous.query.all()
    return render_template("allprevious.html", previous=previous)


@app.route("/addprevious", methods=["GET", "POST"])
@admin_required
def addprevious():
    if request.method == "POST":
        prevname = request.form.get("prevname")
        location = request.form.get("Location")
        date = request.form.get("date")
        details = request.form.get("details")
        description = request.form.get("description")
        video = request.form.get("video")
        image = request.files['image']
        image1 = request.files['image1']
        image2 = request.files['image2']

        destination_folder = os.path.join('static', 'images')

        if image:
            image_path = os.path.join(app.root_path, destination_folder, image.filename)
            image.save(image_path)
            relative_path = os.path.relpath(image_path, app.root_path)
        else:
            relative_path = "null"

        if image1:
                image_path1 = os.path.join(app.root_path, destination_folder, image1.filename)
                image1.save(image_path1)
                relative_path1 = os.path.relpath(image_path1, app.root_path)
        else:
            relative_path1 = "null"
        if image2:
                image_path2 = os.path.join(app.root_path, destination_folder, image2.filename)
                image2.save(image_path2)
                relative_path2 = os.path.relpath(image_path2, app.root_path)
        else:
            relative_path2 = "null"





        previous = Previous(
            name=prevname,
            description= description,
            details=details,
            Location=location,
            date=date,
            photo1=relative_path,
            photo2=relative_path1,
            photo3=relative_path2,
            video=video,

        )
        db.session.add(previous)
        db.session.commit()
        return redirect(url_for("allprevious"))



    return render_template("addprevious.html")


@app.route("/alltestimonials", methods=["GET", "POST"])
@admin_required
def alltestimonials():
    testimonials = Testimonials.query.all()
    return render_template("alltestimonials.html", testimonials=testimonials)



@app.route("/addtestimonials", methods=["GET", "POST"])
@admin_required
def addtestimonials():
    if request.method == "POST":
        image = request.files['userimage']
        if image:


            destination_folder = os.path.join('static', 'images')

            image_path = os.path.join(app.root_path, destination_folder, image.filename)
            image.save(image_path)

            relative_path = os.path.relpath(image_path, app.root_path)
        else:
            relative_path = "../src/images/noprofile.jpg"

        testimonial=Testimonials(

                fname = request.form.get("fname"),
                lname = request.form.get("lname"),
                comment = request.form.get("comment"),
                position = request.form.get("position"),
                company_name = request.form.get("company"),
                photo = relative_path,

           )
        db.session.add(testimonial)
        db.session.commit()
        return redirect(url_for('alltestimonials'))

    else:
        return render_template("addtestimonial.html")


@app.route("/deletetestimonial/<int:id>", methods=["POST", "GET"])
@admin_required
def deletetestimonials(id):
    if request.method == "POST":
        testimonial = Testimonials.query.filter_by(id=id).first()
        db.session.delete(testimonial)
        db.session.commit()
        return redirect(url_for('alltestimonials'))



@app.route("/deleteprevious/<int:id>", methods=["GET", "POST"])
@admin_required
def deleteprevious(id):
    previous =Previous.query.filter_by(id=id).first()
    if previous:
        db.session.delete(previous)
        db.session.commit()
        return redirect(url_for('allprevious'))


@app.route("/newblog", methods=['GET', "POST"])
@admin_required
def newblog():
    if request.method == "POST":
        new_blog = Blog(
            title=request.form.get("title"),
            content= request.form.get("body"),
            subtitle= request.form.get("subtitle"),
            author = request.form.get("author"),
        )
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for("allblog"))
    else:


        return render_template("newblog.html")

@app.route("/editblog/<int:id>", methods=["GET", "POST"])
@admin_required
def editblog(id):
    if request.method == "POST":
        title = bleach.clean(request.form['title'])
        subititle = bleach.clean(request.form['subtitle'])
        content = bleach.clean(request.form["content"])
        blog = Blog.query.filter_by(id=id).first()
        blog.title = title
        blog.subtitle = subititle
        blog.content = content
        db.session.commit()
        return redirect(url_for('allblog'))

    else:
        blog = Blog.query.filter_by(id=id).first()
        return render_template("editblog.html", blog=blog)







@app.route("/deleteblog/<int:id>", methods=["GET", "POST"])
@admin_required
def deleteblog(id):
    delete_blog =Blog.query.filter_by(id=id).first()
    db.session.delete(delete_blog)
    db.session.commit()
    return redirect(url_for('allblog'))

@app.route("/allblog", methods=['GET', "POST"])
def allblog():
    blogs = Blog.query.all()
    return render_template("allblog.html", blogs=blogs)


@app.route("/partners", methods=["GET"])
def partners():

    partners = Partners.query.all()
    return render_template("partners.html", partners=partners)



@app.route("/deletepartner/<int:id>", methods=["GET", "POST"])
@admin_required
def deletepartner(id):
    partner = Partners.query.filter_by(id=id).first()
    db.session.delete(partner)
    db.session.commit()
    return redirect(url_for(allpartners))


@app.route("/allpartners", methods=["GET"])
@admin_required
def allpartners():
    is_logged_in = current_user.is_authenticated
    allpartners = Partners.query.all()
    return render_template("allpartners.html", allpartners=allpartners, is_logged_in=is_logged_in)


@app.route("/addpartner", methods=["GET","POST" ])
@admin_required
def addpartner():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        image = request.files['image']

        destination_folder = os.path.join('static', 'images')

        if image:
            image_path = os.path.join(app.root_path, destination_folder, image.filename)
            image.save(image_path)
            relative_path = os.path.relpath(image_path, app.root_path)
        else:
            relative_path = "null"
        new_partner = Partners(
            name=name,
            description=description,
            logo=image,
        )
        db.session.add(new_partner)
        db.session.commit()
        return redirect(url_for(allpartners))

    else:
        return render_template("addpartner.html")

@app.route("/fetchprice/<int:id>", methods=["POST"])
def fetchprice(id):
    user_id = current_user.id
    event = Event.query.filter_by(id=id).first()
    print(event.price)
    if event:

        response = {"message": "Price fetched successfully", "data": event.price}
        return jsonify(response), 200
    else:
        response = {"message": "Event not found"}
        return jsonify(response), 404


@app.route("/allmessages", methods=["GET"])
@login_required
def messages():
    all_messages =Message.query.order_by(id).desc();
    return render_template("allmessages.html", all_messages=all_messages)

@app.route("/onload", methods=["GET"])
def onpageload():
    return render_template("onpageload.html")

@app.route("/blog", methods=["GET", "POST"])
def blog():
    is_logged_in = current_user.is_authenticated

    page = request.args.get("page", default=1, type=int)
    per_page = 10
    offset = (page - 1) * per_page


    blogs = Blog.query.order_by(Blog.id.desc()).offset(offset).limit(per_page).all()


    total_records = Blog.query.count()


    total_pages = (total_records // per_page) + (1 if total_records % per_page > 0 else 0)

    return render_template("blog-template.html", blogs=blogs,page=page,total_pages=total_pages, is_logged_in=is_logged_in)



@app.route("/blog/<int:id>", methods=['GET', "POST"])
def specficblog(id):
    blog = Blog.query.filter_by(id=id).first()

    return render_template("post-page.html", blog=blog)

@app.route("/sucess", methods=["GET"])
def sucess():
    return render_template("sucess.html")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
   