import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.product import ProductModel
from models.transaction import TransactionModel
from models.settings import SettingsModel
from utils.helpers import format_rupiah
from utils.scanner import BarcodeScanner
from utils.printer import ReceiptPrinter

from models.member import MemberModel

class TransactionView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.user = user
        
        self.product_model = ProductModel()
        self.transaction_model = TransactionModel()
        self.settings_model = SettingsModel()
        self.member_model = MemberModel()
        self.printer = ReceiptPrinter(self.settings_model)
        
        self.cart = []
        self.discount_percent = 0
        self.tax_percent = self.settings_model.get("tax_rate")
        self.current_subtotal = 0
        self.current_member = None # Store member dict if found
        
        self.create_widgets()
        self.refresh_product_list()

    def create_widgets(self):
        # 2 Columns grid
        self.grid_columnconfigure(0, weight=1) # Products
        self.grid_columnconfigure(1, weight=1) # Cart
        self.grid_rowconfigure(0, weight=1)

        # -- Left Panel: Products --
        frame_left = ctk.CTkFrame(self)
        frame_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(frame_left, text="Daftar Produk", font=("Roboto Medium", 16)).pack(pady=10)

        # Search
        frame_search = ctk.CTkFrame(frame_left, fg_color="transparent")
        frame_search.pack(fill="x", padx=10)
        
        self.entry_search = ctk.CTkEntry(frame_search, placeholder_text="Cari Nama / Barcode")
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.entry_search.bind('<Return>', self.handle_barcode_enter)
        self.entry_search.bind('<KeyRelease>', self.filter_products)
        
        btn_scan = ctk.CTkButton(frame_search, text="[o]", width=40, command=self.scan_barcode)
        btn_scan.pack(side="left")

        # Treeview (Products)
        frame_tree = ctk.CTkFrame(frame_left)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        cols = ('id', 'barcode', 'name', 'price', 'stock')
        self.tree_products = ttk.Treeview(frame_tree, columns=cols, show='headings')
        self.tree_products.heading('id', text='ID')
        self.tree_products.heading('barcode', text='Barcode')
        self.tree_products.heading('name', text='Nama')
        self.tree_products.heading('price', text='Harga')
        self.tree_products.heading('stock', text='Stok')
        
        self.tree_products.column('id', width=30)
        self.tree_products.column('barcode', width=80)
        self.tree_products.column('name', width=120)
        self.tree_products.column('price', width=80)
        self.tree_products.column('stock', width=40)
        self.tree_products.pack(fill="both", expand=True)

        ctk.CTkButton(frame_left, text="Tambah ke Keranjang", command=self.add_to_cart).pack(fill="x", padx=10, pady=10)

        # -- Right Panel: Cart --
        frame_right = ctk.CTkFrame(self)
        frame_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Member Section
        frame_member = ctk.CTkFrame(frame_right, fg_color="#333")
        frame_member.pack(fill="x", padx=10, pady=5)
        
        self.entry_member_phone = ctk.CTkEntry(frame_member, placeholder_text="No HP Member", width=150)
        self.entry_member_phone.pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_member, text="Cari", width=50, command=self.search_member).pack(side="left", padx=5)
        ctk.CTkButton(frame_member, text="+Baru", width=50, fg_color="gray", command=self.register_member).pack(side="left")
        
        self.lbl_member_info = ctk.CTkLabel(frame_member, text="Guest", text_color="gray")
        self.lbl_member_info.pack(side="right", padx=10)

        ctk.CTkLabel(frame_right, text="Keranjang Belanja", font=("Roboto Medium", 16)).pack(pady=(5,10))

        # Treeview (Cart)
        frame_cart_list = ctk.CTkFrame(frame_right)
        frame_cart_list.pack(fill="both", expand=True, padx=10)
        
        cols_cart = ('id', 'name', 'price', 'qty', 'subtotal')
        self.tree_cart = ttk.Treeview(frame_cart_list, columns=cols_cart, show='headings')
        self.tree_cart.heading('id', text='ID')
        self.tree_cart.heading('name', text='Nama')
        self.tree_cart.heading('price', text='Harga')
        self.tree_cart.heading('qty', text='Qty')
        self.tree_cart.heading('subtotal', text='Subtotal')
        
        self.tree_cart.column('id', width=40)
        self.tree_cart.column('name', width=120)
        self.tree_cart.column('price', width=80)
        self.tree_cart.column('qty', width=40)
        self.tree_cart.column('subtotal', width=80)
        self.tree_cart.pack(fill="both", expand=True)

        # Controls
        frame_controls = ctk.CTkFrame(frame_right, fg_color="transparent")
        frame_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(frame_controls, text="Hapus Item", command=self.remove_from_cart, fg_color="#f44336", hover_color="#d32f2f").pack(side="left", fill="x", expand=True, padx=(0,5))
        
        # Discount Input
        frame_disc = ctk.CTkFrame(frame_controls, fg_color="transparent")
        frame_disc.pack(side="right")
        self.entry_discount = ctk.CTkEntry(frame_disc, width=50, placeholder_text="%")
        self.entry_discount.insert(0, "0")
        self.entry_discount.pack(side="left", padx=5)
        ctk.CTkButton(frame_disc, text="Set Disc", width=60, command=self.update_totals).pack(side="left")

        # Summary
        frame_summary = ctk.CTkFrame(frame_right, fg_color="transparent")
        frame_summary.pack(fill="x", padx=10, pady=10)
        
        self.lbl_subtotal = ctk.CTkLabel(frame_summary, text="Subtotal: Rp 0")
        self.lbl_subtotal.pack(anchor="e")
        self.lbl_discount = ctk.CTkLabel(frame_summary, text="Diskon: Rp 0", text_color="#f44336")
        self.lbl_discount.pack(anchor="e")
        self.lbl_tax = ctk.CTkLabel(frame_summary, text=f"Pajak ({self.tax_percent}%): Rp 0")
        self.lbl_tax.pack(anchor="e")
        self.lbl_total = ctk.CTkLabel(frame_summary, text="TOTAL: Rp 0", font=("Roboto", 24, "bold"), text_color="#2196F3")
        self.lbl_total.pack(anchor="e", pady=5)

        # Payment
        frame_pay = ctk.CTkFrame(frame_right, fg_color="transparent")
        frame_pay.pack(fill="x", padx=10, pady=10)
        
        self.entry_pay = ctk.CTkEntry(frame_pay, placeholder_text="Jumlah Bayar", font=("Roboto", 16))
        self.entry_pay.pack(fill="x", pady=(0, 5))
        self.entry_pay.bind('<KeyRelease>', self.calculate_change)
        
        self.lbl_change = ctk.CTkLabel(frame_pay, text="Kembalian: Rp 0", font=("Roboto", 14))
        self.lbl_change.pack(anchor="e")

        # Payment Method
        ctk.CTkLabel(frame_pay, text="Metode Pembayaran", font=("Roboto", 12)).pack(anchor="w", pady=(5,0))
        self.seg_payment = ctk.CTkSegmentedButton(frame_pay, values=["CASH", "QRIS", "TRANSFER"])
        self.seg_payment.set("CASH")
        self.seg_payment.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(frame_right, text="PROSES TRANSAKSI", command=self.process_transaction, height=50, font=("Roboto", 14, "bold"), fg_color="#4CAF50", hover_color="#388E3C").pack(fill="x", padx=10, pady=20)

    # ... Reuse logic methods (refresh_product_list, filter, scan, add_to_cart, etc.) ...
    
    def refresh_product_list(self):
        self.products = self.product_model.get_all_products()
        self.update_product_tree(self.products)

    def update_product_tree(self, products):
        for item in self.tree_products.get_children():
            self.tree_products.delete(item)
        for p in products:
            barcode = p.get('barcode', '') or ''
            self.tree_products.insert('', tk.END, values=(p['id'], barcode, p['name'], format_rupiah(p['price']), p['stock']))

    def filter_products(self, event=None):
        query = self.entry_search.get().lower()
        if not query:
            self.update_product_tree(self.products)
            return
            
        filtered = [p for p in self.products if query in p['name'].lower() or query in str(p.get('barcode', '')).lower()]
        self.update_product_tree(filtered)

    def scan_barcode(self):
        scanner = BarcodeScanner()
        code = scanner.scan_one()
        if code:
            self.entry_search.delete(0, tk.END)
            self.entry_search.insert(0, code)
            self.handle_barcode_enter(None)

    def handle_barcode_enter(self, event):
        code = self.entry_search.get().strip()
        if not code: return
        product = next((p for p in self.products if str(p.get('barcode')) == code), None)
        if product:
             self.add_item_to_cart(product)
             self.entry_search.delete(0, tk.END)
        else:
             self.filter_products()

    def add_to_cart(self):
        selected = self.tree_products.selection()
        if not selected: return
        item_values = self.tree_products.item(selected)['values']
        p_id = item_values[0]
        product = next((p for p in self.products if p['id'] == p_id), None)
        if product: self.add_item_to_cart(product)

    def add_item_to_cart(self, product):
        qty = 1
        current_in_cart = sum(item['qty'] for item in self.cart if item['product_id'] == product['id'])
        if current_in_cart + qty > product['stock']:
            messagebox.showwarning("Stock", "Stok tidak mencukupi")
            return

        existing_item = next((item for item in self.cart if item['product_id'] == product['id']), None)
        if existing_item:
             existing_item['qty'] += qty
             existing_item['subtotal'] = existing_item['qty'] * existing_item['price']
        else:
            self.cart.append({
                'product_id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'qty': qty,
                'subtotal': product['price'] * qty
            })
        self.refresh_cart_view()

    def remove_from_cart(self):
        selected = self.tree_cart.selection()
        if not selected: return
        item = self.tree_cart.item(selected)['values']
        product_id = item[0]
        self.cart = [c for c in self.cart if c['product_id'] != product_id]
        self.refresh_cart_view()

    def refresh_cart_view(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)
        self.current_subtotal = 0
        for item in self.cart:
            self.tree_cart.insert('', tk.END, values=(
                item['product_id'],
                item['name'],
                format_rupiah(item['price']),
                item['qty'],
                format_rupiah(item['subtotal'])
            ))
            self.current_subtotal += item['subtotal']
        self.update_totals()

    def update_totals(self):
        try:
            disc_p = float(self.entry_discount.get())
        except ValueError:
            disc_p = 0
            
        self.discount_amount = self.current_subtotal * (disc_p / 100)
        taxable_amount = self.current_subtotal - self.discount_amount
        self.tax_amount = taxable_amount * (self.tax_percent / 100)
        self.final_total = taxable_amount + self.tax_amount
        
        self.lbl_subtotal.configure(text=f"Subtotal: {format_rupiah(self.current_subtotal)}")
        self.lbl_discount.configure(text=f"Diskon ({disc_p}%): -{format_rupiah(self.discount_amount)}")
        self.lbl_tax.configure(text=f"Pajak ({self.tax_percent}%): +{format_rupiah(self.tax_amount)}")
        self.lbl_total.configure(text=f"TOTAL: {format_rupiah(self.final_total)}")
        self.calculate_change()

    def calculate_change(self, event=None):
        try:
            pay = float(self.entry_pay.get())
            change = pay - self.final_total
            self.lbl_change.configure(text=f"Kembalian: {format_rupiah(change)}")
        except ValueError:
            self.lbl_change.configure(text="Kembalian: Rp 0")

    def search_member(self):
        phone = self.entry_member_phone.get()
        if not phone: return
        
        member = self.member_model.get_member_by_phone(phone)
        if member:
            self.current_member = member
            self.lbl_member_info.configure(text=f"{member['name']} ({member['points']} pts)", text_color="#4CAF50")
        else:
            self.current_member = None
            self.lbl_member_info.configure(text="Not Found", text_color="#f44336")

    def register_member(self):
        # Simple popup dialog to register
        phone = self.entry_member_phone.get()
        name = simpledialog.askstring("Register Member", "Nama Member:", parent=self)
        
        if name and phone:
            success, msg = self.member_model.add_member(name, phone)
            if success:
                messagebox.showinfo("Success", "Member terdaftar!")
                self.search_member()
            else:
                messagebox.showerror("Error", msg)

    def process_transaction(self):
        if not self.cart: return
        try:
            pay_amount = float(self.entry_pay.get()) if self.entry_pay.get() else 0
            if pay_amount < self.final_total and self.seg_payment.get() == "CASH":
                messagebox.showwarning("Warning", "Pembayaran kurang!")
                return
            
            payment_method = self.seg_payment.get()
            member_id = self.current_member['id'] if self.current_member else None

            # Save to DB
            success = self.transaction_model.create_transaction(
                self.user['username'],
                self.cart,
                self.current_subtotal,
                self.discount_amount,
                self.tax_amount,
                self.final_total,
                payment_method,
                member_id
            )
            
            if success:
                # Add Points Logic (Rp 10,000 = 1 Point)
                if self.current_member:
                    points_earned = int(self.final_total / 10000)
                    if points_earned > 0:
                        self.member_model.add_points(member_id, points_earned)
                
                # Print Receipt
                last_transactions = self.transaction_model.get_all_transactions()
                last_tx = last_transactions[0] if last_transactions else {'id': 0}
                
                print_success, filename = self.printer.print_receipt(
                    last_tx['id'],
                    self.user['username'],
                    self.cart,
                    self.current_subtotal,
                    self.discount_amount,
                    self.tax_amount,
                    self.final_total,
                    payment_method
                )
                
                change = pay_amount - self.final_total if payment_method == "CASH" else 0
                msg = f"Transaksi Berhasil!\nMethode: {payment_method}\n"
                if payment_method == "CASH":
                    msg += f"Kembalian: {format_rupiah(change)}\n"
                
                if self.current_member:
                    msg += f"Poin member: +{points_earned}"
                
                if print_success:
                    msg += f"\nStruk tercetak: {filename}"
                else:
                    msg += f"\nGagal cetak struk: {filename}"
                    
                messagebox.showinfo("Sukses", msg)
                
                self.cart = []
                self.current_member = None
                self.lbl_member_info.configure(text="Guest", text_color="gray")
                self.entry_member_phone.delete(0, tk.END)
                self.refresh_cart_view()
                self.entry_pay.delete(0, tk.END)
                self.refresh_product_list()
            else:
                messagebox.showerror("Error", "Gagal menyimpan transaksi")

        except ValueError:
             messagebox.showerror("Error", "Input pembayaran salah (Pastikan angka)")
