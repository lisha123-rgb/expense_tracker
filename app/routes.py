from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Expense, Category
from app import db
from sqlalchemy import func
from datetime import datetime
from app.utils import auto_detect_category 
from flask import abort

main = Blueprint("main", __name__)

# -------------------------
# HOME
# -------------------------
@main.route("/")
def index():
    return render_template("index.html")


# -------------------------
# REGISTER
# -------------------------
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        # Basic validation
        if len(password) < 6:
            flash("Password must be at least 6 characters")
            return redirect(url_for("main.register"))

        # Check duplicate email
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("main.register"))

        # Check duplicate username
        if User.query.filter_by(username=username).first():
            flash("Username already taken")
            return redirect(url_for("main.register"))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("main.login"))

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------
@main.route("/login", methods=["GET", "POST"])
def login():

    # Initialize brute-force protection
    if "login_attempts" not in session:
        session["login_attempts"] = 0

    if session["login_attempts"] >= 5:
        flash("Too many login attempts. Try again later.")
        return redirect(url_for("main.login"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            session["login_attempts"] = 0
            return redirect(url_for("main.dashboard"))

        session["login_attempts"] += 1
        flash("Invalid email or password")
        return redirect(url_for("main.login"))

    return render_template("login.html")


# -------------------------
# DASHBOARD
# -------------------------
@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    # ========================
    # HANDLE ADD EXPENSE
    # ========================
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            description = request.form["description"].strip()
            date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()

            category_id = request.form.get("category_id")
            print("CATEGORY ID FROM FORM:", category_id)


            # ------------------------
            # AUTO DETECT CATEGORY
            # ------------------------
            if not category_id:
                predicted_name = auto_detect_category(description)
                print("AUTO DETECT TRIGGERED")
                print("Predicted:", predicted_name)

                category = Category.query.filter_by(name=predicted_name).first()

                # If predicted category doesn't exist → create it
                if not category:
                    category = Category(name=predicted_name)
                    db.session.add(category)
                    db.session.commit()

                category_id = category.id

            else:
                category_id = int(category_id)

                # Verify category exists
                category = Category.query.get(category_id)
                if not category:
                    flash("Invalid category", "danger")
                    return redirect(url_for("main.dashboard"))

            # ------------------------
            # CREATE EXPENSE
            # ------------------------
            expense = Expense(
                amount=amount,
                description=description,
                date=date,
                category_id=category_id,
                user_id=current_user.id
            )

            db.session.add(expense)
            db.session.commit()
            flash("Expense added successfully", "success")

        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Error adding expense", "danger")

        return redirect(url_for("main.dashboard"))

    # ========================
    # YEAR FILTER
    # ========================
    selected_year = request.args.get("year", type=int)

    years = db.session.query(
        func.extract('year', Expense.date)
    ).filter(
        Expense.user_id == current_user.id
    ).distinct().all()

    years = sorted([int(y[0]) for y in years if y[0]], reverse=True)

    if not selected_year:
        selected_year = datetime.now().year

    # ========================
    # FETCH EXPENSES FOR YEAR
    # ========================
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        func.extract('year', Expense.date) == selected_year
    ).order_by(Expense.date.desc()).all()

    categories = Category.query.all()

    # ========================
    # GROUP BY MONTH
    # ========================
    expenses_by_month = {}

    for expense in expenses:
        month_key = expense.date.strftime("%B")

        if month_key not in expenses_by_month:
            expenses_by_month[month_key] = {
                "items": [],
                "month_total": 0
            }

        expenses_by_month[month_key]["items"].append(expense)
        expenses_by_month[month_key]["month_total"] += float(expense.amount)

    # ========================
    # TOTALS
    # ========================
    yearly_total = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id,
        func.extract('year', Expense.date) == selected_year
    ).scalar() or 0

    overall_total = db.session.query(
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id
    ).scalar() or 0

    return render_template(
        "dashboard.html",
        expenses_by_month=expenses_by_month,
        categories=categories,
        yearly_total=float(yearly_total),
        overall_total=float(overall_total),
        selected_year=selected_year,
        years=years
    )


# -------------------------
# ANALYTICS
# -------------------------
@main.route("/analytics")
@login_required
def analytics():

    now = datetime.now()

    selected_month = request.args.get("month", type=int)
    selected_year = request.args.get("year", type=int)

    if not selected_month:
        selected_month = now.month

    if not selected_year:
        selected_year = now.year

    category_data = (
        db.session.query(
            Category.name,
            func.sum(Expense.amount)
        )
        .join(Expense, Expense.category_id == Category.id)
        .filter(
            Expense.user_id == current_user.id,
            func.extract('month', Expense.date) == selected_month,
            func.extract('year', Expense.date) == selected_year
        )
        .group_by(Category.name)
        .all()
    )

    labels = [row[0] for row in category_data]
    values = [float(row[1]) for row in category_data if row[1]]

    years = (
        db.session.query(func.extract('year', Expense.date))
        .filter(Expense.user_id == current_user.id)
        .distinct()
        .all()
    )

    years = sorted([int(y[0]) for y in years if y[0]], reverse=True)

    return render_template(
        "analytics.html",
        labels=labels,
        values=values,
        selected_month=selected_month,
        selected_year=selected_year,
        years=years
    )


# -------------------------
# LOGOUT
# -------------------------
@main.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("main.index"))


# -------------------------
# DELETE EXPENSE (SECURE)
# -------------------------
@main.route("/delete-expense/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully")
    return redirect(url_for("main.dashboard"))

# -------------------------
# EDIT EXPENSE
# -------------------------
@main.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):

    expense = Expense.query.get_or_404(expense_id)

    # Only owner can edit
    if expense.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        try:
            expense.amount = float(request.form["amount"])
            expense.description = request.form["description"].strip()
            expense.date = datetime.strptime(
                request.form["date"], "%Y-%m-%d"
            ).date()

            category_id = request.form.get("category_id")

            # If category selected manually
            if category_id:
                category = Category.query.get(int(category_id))
                if category:
                    expense.category_id = category.id
                else:
                    flash("Invalid category", "danger")
                    return redirect(url_for("main.dashboard"))

            # If no category → auto detect
            else:
                predicted_name = auto_detect_category(expense.description)

                category = Category.query.filter_by(name=predicted_name).first()

                if not category:
                    category = Category(name=predicted_name)
                    db.session.add(category)
                    db.session.commit()

                expense.category_id = category.id

            db.session.commit()
            flash("Expense updated successfully", "success")

        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Error updating expense", "danger")

        return redirect(url_for("main.dashboard"))

    categories = Category.query.all()

    return render_template(
        "edit_expense.html",
        expense=expense,
        categories=categories
    )
