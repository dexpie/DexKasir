import customtkinter as ctk
from models.settings import SettingsModel
from tkinter import messagebox

class SettingsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.settings_model = SettingsModel()
        self.create_widgets()
        self.load_current_settings()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Pengaturan Aplikasi", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))

        # Store Name
        ctk.CTkLabel(self, text="Nama Toko").pack(anchor="w", padx=20)
        self.entry_store_name = ctk.CTkEntry(self, width=300)
        self.entry_store_name.pack(anchor="w", padx=20, pady=(0, 10))

        # Store Address
        ctk.CTkLabel(self, text="Alamat Toko").pack(anchor="w", padx=20)
        self.entry_address = ctk.CTkEntry(self, width=400)
        self.entry_address.pack(anchor="w", padx=20, pady=(0, 10))

        # Tax Rate
        ctk.CTkLabel(self, text="Pajak PPN (%)").pack(anchor="w", padx=20)
        self.entry_tax = ctk.CTkEntry(self, width=100)
        self.entry_tax.pack(anchor="w", padx=20, pady=(0, 10))

        # Theme
        ctk.CTkLabel(self, text="Tema (Restart Required)").pack(anchor="w", padx=20)
        self.combo_theme = ctk.CTkComboBox(self, values=["Dark", "Light", "System"])
        self.combo_theme.pack(anchor="w", padx=20, pady=(0, 10))

        # Save Button
        ctk.CTkButton(self, text="Simpan Pengaturan", command=self.save_settings, fg_color="#4CAF50").pack(anchor="w", padx=20, pady=20)
        
        # Backup Button
        ctk.CTkButton(self, text="Backup Database", command=self.backup_database, fg_color="#2196F3").pack(anchor="w", padx=20, pady=(0, 20))

    def load_current_settings(self):
        self.entry_store_name.insert(0, self.settings_model.get("store_name"))
        self.entry_address.insert(0, self.settings_model.get("store_address"))
        self.entry_tax.insert(0, str(self.settings_model.get("tax_rate")))
        self.combo_theme.set(self.settings_model.get("theme"))

    def backup_database(self):
        import shutil
        import os
        from datetime import datetime
        
        db_file = "kasir.db"
        if not os.path.exists(db_file):
            messagebox.showerror("Error", "Database file not found!")
            return
            
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/pos_backup_{date_str}.db"
        
        try:
            shutil.copy(db_file, backup_file)
            messagebox.showinfo("Success", f"Backup created:\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")

    def save_settings(self):
        name = self.entry_store_name.get()
        addr = self.entry_address.get()
        tax = self.entry_tax.get()
        theme = self.combo_theme.get()
        
        try:
            tax_val = float(tax)
        except ValueError:
            messagebox.showerror("Error", "Pajak harus angka")
            return
            
        self.settings_model.set("store_name", name)
        self.settings_model.set("store_address", addr)
        self.settings_model.set("tax_rate", tax_val)
        self.settings_model.set("theme", theme)
        
        messagebox.showinfo("Success", "Pengaturan disimpan! Restart aplikasi untuk menerapkan tema.")
