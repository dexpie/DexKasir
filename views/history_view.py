import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from models.transaction import TransactionModel
from utils.helpers import format_rupiah

class HistoryView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.transaction_model = TransactionModel()
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        # Header
        ctk.CTkLabel(self, text="Riwayat Transaksi", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkButton(self, text="Refresh Data", command=self.refresh_data, width=120).pack(anchor="w", pady=(0, 10))

        # Treeview
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True)
        
        cols = ('id', 'date', 'cashier', 'total')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        
        self.tree.heading('id', text='ID Transaksi')
        self.tree.heading('date', text='Tanggal')
        self.tree.heading('cashier', text='Kasir')
        self.tree.heading('total', text='Total')
        
        self.tree.column('id', width=80)
        self.tree.column('date', width=150)
        self.tree.column('cashier', width=100)
        self.tree.column('total', width=120)
        
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.tree.bind('<Double-1>', self.show_details)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        transactions = self.transaction_model.get_all_transactions()
        for t in transactions:
            self.tree.insert('', tk.END, values=(
                t['id'], 
                t['date'], 
                t['cashier_name'], 
                format_rupiah(t['final_total'])
            ))

    def show_details(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected)['values']
        t_id = item[0]
        
        # Get items
        items = self.transaction_model.get_transaction_items(t_id)
        
        # Details Popup
        top = ctk.CTkToplevel(self)
        top.title(f"Detail Transaksi #{t_id}")
        top.geometry("500x400")
        
        ctk.CTkLabel(top, text=f"Items in Transaction #{t_id}", font=("Roboto Medium", 16)).pack(pady=10)

        cols = ('product', 'qty', 'subtotal')
        tree_det = ttk.Treeview(top, columns=cols, show='headings')
        tree_det.heading('product', text='Produk')
        tree_det.heading('qty', text='Qty')
        tree_det.heading('subtotal', text='Subtotal')
        tree_det.pack(fill="both", expand=True, padx=10, pady=10)
        
            ))
            
        # Void Button
        status = tx.get('status', 'SUCCESS')
        if status != 'REFUNDED':
             btn_void = ctk.CTkButton(top, text="VOID / REFUND", fg_color="#d32f2f", hover_color="#b71c1c", 
                                     command=lambda: self.void_transaction(top, t_id))
             btn_void.pack(pady=10)
        else:
            ctk.CTkLabel(top, text="[REFUNDED]", text_color="red", font=("Roboto", 14, "bold")).pack(pady=10)

    def void_transaction(self, window, tx_id):
        from tkinter import messagebox
        if messagebox.askyesno("Konfirmasi Refund", "Batalkan transaksi ini? Stok akan dikembalikan."):
            success, msg = self.transaction_model.refund_transaction(tx_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                window.destroy()
                self.refresh_data()
            else:
                messagebox.showerror("Gagal", msg)
