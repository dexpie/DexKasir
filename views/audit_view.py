import customtkinter as ctk
from tkinter import ttk
from models.audit import AuditModel

class AuditView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        self.audit_model = AuditModel()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Audit Logs (Security Trail)", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))
        
        ctk.CTkButton(self, text="Refresh Logs", command=self.refresh_table).pack(anchor="e", pady=5)

        # Table
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True)
        
        cols = ('id', 'time', 'user', 'action', 'details')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('time', text='Waktu')
        self.tree.heading('user', text='User')
        self.tree.heading('action', text='Aksi')
        self.tree.heading('details', text='Detail')
        
        self.tree.column('id', width=40)
        self.tree.column('time', width=150)
        self.tree.column('user', width=100)
        self.tree.column('action', width=150)
        self.tree.column('details', width=300)
        
        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        logs = self.audit_model.get_logs(limit=100)
        for log in logs:
            self.tree.insert('', 'end', values=(log['id'], log['timestamp'], log['user'], log['action'], log['details']))
