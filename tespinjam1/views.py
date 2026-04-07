from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.shortcuts import render
from .firebase_config import db , auth
from .firebase_auth import get_token
from .sheet_firebase_sync import sync_sheet_to_firebase
from django.views.decorators.http import require_POST
from .sheets_client import get_sheet_rows, update_datein, delete_sheet_row, normalize_date
import csv


def write_data(request):
    token = get_token(request)
    if request.method == "POST":
        name = request.POST.get("name")
        item = request.POST.get("item")
        keperluan = request.POST.get("keperluan")
        dateout = request.POST.get("dateout")
        datein = request.POST.get("datein")
        

        db.child("products").push({
            "name": name,
            "item": item,
            "keperluan": keperluan,
            "dateout":   dateout,
            "datein": datein,
        }, token)
    return redirect ("index")

def read_data(request):
    token = get_token(request)
    products = db.child("products").get(token)         
    data = products.val() if products.each() else {}
    return render(request, "products.html", {"products": data})

def index(request):
    rows = get_sheet_rows()

    for i, row in enumerate(rows, start=2):
        row["sheet_row"] = i 
        
        row["date_in"] = normalize_date(row.get("date_in")) or ""   # IMPORTANT
        row["status"] = "Returned" if row["date_in"] else "Borrowed"

    return render(request, "index.html", {"rows": rows})
    
def edit_datein(request, sheet_row):
    if request.method == "POST":
        datein = request.POST.get("datein")
        update_datein(sheet_row, datein)

    return redirect("index")
    
def delete_user(request, product_id):
    token = get_token(request)
    if request.method == "POST":
        db.child("products").child(product_id).remove(token)

    return redirect("index")

"""
def update_datein(request, product_id):
    token = get_token(request)
    if request.method == "POST":
        datein = request.POST.get("datein")

        if datein:
            db.child("products").child(product_id).update({
                "datein": datein
            }, token)

    return redirect("index")
"""

@require_POST
def update_datein_view(request):
    sheet_row = int(request.POST["sheet_row"])
    date_in = request.POST["date_in"]  # may be empty

    update_datein(sheet_row, date_in)

    return redirect("index")

@require_POST
def sync_forms_view(request):
    sync_sheet_to_firebase()
    return redirect("index")

def product_list(request):
    rows = get_sheet_rows()
    return render(request, "products.html", {"rows": rows})

@require_POST
def delete_entry(request):
    sheet_row = int(request.POST["sheet_row"])
    delete_sheet_row(sheet_row)
    return redirect("index")

def download_csv(request):
    rows = get_sheet_rows()

    # Create HTTP response with CSV headers
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data_pinjam.csv"'

    writer = csv.writer(response)

    if not rows:
        return response

    # CSV header (keys from first row)
    headers = [key for key in rows[0].keys() if key != "row"]
    writer.writerow(headers)

    # CSV rows
    for row in rows:
        writer.writerow([row.get(h, "") for h in headers])

    return response

# Create your views here.

