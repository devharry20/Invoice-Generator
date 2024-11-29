import os
from datetime import datetime

from flask import Flask, render_template, request, send_file, redirect, url_for

from invoice import Invoice

app = Flask(__name__, template_folder=os.getcwd() + r"\static\templates")
FILE_NAME = "output.pdf"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/customise", methods=["GET", "POST"])
def customise():
    return render_template("customise.html")

@app.route("/generate-invoice", methods=["POST"])
def generate_invoice():
    company_name = request.form.get("company_name")
    company_address = request.form.get("company_address")
    company_city = request.form.get("company_city")
    company_postcode = request.form.get("company_postcode")
    company_country = request.form.get("company_country")
    client_name = request.form.get("client_name")
    client_address = request.form.get("client_address")
    client_city = request.form.get("client_city")
    client_postcode = request.form.get("client_postcode")
    client_country = request.form.get("client_country")
    invoice_date = datetime.strptime(request.form.get("invoice_date"), "%Y-%m-%dT%H:%M")
    invoice_reference = request.form.get("invoice_ref")
    invoice_number = request.form.get("invoice_num")
    descriptions = request.form.getlist('description[]')
    quantities = request.form.getlist('quantity[]')
    unit_prices = request.form.getlist('unit_price[]')
    items = [[descriptions[i], float(quantities[i]), float(unit_prices[i])] for i in range(len(descriptions))]
    invoice = Invoice(
        company_addr_name=company_name,
        company_addr_addr=company_address,
        company_addr_city=company_city,
        company_addr_postal=company_postcode,
        company_addr_country=company_country,
        client_addr_name=client_name,
        client_addr_addr=client_address,
        client_addr_city=client_city,
        client_addr_postal=client_postcode,
        client_addr_country=client_country,
        invoice_date=invoice_date,
        invoice_ref=invoice_reference,
        invoice_num=invoice_number,
        items=items
    )

    invoice.create(
        filename=FILE_NAME,
        image_path=os.getcwd() + r"\static\images\logo.png",
        image_size=(150, 51)   
    )

    return render_template("generate-invoice.html")

@app.route("/file")
def file():
    return send_file(FILE_NAME, as_attachment=True)

@app.route("/after_download")
def after_download():
    return redirect(url_for('index'))

app.run()