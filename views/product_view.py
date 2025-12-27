import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from models.product import ProductModel
from utils.helpers import format_rupiah

class ProductView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.product_model = ProductModel()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # -- Title --
        ctk.CTkLabel(self, text="Manajemen Produk", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))

        # -- Form Frame --
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x", pady=5)

        # Row 1
        frame_row1 = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_row1.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_row1, text="Barcode").pack(side="left", padx=5)
        self.entry_barcode = ctk.CTkEntry(frame_row1, width=150)
        self.entry_barcode.pack(side="left", padx=5)
        
        btn_scan = ctk.CTkButton(frame_row1, text="Scan", width=60, command=self.scan_barcode)
        btn_scan.pack(side="left", padx=5)

        ctk.CTkLabel(frame_row1, text="Nama Produk").pack(side="left", padx=5)
        self.entry_name = ctk.CTkEntry(frame_row1, width=200)
        self.entry_name.pack(side="left", padx=5)

        # Row 2
        frame_row2 = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_row2.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_row2, text="Harga (Rp)").pack(side="left", padx=5)
        self.entry_price = ctk.CTkEntry(frame_row2, width=150)
        self.entry_price.pack(side="left", padx=5)

        ctk.CTkLabel(frame_row2, text="Stok").pack(side="left", padx=5)
        self.entry_stock = ctk.CTkEntry(frame_row2, width=100)
        self.entry_stock.pack(side="left", padx=5)

        # Buttons
        frame_buttons = ctk.CTkFrame(frame_form, fg_color="transparent")
        frame_buttons.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(frame_buttons, text="Tambah", command=self.add_product, fg_color="#4CAF50", hover_color="#388E3C").pack(side="left", padx=5)
        ctk.CTkButton(frame_buttons, text="Update", command=self.update_product, fg_color="#FF9800", hover_color="#F57C00").pack(side="left", padx=5)
        ctk.CTkButton(frame_buttons, text="Hapus", command=self.delete_product, fg_color="#f44336", hover_color="#d32f2f").pack(side="left", padx=5)
        ctk.CTkButton(frame_buttons, text="Reset", command=self.reset_form, fg_color="gray").pack(side="left", padx=5)

        # -- Table --
        # CustomTkinter doesn't have a Treeview, so we style the ttk.Treeview
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b", 
                        rowheight=25)
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, pady=10)

        columns = ('id', 'barcode', 'name', 'price', 'stock')
        self.tree = ttk.Treeview(frame_table, columns=columns, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('barcode', text='Barcode')
        self.tree.heading('name', text='Nama Produk')
        self.tree.heading('price', text='Harga')
        self.tree.heading('stock', text='Stok')

        self.tree.column('id', width=40)
        self.tree.column('barcode', width=100)
        self.tree.column('name', width=200)
        self.tree.column('price', width=100)
        self.tree.column('stock', width=60)

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    # Reuse logic from prev implementation, just UI changed
    def scan_barcode(self):
        from utils.scanner import BarcodeScanner
        scanner = BarcodeScanner()
        code = scanner.scan_one()
        if code:
            self.entry_barcode.delete(0, tk.END)
            self.entry_barcode.insert(0, code)
            messagebox.showinfo("Scan", f"Barcode: {code}")

        # Configure tag for low stock
        self.tree.tag_configure('low_stock', background='#5c1e1e', foreground='white') # Dark red background

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        products = self.product_model.get_all_products()
        for p in products:
            barcode = p.get('barcode') or ""
            tags = ('low_stock',) if p['stock'] < 5 else ()
            self.tree.insert('', tk.END, values=(p['id'], barcode, p['name'], format_rupiah(p['price']), p['stock']), tags=tags)

    def reset_form(self):
        self.entry_barcode.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.selected_id = None

    def on_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item = self.tree.item(selected_item)
        values = item['values']
        
        self.selected_id = values[0]
        
        self.entry_barcode.delete(0, tk.END)
        self.entry_barcode.insert(0, values[1] if values[1] != 'None' else "")
        
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[2])
        
        price_str = str(values[3]).replace("Rp ", "").replace(".", "")
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, price_str)
        
        self.entry_stock.delete(0, tk.END)
        self.entry_stock.insert(0, values[4])

    def add_product(self):
        barcode = self.entry_barcode.get()
        name = self.entry_name.get()
        price = self.entry_price.get()
        stock = self.entry_stock.get()

        if not name or not price or not stock:
            messagebox.showwarning("Warning", "Nama, Harga, dan Stok harus diisi")
            return

        try:
            price = float(price)
            stock = int(stock)
            if self.product_model.add_product(name, price, stock, barcode):
                messagebox.showinfo("Success", "Produk berhasil ditambahkan")
                self.reset_form()
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Gagal menambah produk (Mungkin barcode duplikat)")
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus angka")

    def update_product(self):
        if not hasattr(self, 'selected_id') or not self.selected_id:
            messagebox.showwarning("Warning", "Pilih produk untuk diedit")
            return

        barcode = self.entry_barcode.get()
        name = self.entry_name.get()
        price = self.entry_price.get()
        stock = self.entry_stock.get()

        try:
            price = float(price)
            stock = int(stock)
            if self.product_model.update_product(self.selected_id, name, price, stock, barcode):
                messagebox.showinfo("Success", "Produk berhasil diupdate")
                self.reset_form()
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Gagal update produk")
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus angka")

    def delete_product(self):
        if not hasattr(self, 'selected_id') or not self.selected_id:
            messagebox.showwarning("Warning", "Pilih produk untuk dihapus")
            return

        if messagebox.askyesno("Confirm", "Yakin ingin menghapus produk ini?"):
            if self.product_model.delete_product(self.selected_id):
                messagebox.showinfo("Success", "Produk berhasil dihapus")
                self.reset_form()
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Gagal menghapus produk")
