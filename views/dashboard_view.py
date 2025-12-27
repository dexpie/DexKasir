import customtkinter as ctk
import tkinter as tk
from views.product_view import ProductView
from views.history_view import HistoryView
from views.transaction_view import TransactionView
from views.report_view import ReportView
from views.settings_view import SettingsView
from views.promo_view import PromoView
from views.overview_view import OverviewView
from views.audit_view import AuditView
from views.opname_view import StockOpnameView

class DashboardView(ctk.CTkToplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.title(f"DexKasir - Dashboard ({user['role'].upper()})")
        self.geometry("1100x700")
        self.user = user
        self.parent = parent
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Grid layout 1x2 (Sidebar, Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_main_area()
        
        # Default view
        if user['role'] == 'admin':
            self.show_view("overview") # Default to home
            self.check_low_stock()
        else:
            self.show_view("cashier")

    def check_low_stock(self):
        # Quick check for low stock items
        from models.product import ProductModel
        pm = ProductModel()
        items = pm.get_all_products()
        low_items = [i for i in items if i['stock'] < 5]
        
        if low_items:
            names = ", ".join([i['name'] for i in low_items[:3]])
            msg = f"Low Stock Warning: {names}"
            if len(low_items) > 3: msg += "..."
            
            # Show a warning label in sidebar or toaster? 
            # Let's put a distinct label in sidebar bottom
            lbl_warn = ctk.CTkLabel(self.sidebar, text=msg, text_color="orange", wraplength=180)
            lbl_warn.pack(side="bottom", pady=10)

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo / Title
        logo = ctk.CTkLabel(self.sidebar, text="DexKasir", font=("Roboto Medium", 20))
        logo.pack(pady=30)
        
        # Buttons
        self.btn_dashboard = self.create_nav_btn("Dashboard", lambda: self.show_view("overview"))
        self.btn_cashier = self.create_nav_btn("Kasir", lambda: self.show_view("cashier"))
        self.btn_report = self.create_nav_btn("Laporan", lambda: self.show_view("report")) # Separate Report btn
        self.btn_products = self.create_nav_btn("Produk", lambda: self.show_view("products"))
        self.btn_history = self.create_nav_btn("Riwayat", lambda: self.show_view("history"))
        self.btn_users = self.create_nav_btn("Users", lambda: self.show_view("users"))
        self.btn_promos = self.create_nav_btn("Promos", lambda: self.show_view("promos"))
        self.btn_opname = self.create_nav_btn("Stock Opname", lambda: self.show_view("opname"))
        self.btn_audit = self.create_nav_btn("Audit Logs", lambda: self.show_view("audit"))
        self.btn_settings = self.create_nav_btn("Pengaturan", lambda: self.show_view("settings"))
        
        # Role based hiding
        if self.user['role'] != 'admin':
            self.btn_dashboard.pack_forget()
            self.btn_products.pack_forget()
            self.btn_users.pack_forget()
            self.btn_promos.pack_forget()
            self.btn_opname.pack_forget()
            self.btn_audit.pack_forget()
            self.btn_settings.pack_forget()
            self.btn_history.pack_forget()

        # Logout at bottom
        btn_logout = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout, fg_color="#d32f2f", hover_color="#b71c1c")
        btn_logout.pack(side="bottom", pady=20, padx=20)

    def create_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w")
        btn.pack(pady=5, padx=20, fill="x")
        return btn

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_view(self, view_name):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        if view_name == "cashier":
            TransactionView(self.main_frame, self.user)
        elif view_name == "products":
            ProductView(self.main_frame)
        elif view_name == "history":
            HistoryView(self.main_frame)
        elif view_name == "report":
            ReportView(self.main_frame) # Contains Dashboard/Charts
        elif view_name == "settings":
            SettingsView(self.main_frame)
        elif view_name == "users":
            UserView(self.main_frame)
        elif view_name == "promos":
            PromoView(self.main_frame)
        elif view_name == "overview":
            OverviewView(self.main_frame)
        elif view_name == "audit":
            AuditView(self.main_frame)
        elif view_name == "opname":
            StockOpnameView(self.main_frame, self.user)

    def logout(self):
        self.destroy()
        self.parent.deiconify()
        self.parent.entry_password.delete(0, tk.END)

    def on_close(self):
        self.parent.destroy()
