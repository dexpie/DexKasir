import customtkinter as ctk
from tkinter import ttk, messagebox
from models.product import ProductModel
from models.audit import AuditModel
from utils.helpers import format_rupiah

class StockOpnameView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.user = user
        
        self.product_model = ProductModel()
        self.audit_model = AuditModel()
        
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Stock Opname (Cek Gudang)", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))
        
        # Note
        ctk.CTkLabel(self, text="Klik baris produk -> 'Edit Actual Stock' -> Masukkan jumlah real. Klik 'Save Adjustment' untuk update.", text_color="gray").pack(anchor="w")

        # Table
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, pady=10)
        
        cols = ('id', 'name', 'system_stock', 'actual_stock', 'variance')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Produk')
        self.tree.heading('system_stock', text='Stok Sistem')
        self.tree.heading('actual_stock', text='Stok Fisik') # Initially same as system
        self.tree.heading('variance', text='Selisih')
        
        self.tree.column('id', width=40)
        self.tree.column('name', width=200)
        self.tree.column('system_stock', width=80)
        self.tree.column('actual_stock', width=80)
        self.tree.column('variance', width=80)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # Adjustment pending map: {product_id: actual_qty}
        self.adjustments = {} 
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="Simpan Perubahan (Adjust)", command=self.save_adjustments, fg_color="#FF9800", hover_color="#F57C00").pack(side="right")
        ctk.CTkButton(btn_frame, text="Reset", command=self.refresh_table, fg_color="gray").pack(side="right", padx=10)

    def refresh_table(self):
        self.adjustments = {}
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        self.products = self.product_model.get_all_products()
        for p in self.products:
            self.tree.insert('', 'end', values=(p['id'], p['name'], p['stock'], p['stock'], 0)) # Default actual = system

    def on_double_click(self, event):
        item_id = self.tree.selection()[0]
        vals = self.tree.item(item_id, 'values')
        
        # Simple input dialog logic... 
        # Since we are in a Frame, we use ctk.CTkInputDialog
        dialog = ctk.CTkInputDialog(text=f"Stok Fisik untuk '{vals[1]}':", title="Input Stok Opname")
        new_val = dialog.get_input()
        
        if new_val is not None:
            try:
                actual = int(new_val)
                system = int(vals[2])
                variance = actual - system
                
                # Update UI row
                self.tree.item(item_id, values=(vals[0], vals[1], system, actual, variance))
                
                # Store adjustment
                self.adjustments[int(vals[0])] = actual
                
            except ValueError:
                messagebox.showerror("Error", "Input harus angka bulat!")

    def save_adjustments(self):
        if not self.adjustments:
            messagebox.showinfo("Info", "Tidak ada perubahan stok.")
            return
            
        confirm = messagebox.askyesno("Confirm", f"Yakin simpan {len(self.adjustments)} penyesuaian stok?")
        if not confirm: return
        
        count = 0
        for pid, actual in self.adjustments.items():
            # Update product stock (We reuse update_product but we need to fetch other fields? Or create update_stock method?)
            # Efficient way: Create update_stock method or fetching first.
            # Let's fetch first.
            p = next((x for x in self.products if x['id'] == pid), None)
            if p:
                old_stock = p['stock']
                diff = actual - old_stock
                # Update
                # Since update_product requires all fields, let's just use SQL via model if possible
                # But we don't have partial update in model. Let's assume we pass existing vals.
                # Actually, better to add update_stock method in product model for atomic update.
                # I will do full update since I have p
                
                # But wait, p has 'price' etc.
                if self.product_model.update_product(p['id'], p['name'], p['price'], actual, p.get('barcode'), p.get('cost_price')):
                    # Log Audit
                    self.audit_model.log_action(self.user['username'], "STOCK_OPNAME", f"Product {p['name']}: {old_stock} -> {actual} ({diff:+d})")
                    count += 1
        
        messagebox.showinfo("Success", f"{count} produk berhasil disesuaikan!")
        self.refresh_table()
