import customtkinter as ctk
from tkinter import ttk, messagebox
from models.expense import ExpenseModel
from utils.helpers import format_rupiah

class ExpenseView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.user = user
        self.expense_model = ExpenseModel()
        
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Manajemen Pengeluaran (Beban Operasional)", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))
        
        # Form
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x")
        
        ctk.CTkLabel(frame_form, text="Kategori").pack(side="left", padx=10)
        self.combo_category = ctk.CTkComboBox(frame_form, values=["Listrik", "Sewa", "Gaji", "Internet", "Packaging", "Lainnya"])
        self.combo_category.pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_form, text="Rp").pack(side="left", padx=5)
        self.entry_amount = ctk.CTkEntry(frame_form, placeholder_text="0")
        self.entry_amount.pack(side="left", padx=5)
        
        ctk.CTkLabel(frame_form, text="Deskripsi").pack(side="left", padx=10)
        self.entry_desc = ctk.CTkEntry(frame_form, width=200)
        self.entry_desc.pack(side="left", padx=10)
        
        ctk.CTkButton(frame_form, text="Simpan Pengeluaran", command=self.add_expense, fg_color="#F44336").pack(side="left", padx=20)
        
        # Table
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, pady=20)
        
        cols = ('date', 'category', 'amount', 'desc', 'user')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('date', text='Tanggal')
        self.tree.heading('category', text='Kategori')
        self.tree.heading('amount', text='Jumlah')
        self.tree.heading('desc', text='Deskripsi')
        self.tree.heading('user', text='User')
        
        self.tree.column('date', width=100)
        self.tree.column('category', width=100)
        self.tree.column('amount', width=120)
        self.tree.column('desc', width=200)
        
        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        rows = self.expense_model.get_expenses()
        for r in rows:
            self.tree.insert('', 'end', values=(r['date'], r['category'], format_rupiah(r['amount']), r['description'], r['user']))

    def add_expense(self):
        cat = self.combo_category.get()
        amt = self.entry_amount.get()
        desc = self.entry_desc.get()
        
        if not amt: return
        try:
            val = float(amt)
        except:
            messagebox.showerror("Error", "Jumlah harus angka")
            return
            
        if self.expense_model.add_expense(cat, val, desc, self.user['username']):
            messagebox.showinfo("Success", "Pengeluaran dicatat.")
            self.entry_amount.delete(0, 'end')
            self.entry_desc.delete(0, 'end')
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Gagal menyimpan")
