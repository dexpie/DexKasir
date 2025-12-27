import customtkinter as ctk
from models.transaction import TransactionModel
from models.product import ProductModel
from datetime import datetime
from utils.helpers import format_rupiah

class OverviewView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.transaction_model = TransactionModel()
        self.product_model = ProductModel()
        
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Dashboard Overview", font=("Roboto Medium", 24)).pack(anchor="w", pady=20)
        
        # Grid for Cards
        frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        frame_cards.pack(fill="x", pady=10)
        
        # Get Data
        today = datetime.now().strftime("%Y-%m-%d")
        daily_sales = self.get_daily_sales(today)
        txn_count = self.get_txn_count(today)
        low_stock = self.get_low_stock_count()
        
        # Build Cards
        self.create_card(frame_cards, "Omzet Hari Ini", format_rupiah(daily_sales), "#4CAF50", 0)
        self.create_card(frame_cards, "Transaksi Hari Ini", f"{txn_count} Trx", "#2196F3", 1)
        self.create_card(frame_cards, "Stok Menipis", f"{low_stock} Item", "#FF9800", 2)

    def create_card(self, parent, title, value, color, col_idx):
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        card.grid(row=0, column=col_idx, sticky="ew", padx=10, pady=5)
        parent.grid_columnconfigure(col_idx, weight=1)
        
        ctk.CTkLabel(card, text=title, text_color="white", font=("Roboto", 14)).pack(pady=(15,0))
        ctk.CTkLabel(card, text=value, text_color="white", font=("Roboto Medium", 22)).pack(pady=(5,15))

    def get_daily_sales(self, date_str):
        txns = self.transaction_model.get_all_transactions() # Inefficient, but works for prototype
        # Need date filtering logic. Let's do rough filter
        total = 0
        for t in txns:
            if t['date'].startswith(date_str) and t['status'] == 'SUCCESS':
                total += t['final_total']
        return total

    def get_txn_count(self, date_str):
        txns = self.transaction_model.get_all_transactions()
        count = 0
        for t in txns:
            if t['date'].startswith(date_str) and t['status'] == 'SUCCESS':
                count += 1
        return count
        
    def get_low_stock_count(self):
        products = self.product_model.get_all_products()
        return len([p for p in products if p['stock'] < 5])
