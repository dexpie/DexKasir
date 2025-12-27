from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime
from utils.helpers import format_rupiah

class ReportGenerator:
    def export_pdf(self, transactions, total_revenue, period_str, filename="report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Title
        pdf.cell(0, 10, f"Laporan Penjualan - {period_str}", ln=True, align='C')
        pdf.ln(10)
        
        # Highlights
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Total Pendapatan: {format_rupiah(total_revenue)}", ln=True)
        pdf.cell(0, 10, f"Total Transaksi: {len(transactions)}", ln=True)
        pdf.ln(10)
        
        # Table Header
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(30, 10, "ID", 1)
        pdf.cell(50, 10, "Tanggal", 1)
        pdf.cell(40, 10, "Kasir", 1)
        pdf.cell(40, 10, "Total", 1)
        pdf.ln()
        
        # Table Data
        pdf.set_font("Arial", '', 10)
        for t in transactions:
            pdf.cell(30, 10, str(t['id']), 1)
            pdf.cell(50, 10, str(t['date']), 1)
            pdf.cell(40, 10, t['cashier_name'], 1)
            pdf.cell(40, 10, format_rupiah(t['final_total']), 1)
            pdf.ln()
            
        try:
            pdf.output(filename)
            return True, filename
        except Exception as e:
            return False, str(e)

    def export_excel(self, transactions, filename="report.xlsx"):
        try:
            # Prepare data for DataFrame
            data = []
            for t in transactions:
                data.append({
                    'ID Transaksi': t['id'],
                    'Tanggal': t['date'],
                    'Kasir': t['cashier_name'],
                    'Subtotal': t['subtotal'],
                    'Diskon': t['discount'],
                    'Pajak': t['tax'],
                    'Total Final': t['final_total']
                })
            
            df = pd.DataFrame(data)
            
            # Export
            df.to_excel(filename, index=False)
            return True, filename
        except Exception as e:
            return False, str(e)
