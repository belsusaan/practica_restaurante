import os, requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "frontend_secret_key"
API = os.getenv("API_BASE_URL", "http://localhost:8000")


def auth_headers():
    token = session.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "full_name": request.form.get("full_name"),
        }
        resp = requests.post(f"{API}/auth/register", json=data)
        if resp.status_code == 201:
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        else:
            flash(resp.json().get("detail", "Registration failed"), "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
        }
        resp = requests.post(f"{API}/auth/login", json=data)
        if resp.status_code == 200:
            res_json = resp.json()
            session["token"] = res_json.get("access_token")
            session["username"] = request.form.get("username")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.get(f"{API}/orders/mine", headers=auth_headers())
    orders = resp.json() if resp.status_code == 200 else []
    return render_template("dashboard.html", orders=orders)


@app.route("/menu")
def menu():
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.get(f"{API}/menu/all", headers=auth_headers())
    items = resp.json() if resp.status_code == 200 else []
    return render_template("menu.html", items=items)


@app.route("/menu/add", methods=["GET", "POST"])
def menu_add():
    if "token" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "price": float(request.form.get("price")),
            "category": request.form.get("category"),
        }
        resp = requests.post(f"{API}/menu/", json=data, headers=auth_headers())
        if resp.status_code == 201:
            flash("Item added successfully!", "success")
            return redirect(url_for("menu"))
        else:
            flash(resp.json().get("detail", "Error adding item"), "error")
    return render_template("add_menu_item.html")


@app.route("/menu/<int:item_id>/toggle", methods=["POST"])
def menu_toggle(item_id):
    if "token" not in session:
        return redirect(url_for("login"))
    requests.patch(f"{API}/menu/{item_id}/toggle", headers=auth_headers())
    return redirect(url_for("menu"))


@app.route("/orders")
def orders():
    if "token" not in session:
        return redirect(url_for("login"))
    resp = requests.get(f"{API}/orders/", headers=auth_headers())
    all_orders = resp.json() if resp.status_code == 200 else []
    return render_template("orders.html", orders=all_orders)


@app.route("/orders/new", methods=["GET", "POST"])
def order_new():
    if "token" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        items_raw = request.form.getlist("menu_item_id")
        quantities_raw = request.form.getlist("quantity")
        items = []
        for mid, qty in zip(items_raw, quantities_raw):
            if qty and int(qty) > 0:
                items.append({"menu_item_id": int(mid), "quantity": int(qty)})

        payload = {
            "table_number": int(request.form.get("table_number")),
            "notes": request.form.get("notes"),
            "items": items,
        }
        resp = requests.post(f"{API}/orders/", json=payload, headers=auth_headers())
        if resp.status_code == 201:
            flash("Order placed successfully!", "success")
            return redirect(url_for("dashboard"))
        elif resp.status_code == 422:
            flash("Some items are unavailable or missing", "error")
        else:
            flash("Error placing order", "error")

    resp_menu = requests.get(f"{API}/menu/", headers=auth_headers())
    available_items = resp_menu.json() if resp_menu.status_code == 200 else []
    return render_template("new_order.html", items=available_items)


@app.route("/orders/<int:order_id>/status", methods=["POST"])
def order_status(order_id):
    if "token" not in session:
        return redirect(url_for("login"))
    new_status = request.form.get("status")
    resp = requests.patch(
        f"{API}/orders/{order_id}/status",
        json={"status": new_status},
        headers=auth_headers(),
    )
    if resp.status_code == 422:
        flash("Invalid status transition", "error")
    return redirect(url_for("orders"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
