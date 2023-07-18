from flask import Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo 
import bcrypt



app = Flask(__name__)
#database
app.config["MONGO_URI"] = "mongodb+srv://smitranpariya30:gw1u2rpX8s3nvLn7@mycloudbss2023.zajjr9o.mongodb.net/mycloudbss2023"
mongo = PyMongo(app) 
app.secret_key = "testing" 



@app.route("/")
def login():
    return render_template("login_page.html")

@app.route("/signup")
def signup():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return render_template("signup_page.html")

@app.route("/ret_login")
def ret_login():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return render_template("login_page.html")

@app.route("/dologin", methods=['POST','GET'])
def doLogin():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        db = mongo.db

        email = request.form.get("email")
        password = request.form.get("password")
        email_found = db.admins.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('dashboard'))
            else:
                if "email" in session:
                    return redirect(url_for("dashboard"))
                message = 'Wrong password'
                return render_template("login_page.html", message=message)
        else:
            message = 'Email not found'
            return render_template("login_page.html", message=message)

@app.route("/forget_password")
def forget_password():
    return render_template("FORGET PASSWORD.html")


@app.route("/dashboard")
def dashboard():
    if "email" in session:
        db = mongo.db
        user = db.admins.find_one({"email":session['email']})
        return render_template("index.html",user=user)
    else:
        return redirect(url_for("dologin"))
    
 
@app.route("/signup", methods=['POST','GET'])
def dosignup():  
    from subpackages.models import do_signup
    do_signup = do_signup()
    return do_signup
        
@app.route('/logout')
def logout():
	session.pop('email',None)
	return redirect('/ret_login')

@app.route('/dashboard/wifi_customer', methods=['POST','GET'])
def wifi_customer():
    db = mongo.db
    user = db.admins.find_one({"email":session['email']})    

    if request.method == 'POST':
        db=mongo.db
        doc_number = request.form.get("doc_number")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        sim_card = request.form.get("sim_card")
        offer_id = request.form.get("offer_id")
        em_ail =  request.form.get("_email")
        date_of_birth = request.form.get("date_of_birth")
        mobile_No = request.form.get("mobile_No")
        landmark = request.form.get("landmark")
        pass_word = request.form.get("_password")
        confirm_password = request.form.get("_confirmpassword")
        adress = request.form.get("adress")
        pincode = request.form.get("pincode")
        state = request.form.get("state")
        status= request.form.get("status")

        hashed = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt())
        if pass_word != confirm_password:
            message1 = "password shouldn't match"
            return message1
        else:
            form_input = {"doc_number":doc_number,
                           "first_name":first_name,
                           "last_name":last_name,
                           "sim_card":sim_card,
                           "offer_id":offer_id, 
                           "_email":em_ail,
                           "date_of_birth":date_of_birth,
                           "mobile_No":mobile_No,
                           "landmark":landmark,
                           "_password":hashed,
                           "adress":adress,
                           "pincode":pincode,
                           "state":state,
                           "status":status}
            db.wifi_customer.insert_one(form_input)
            return render_template("wifi_customer.html",user=user)
    else:
        return render_template("wifi_customer.html",user=user)
    
@app.route('/dashboard/lte_customer', methods=['POST','GET'])
def lte_customer():
    db = mongo.db
    user = db.admins.find_one({"email":session['email']})    

    if request.method == 'POST':
        db=mongo.db
        doc_number = request.form.get("doc_number")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        sim_card = request.form.get("sim_card")
        offer_id = request.form.get("offer_id")
        em_ail =  request.form.get("_email")
        date_of_birth = request.form.get("date_of_birth")
        mobile_No = request.form.get("mobile_No")
        landmark = request.form.get("landmark")
        pass_word = request.form.get("_password")
        confirm_password = request.form.get("_confirmpassword")
        adress = request.form.get("adress")
        pincode = request.form.get("pincode")
        state = request.form.get("state")
        status= request.form.get("status")

        hashed = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt())
        if pass_word != confirm_password:
            message1 = "password shouldn't match"
            return message1
        else:
            form_input = {"doc_number":doc_number,
                           "first_name":first_name,
                           "last_name":last_name,
                           "sim_card":sim_card,
                           "offer_id":offer_id, 
                           "_email":em_ail,
                           "date_of_birth":date_of_birth,
                           "mobile_No":mobile_No,
                           "landmark":landmark,
                           "_password":hashed,
                           "adress":adress,
                           "pincode":pincode,
                           "state":state,
                           "status":status}
            db.lte_customer.insert_one(form_input)
            return render_template("lte_customer.html",user=user)
    else:
        return render_template("lte_customer.html",user=user)
                 
@app.route('/dashboard/settings')
def settings():
    db=mongo.db
    user = db.admins.find_one({"email":session['email']})
    return render_template('settings.html',user=user)

@app.route('/dashboard/internet')
def internet():
    db=mongo.db
    user = db.admins.find_one({"email":session['email']})
    return render_template('internet.html',user=user)

@app.route('/dashboard/product_offering')
def product_offering():
    db=mongo.db
    user = db.admins.find_one({"email":session['email']})
    return render_template('productoffering.html',user=user)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True) 
