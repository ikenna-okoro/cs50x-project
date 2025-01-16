import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, url_for, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from werkzeug.utils import secure_filename

from helpers import apology, login_required, pound, remark

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["pound"] = pound

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///iyk-sandwich.db")

# Configure file upload (adapted for chatgpt)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directory to store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Limit file size to 2MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# adapted from Chatgpt helper function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    """Show landing page with business details"""
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM Customers WHERE name = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["customerID"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        user_name = request.form.get("username")
        if not user_name:
            return apology("must provide username", 400)
        
        # Ensure email was submitted
        email = request.form.get("email")
        if not email:
            return apology("must provide email", 400)
        
        # Ensure address was submitted
        address = request.form.get("address")
        if not address:
            return apology("must provide address", 400)
        
        # Ensure phone number was submitted
        phoneNumber = request.form.get("phoneNumber")
        if not phoneNumber:
            return apology("must provide phone number", 400)
        
        

        # Ensure password was submitted
        pass_word = request.form.get("password")
        if not pass_word:
            return apology("must provide password", 400)

        # Ensure confirm password was submitted
        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return apology("must confirm password", 400)

        # Ensure passords match
        if pass_word != confirm_password:
            return apology("passwords do not match", 400)

        # Check if username exists
        rows = db.execute("SELECT * FROM Customers WHERE name = ?", user_name)
        if len(rows) > 0:
            return apology("Username already exists, Please choose another username.", 400)

        hash_value = generate_password_hash(pass_word)
        db.execute("INSERT INTO Customers (name, email, hash, address, phoneNumber) VALUES (?, ?, ?, ?, ?)",
                   user_name, email, hash_value, address, phoneNumber)

        rows = db.execute("SELECT * FROM Customers WHERE name = ?", user_name)

        # Remember which user has logged in
        session["user_id"] = rows[0]["customerID"]

        flash('You have successfully registered!', 'success')
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/reset_password", methods=["GET", "POST"])
@login_required
def reset_password():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    user = db.execute("SELECT customerID FROM Customers WHERE customerID = ?", user_id)[0]["CustomerID"]
    if not user:
        return redirect("/login")

    if request.method == "POST":
        new_password = request.form["password"]
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE Customers SET hash = ? WHERE customerID = ?", hashed_password, user)
        return redirect("/login")
    return render_template("reset_password.html")


@app.route("/products")
@login_required
def products():
    """Show catalogue of products"""
    if 'user_id' in session:
        id = session["user_id"]
        
        customers = db.execute("SELECT * FROM Customers WHERE customerID= ?", id)

        menu = db.execute("SELECT * FROM MenuItems AS m INNER JOIN Category AS c ON m.catID = c.catID ORDER BY catID;")
        
        cat1 = db.execute("SELECT * FROM Category WHERE catID = 1")
        cat2 = db.execute("SELECT * FROM Category WHERE catID = 2")
        cat3 = db.execute("SELECT * FROM Category WHERE catID = 3")

        return render_template("products.html", menu=menu, customers=customers, cat1=cat1, cat2=cat2, cat3=cat3)

    else:
        return redirect("/login.html")
    


@app.route("/basket", methods=["GET", "POST"])
@login_required
def basket():
    # Ensure the cart exists in the session
    if "basket" not in session:
        session["basket"] = []

    # POST handling
    if request.method == "POST":
        action = request.form.get("action")

        # Adding items to the basket
        if action == "add_to_basket":
            item_id = request.form.get("id")
            if item_id:
                session["basket"].append(item_id)
            return redirect("/products")

        # Processing customer details
        elif action == "customer_details":
            firstname = request.form.get("firstname", "").strip()
            lastname = request.form.get("lastname", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phoneNumber", "").strip()
            address = request.form.get("address", "").strip()
            total_cost = request.form.get("total_cost", "0").strip()

            # Validate required fields
            if not all([firstname, lastname, email, phone, address, total_cost]):
                return "All fields are required for customer details", 400

            # Store customer details in session for payment
            session["customer_details"] = {
                "firstname": firstname.upper(),
                "lastname": lastname.upper(),
                "email": email,
                "phone": phone,
                "address": address.upper(),
                "total_cost": float(total_cost),
            }
            print("Successfully submitted")
            ok = 200
            return "Successfully submitted MY G", ok   # Return success response for AJAX
            

        # Handling payment
        elif action == "payment":
            pay = int(request.form.get("pay", 0))
            if pay != 1:
                return apology("Insufficient funds in your account", 400)

            # Insert transaction into the admin database
            customer = session.get("customer_details", {})
            
            if not customer:
                return apology("Customer details are missing. Please provide them first.", 400)

            id = session["user_id"]
            x = datetime.datetime.now().strftime("%c")
            db.execute(
                """
                INSERT INTO admin (cust_id, firstname, lastname, email, phone_number, address, total_cost, date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                id,
                customer["firstname"],
                customer["lastname"],
                customer["email"],
                customer["phone"],
                customer["address"],
                customer["total_cost"],
                x,
                "Successful",
            )
            flash("Payment Successful!", "success")
            
            # Clear basket and customer details after successful payment (adopted from research at ChatGpt)
            session.pop("basket", None)
            session.pop("customer_details", None)
            return redirect("/products")

    # GET handling (display basket items)
    if session["basket"]:
        # Get unique item IDs from the basket
        unique_item_ids = list(set(session["basket"]))

        # Create placeholders for the query
        placeholders = ",".join("?" for _ in unique_item_ids)
        query = f"SELECT * FROM MenuItems WHERE itemID IN ({placeholders})"

        # Fetch unique items from the database
        basket = db.execute(query, *unique_item_ids)
    else:
        basket = []

    # Calculate the total cost of the items in the basket
    total_cost = sum(item["price"] for item in basket)

    # Reflect the number of unique items in total_items
    return render_template(
        "basket.html",
        basket=basket,
        total_items=len(set(session["basket"])),  # Count unique item IDs
        total_cost=total_cost,
        customer=session.get("customer_details", {}),
    )


        

        

@app.route("/admin/")
@login_required
def admin():
    if request.method == "GET":
        """Show summary of customer orders"""
        id = session.get("user_id")
        if id == 1:
            data = db.execute("SELECT * FROM admin")
            return render_template("admin/index.html", data = data)
        else:
            flash("Sorry you must be the Admin to view this page!")
            return redirect("/")    
        
    else:
        return render_template("/admin/index.html")
    
   
    
@app.route("/admin/items", methods=["GET", "POST"])
@login_required
def menuItems():
    if request.method == "POST":
        # TODO: Add the menu items into the database
        
        catID = request.form.get("catID")
        if not catID:
            return redirect("/admin/items")
        try:
            catID = int(catID)
        except ValueError:
            return redirect("/admin/items")
        if catID < 1 or catID > 3:
            return redirect("/admin/items")

        name = request.form.get("name")
        if not name:
            return redirect("/admin/items")
        description = request.form.get("description")
        if not description:
            return redirect("/admin/items")
        price = request.form.get("price")
        try:
            price = float(price)
        except ValueError:
            return redirect("/admin/items")
        if price < 0:
            return redirect("/admin/items")
        file = request.files['image']
        
         # Validate and save the file (adapted from chatgpt)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)


            db.execute(
            "INSERT INTO MenuItems (catID, name, description, price, image_path) VALUES (?, ?, ?, ?, ?)", catID, name, description, price, filepath)
            flash('Menu item added successfully!', 'success')
        else:
            flash('Invalid file type. Please upload an image file.', 'error')

        return redirect("/admin/items")
  
        
    else:
        data = db.execute("SELECT * FROM MenuItems")
        return render_template("/admin/items.html", data=data)
    

@app.route("/admin/customers", methods=["GET"])
@login_required
def customers():
    data = db.execute("SELECT * FROM Customers")
    return render_template("/admin/customers.html", data=data)
    
      


@app.route("/removeItem", methods=["POST"])
@login_required
def removeItem():
    # remove item
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM MenuItems WHERE itemID = ?", id)
    return redirect("/admin/items")


@app.route("/removeCustomer", methods=["POST"])
@login_required
def removeCustomer():
    # remove customer
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Customers WHERE customerID = ?", id)
    return redirect("/admin/customers")


@app.route("/admin/edit", methods=["GET", "POST"])
@login_required
def editItem():
    id = request.form.get("id")
    if id:
        data = db.execute("SELECT * FROM MenuItems WHERE itemID =?", id)

    return render_template("/admin/edit.html", data=data)
    
    

    


@app.route("/update", methods=["POST"])
@login_required
def update():
    id = request.form.get("id")
    catID = request.form.get("catID")
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    # Ensure the request includes an image and an item ID
    if "image" not in request.files or "id" not in request.form:
        flash("Missing file or item ID.", "error")
        return redirect("/admin/items")

    image = request.files["image"]

    if image.filename == "":
        flash("No selected file.", "error")
        return redirect(url_for("/admin/items"))

    if image:
        # Generate a secure filename and save the file
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)

        db.execute("UPDATE MenuItems SET catID = ?, name = ?, description = ?, price = ?, image_path = ? WHERE itemID = ?", catID, name, description, price, image_path, id)
        flash('Menu item updated successfully!', 'success')
    else:
        flash('Invalid file type. Please upload an image file.', 'error')

    return redirect("/admin/items")


@app.context_processor
def inject_total_items():
    total_items = len(set(session.get("basket", [])))  # Count unique items in the basket
    return {"total_items": total_items}


# Make "total_items" available globally for all routes that use the layout so it can be dynamically displayed (adapted from chatgpt).
@app.context_processor
def inject_total_items():
    total_items = len(set(session.get("basket", [])))  # Count unique items in the basket
    return {"total_items": total_items}

