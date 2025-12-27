import customtkinter as ctk
from utils.helpers import format_rupiah

class CustomerDisplay(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Customer Display")
        self.geometry("800x600")
        
        self.create_widgets()

    def create_widgets(self):
        # Split into Left (Cart) and Right (Total)
        self.grid_columnconfigure(0, weight=3) # Cart
        self.grid_columnconfigure(1, weight=2) # Total
        self.grid_rowconfigure(0, weight=1)

        # -- Left: Item List --
        self.frame_cart = ctk.CTkFrame(self)
        self.frame_cart.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.frame_cart, text="Daftar Belanja", font=("Roboto", 20)).pack(pady=10)
        
        self.scroll_cart = ctk.CTkScrollableFrame(self.frame_cart)
        self.scroll_cart.pack(fill="both", expand=True, padx=5, pady=5)
        
        # -- Right: Total --
        self.frame_total = ctk.CTkFrame(self, fg_color="#1a1a1a") # Darker
        self.frame_total.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.frame_total, text="Total Belanja", font=("Roboto", 24), text_color="gray").pack(pady=(100, 10))
        self.lbl_total = ctk.CTkLabel(self.frame_total, text="Rp 0", font=("Roboto", 64, "bold"), text_color="#4CAF50")
        self.lbl_total.pack(pady=10)
        
        self.lbl_change_title = ctk.CTkLabel(self.frame_total, text="Kembalian", font=("Roboto", 20), text_color="gray")
        self.lbl_change_title.pack(pady=(50, 10))
        self.lbl_change = ctk.CTkLabel(self.frame_total, text="-", font=("Roboto", 48, "bold"), text_color="#2196F3")
        self.lbl_change.pack(pady=10)

        # Promo info
        self.lbl_promo = ctk.CTkLabel(self.frame_total, text="", font=("Roboto", 16), text_color="#E91E63")
        self.lbl_promo.pack(side="bottom", pady=20)

    def update_data(self, cart, total, change=0, promo_text=""):
        # Clear cart list
        for widget in self.scroll_cart.winfo_children():
            widget.destroy()
            
        # Repopulate
        for item in cart:
            row = ctk.CTkFrame(self.scroll_cart, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=item['name'], font=("Roboto", 16)).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"{item['qty']} x {format_rupiah(item['price'])}", font=("Roboto", 14), text_color="gray").pack(side="right", padx=10)
        
        # Update Total
        self.lbl_total.configure(text=format_rupiah(total))
        
        # Update Change
        if change > 0:
            self.lbl_change.configure(text=format_rupiah(change))
        else:
            self.lbl_change.configure(text="-")
            
        # Update Promo
        self.lbl_promo.configure(text=promo_text)
