# utils.py
import datetime
from django.db.models import Sum
from .models import Assest

# def detect_anomalies(assets):
#     anomalies = []
#     for asset in assets:
#         if asset.usage_hours > 200:  # Example threshold
#             anomalies.append({
#                 'asset_id': asset.id,
#                 'reason': 'High usage hours'
#             })
#     return anomalies

from datetime import date

def detect_anomalies(assets):
    anomalies = []
    for asset in assets:
        usage_days = (asset.rdt - asset.gdt).days
        if usage_days > 365:  # example condition
            anomalies.append(asset)
    return anomalies


def calculate_depreciation(asset):
    age_in_years = (datetime.date.today() - asset.purchase_date).days / 365
    depreciation_rate = 0.1  # 10% per year
    return asset.initial_value * (depreciation_rate * age_in_years)

def generate_report():
    from reportlab.pdfgen import canvas
    file_path = "asset_report.pdf"
    c = canvas.Canvas(file_path)
    c.drawString(100, 800, "Asset Management Report")
    total_assets = Assest.objects.count()
    total_value = Assest.objects.aggregate(Sum('initial_value'))['initial_value__sum']
    c.drawString(100, 780, f"Total Assets: {total_assets}")
    c.drawString(100, 760, f"Total Value: {total_value}")
    c.showPage()
    c.save()
    return file_path
