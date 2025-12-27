import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
from models.member import MemberModel
from utils.helpers import format_rupiah

class MemberView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.member_model = MemberModel()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Manajemen Member & Kasbon", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))
        
        # Form
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x")
        
        ctk.CTkLabel(frame_form, text="Nama").pack(side="left", padx=10)
        self.entry_name = ctk.CTkEntry(frame_form)
        self.entry_name.pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_form, text="Nomor HP").pack(side="left", padx=10)
        self.entry_phone = ctk.CTkEntry(frame_form)
        self.entry_phone.pack(side="left", padx=10)
        
        ctk.CTkButton(frame_form, text="Tambah Member", command=self.add_member, fg_color="#4CAF50").pack(side="left", padx=20)
        
        # Table
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, pady=20, padx=5)
        
        cols = ('id', 'name', 'phone', 'points', 'debt')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Nama')
        self.tree.heading('phone', text='HP')
        self.tree.heading('points', text='Poin')
        self.tree.heading('debt', text='Hutang (Kasbon)')
        
        self.tree.column('id', width=50)
        self.tree.column('name', width=200)
        self.tree.column('debt', width=150)
        
        self.tree.pack(fill="both", expand=True)
        
        # Actions
        frame_actions = ctk.CTkFrame(self, fg_color="transparent")
        frame_actions.pack(fill="x", pady=10)
        
        ctk.CTkButton(frame_actions, text="Bayar Hutang", command=self.pay_debt, fg_color="#2196F3").pack(side="right") # Blue

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        members = self.member_model.get_all_members()
        for m in members:
            self.tree.insert('', 'end', values=(m['id'], m['name'], m['phone'], m['points'], format_rupiah(m['debt'])))

    def add_member(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        if not name or not phone:
            messagebox.showwarning("Warning", "Isi Nama dan HP!")
            return
            
        if self.member_model.add_member(name, phone):
            messagebox.showinfo("Success", "Member ditambahkan")
            self.refresh_table()
            self.entry_name.delete(0, 'end')
            self.entry_phone.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Gagal (HP mungkin duplikat)")

    def pay_debt(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Pilih Member dulu!")
            return
            
        val = self.tree.item(sel)['values']
        mid = val[0]
        name = val[1]
        
        # Get numeric debt from db to be safe (val has "Rp...")
        # Simpler: search by phone(val[2]) or just select by id
        # Let's simple ask amount
        
        amount = simpledialog.askfloat("Bayar Hutang", f"Masukkan jumlah bayar untuk {name}:")
        if amount and amount > 0:
             if self.member_model.update_debt(mid, -amount):
                 messagebox.showinfo("Success", f"Pembayaran Rp {amount:,.0f} diterima.")
                 self.log_audit(f"Member {name} pay debt: {amount}")
                 self.refresh_table()
             else:
                 messagebox.showerror("Error", "Gagal update hutang.")

    def log_audit(self, msg):
        from models.audit import AuditModel
        AuditModel().log_action("Admin", "PAY_DEBT", msg)
