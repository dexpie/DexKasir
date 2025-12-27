import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import UserModel

class UserView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.user_model = UserModel()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Header
        ctk.CTkLabel(self, text="Manajemen User (Admin)", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))

        # Form Frame
        frame_form = ctk.CTkFrame(self)
        frame_form.pack(fill="x", padx=10, pady=5)
        
        # Row 1
        ctk.CTkLabel(frame_form, text="Username").pack(side="left", padx=10)
        self.entry_username = ctk.CTkEntry(frame_form, width=150)
        self.entry_username.pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_form, text="Password").pack(side="left", padx=10)
        self.entry_password = ctk.CTkEntry(frame_form, width=150, show="*")
        self.entry_password.pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_form, text="Role").pack(side="left", padx=10)
        self.combo_role = ctk.CTkComboBox(frame_form, values=["kasir", "admin"], width=100)
        self.combo_role.set("kasir")
        self.combo_role.pack(side="left", padx=10)
        
        ctk.CTkButton(frame_form, text="Tambah User", command=self.add_user, fg_color="#4CAF50").pack(side="left", padx=20)
        
        # Table
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        cols = ('id', 'username', 'role')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('username', text='Username')
        self.tree.heading('role', text='Role')
        
        self.tree.column('id', width=50)
        self.tree.column('username', width=150)
        self.tree.column('role', width=100)
        self.tree.pack(fill="both", expand=True)
        
        # Delete Button
        ctk.CTkButton(self, text="Hapus User Terpilih", command=self.delete_user, fg_color="#f44336").pack(padx=10, pady=10, anchor="e")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        users = self.user_model.get_all_users()
        for u in users:
            self.tree.insert('', tk.END, values=(u['id'], u['username'], u['role']))

    def add_user(self):
        user = self.entry_username.get()
        pwd = self.entry_password.get()
        role = self.combo_role.get()
        
        if not user or not pwd:
            messagebox.showwarning("Warning", "Username dan Password wajib diisi")
            return
            
        success, msg = self.user_model.add_user(user, pwd, role)
        if success:
            messagebox.showinfo("Success", "User berhasil ditambahkan")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showerror("Error", msg)

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih user untuk dihapus")
            return
            
        item = self.tree.item(selected)['values']
        u_id = item[0]
        u_name = item[1]
        
        if u_name == 'admin': # Prevent deleting main admin (simple check)
            messagebox.showerror("Error", "Tidak bisa menghapus user 'admin'")
            return
            
        if messagebox.askyesno("Confirm", f"Hapus user '{u_name}'?"):
            if self.user_model.delete_user(u_id):
                messagebox.showinfo("Success", "User dihapus")
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Gagal menghapus user")
