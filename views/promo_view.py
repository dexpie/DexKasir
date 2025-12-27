import customtkinter as ctk
from tkinter import ttk, messagebox
from models.promo import PromoModel
from utils.helpers import format_rupiah

class PromoView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.promo_model = PromoModel()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Manajemen Promo", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))

        # Form
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x")

        ctk.CTkLabel(frame_form, text="Kode Promo").pack(side="left", padx=10, pady=10)
        self.entry_code = ctk.CTkEntry(frame_form, width=150)
        self.entry_code.pack(side="left", padx=10)

        ctk.CTkLabel(frame_form, text="Tipe").pack(side="left", padx=10)
        self.combo_type = ctk.CTkComboBox(frame_form, values=["PERCENT", "FIXED"], width=100)
        self.combo_type.pack(side="left", padx=10)

        ctk.CTkLabel(frame_form, text="Nilai (Rp/%)").pack(side="left", padx=10)
        self.entry_value = ctk.CTkEntry(frame_form, width=100)
        self.entry_value.pack(side="left", padx=10)

        ctk.CTkButton(frame_form, text="Simpan", command=self.add_promo, fg_color="#4CAF50").pack(side="left", padx=20)

        # Table
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, pady=20)
        
        cols = ('id', 'code', 'type', 'value', 'active')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('code', text='Kode Promo')
        self.tree.heading('type', text='Tipe Diskon')
        self.tree.heading('value', text='Nilai')
        self.tree.heading('active', text='Status')
        
        self.tree.column('id', width=50)
        self.tree.column('code', width=150)
        self.tree.column('type', width=100)
        self.tree.column('value', width=100)
        self.tree.column('active', width=80)
        self.tree.pack(fill="both", expand=True)
        
        ctk.CTkButton(self, text="Hapus Promo Terpilih", command=self.delete_promo, fg_color="#f44336").pack(anchor="w", pady=10)

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        promos = self.promo_model.get_all_promos()
        for p in promos:
            val = f"{p['value']}%" if p['type'] == 'PERCENT' else format_rupiah(p['value'])
            active = "Aktif" if p['active'] else "Non-Aktif"
            self.tree.insert('', 'end', values=(p['id'], p['code'], p['type'], val, active))

    def add_promo(self):
        code = self.entry_code.get().upper()
        ptype = self.combo_type.get()
        try:
            val = float(self.entry_value.get())
        except ValueError:
            messagebox.showerror("Error", "Nilai harus angka")
            return
            
        if not code:
            messagebox.showwarning("Warning", "Kode harus diisi")
            return
            
        if self.promo_model.create_promo(code, ptype, val):
            messagebox.showinfo("Success", "Promo ditambahkan")
            self.refresh_table()
            self.entry_code.delete(0, 'end')
            self.entry_value.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Gagal (Kode mungkin duplikat)")

    def delete_promo(self):
        sel = self.tree.selection()
        if not sel: return
        pid = self.tree.item(sel)['values'][0]
        if self.promo_model.delete_promo(pid):
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Gagal hapus")
