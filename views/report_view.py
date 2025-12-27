import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.report import ReportModel
from utils.report_utils import ReportGenerator
from utils.helpers import format_rupiah
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.report_model = ReportModel()
        self.generator = ReportGenerator()
        
        # Tabs for "Laporan Bulanan" and "Analytics"
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_report = self.tabview.add("Laporan Bulanan")
        self.tab_analytics = self.tabview.add("Analytics Dashboard")
        
        self.create_report_tab()
        self.create_analytics_tab()

    def create_report_tab(self):
        # Filter Frame
        frame_filter = ctk.CTkFrame(self.tab_report)
        frame_filter.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame_filter, text="Bulan:").pack(side="left", padx=5)
        self.combo_month = ctk.CTkComboBox(frame_filter, values=[str(i) for i in range(1, 13)], width=60)
        self.combo_month.set(str(datetime.now().month))
        self.combo_month.pack(side="left", padx=5)
        
        ctk.CTkLabel(frame_filter, text="Tahun:").pack(side="left", padx=5)
        self.combo_year = ctk.CTkComboBox(frame_filter, values=[str(i) for i in range(2023, 2030)], width=80)
        self.combo_year.set(str(datetime.now().year))
        self.combo_year.pack(side="left", padx=5)
        
        ctk.CTkButton(frame_filter, text="Tampilkan", command=self.load_report_data, width=100).pack(side="left", padx=20)
        
        ctk.CTkButton(frame_filter, text="Export Excel", command=self.export_excel, fg_color="#4CAF50").pack(side="right", padx=5)
        ctk.CTkButton(frame_filter, text="Export PDF", command=self.export_pdf, fg_color="#FF5722").pack(side="right", padx=5)
        
        # Summary
        frame_summary = ctk.CTkFrame(self.tab_report, fg_color="transparent")
        frame_summary.pack(pady=10)
        
        self.lbl_revenue = ctk.CTkLabel(frame_summary, text="Omzet: Rp 0", font=("Roboto Medium", 16))
        self.lbl_revenue.pack(side="left", padx=20)
        
        self.lbl_profit = ctk.CTkLabel(frame_summary, text="Profit: Rp 0", font=("Roboto Medium", 16), text_color="#4CAF50")
        self.lbl_profit.pack(side="left", padx=20)
        
        # Table
        frame_table = ctk.CTkFrame(self.tab_report)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)
        
        cols = ('id', 'date', 'cashier', 'total', 'profit')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('date', text='Tanggal')
        self.tree.heading('cashier', text='Kasir')
        self.tree.heading('total', text='Omzet')
        self.tree.heading('profit', text='Profit')
        
        self.tree.column('id', width=40)
        self.tree.column('date', width=120)
        self.tree.column('cashier', width=80)
        self.tree.column('total', width=100)
        self.tree.column('profit', width=100)
        self.tree.pack(fill="both", expand=True)
        
        self.current_report_data = []

    def create_analytics_tab(self):
        # 2 Charts: Sales Trend (Bar) and Top Products (Pie)
        
        # Frame for charts
        frame_charts = ctk.CTkFrame(self.tab_analytics, fg_color="transparent")
        frame_charts.pack(fill="both", expand=True)
        
        self.frame_chart1 = ctk.CTkFrame(frame_charts)
        self.frame_chart1.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        self.frame_chart2 = ctk.CTkFrame(frame_charts)
        self.frame_chart2.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkButton(self.tab_analytics, text="Refresh Charts", command=self.load_analytics).pack(pady=10)
        
        # Initial Load
        self.after(500, self.load_analytics)

    def load_report_data(self):
        m = int(self.combo_month.get())
        y = int(self.combo_year.get())
        
        # 1. Get Transactions
        self.report_model.db.connect()
        cursor = self.report_model.db.conn.cursor()
        
        start_date = f"{y}-{m:02d}-01"
        if m == 12: end_date = f"{y+1}-01-01"
        else: end_date = f"{y}-{m+1:02d}-01"
            
        cursor.execute("SELECT * FROM transactions WHERE date >= ? AND date < ? AND status = 'SUCCESS'", (start_date, end_date))
        transactions = [dict(row) for row in cursor.fetchall()]
        
        total_revenue = 0
        total_cost = 0
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for t in transactions:
            # Calculate cost for this transaction
            cursor.execute("SELECT SUM(cost_at_sale * quantity) FROM transaction_items WHERE transaction_id = ?", (t['id'],))
            res = cursor.fetchone()[0]
            cost = res if res else 0
            
            revenue = t['final_total']
            profit = revenue - cost
            
            total_revenue += revenue
            total_cost += cost
            
            self.tree.insert('', tk.END, values=(
                t['id'], t['date'], t['cashier_name'],
                format_rupiah(revenue),
                format_rupiah(profit)
            ))
            
        self.report_model.db.close()
        
        total_profit = total_revenue - total_cost
        
        self.lbl_revenue.configure(text=f"Omzet: {format_rupiah(total_revenue)}")
        self.lbl_profit.configure(text=f"Profit: {format_rupiah(total_profit)}")
        
        self.current_report_data = transactions

    def load_analytics(self):
        # Dummy logic for chart data fetching (Direct DB query instead of model mostly for simplicity here)
        
        # Clear old charts
        for widget in self.frame_chart1.winfo_children(): widget.destroy()
        for widget in self.frame_chart2.winfo_children(): widget.destroy()

        # --- Chart 1: Sales Trend ---
        dates = []
        revenues = []
        for i in range(6, -1, -1):
            d = datetime.now() - timedelta(days=i)
            d_str = d.strftime("%Y-%m-%d")
            _, total = self.report_model.get_daily_sales(d_str)
            dates.append(d.strftime("%d/%m"))
            revenues.append(total)

        fig1, ax1 = plt.subplots(figsize=(5, 4), dpi=100)
        ax1.bar(dates, revenues, color='#4CAF50')
        ax1.set_title("Penjualan 7 Hari Terakhir")
        ax1.set_ylabel("Rupiah")
        
        canvas1 = FigureCanvasTkAgg(fig1, master=self.frame_chart1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        # --- Chart 2: Top Products ---
        self.report_model.db.connect()
        curr = self.report_model.db.conn.cursor()
        curr.execute("SELECT product_name, SUM(quantity) as qty FROM transaction_items GROUP BY product_name ORDER BY qty DESC LIMIT 5")
        rows = curr.fetchall()
        self.report_model.db.close()
        
        if rows:
            labels = [r[0] for r in rows]
            sizes = [r[1] for r in rows]
            
            fig2, ax2 = plt.subplots(figsize=(5, 4), dpi=100)
            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            ax2.set_title("Top 5 Produk Terlaris")
            
            canvas2 = FigureCanvasTkAgg(fig2, master=self.frame_chart2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True)
        else:
             ctk.CTkLabel(self.frame_chart2, text="Belum ada data penjualan").pack(pady=20)

    def export_pdf(self):
        if not self.current_report_data: return
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not filename: return
        m = self.combo_month.get()
        y = self.combo_year.get()
        total_revenue = sum(t['final_total'] for t in self.current_report_data)
        success, msg = self.generator.export_pdf(self.current_report_data, total_revenue, f"{m}/{y}", filename)
        if success: messagebox.showinfo("Success", f"PDF Saved: {msg}")
        else: messagebox.showerror("Error", str(msg))

    def export_excel(self):
        if not self.current_report_data: return
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not filename: return
        success, msg = self.generator.export_excel(self.current_report_data, filename)
        if success: messagebox.showinfo("Success", f"Excel Saved: {msg}")
        else: messagebox.showerror("Error", str(msg))
