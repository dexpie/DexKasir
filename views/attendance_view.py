import customtkinter as ctk
from datetime import datetime
from PIL import Image
import tkinter as tk
from tkinter import ttk, messagebox
from models.attendance import AttendanceModel

class AttendanceView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.user = user
        
        self.attendance_model = AttendanceModel()
        
        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        ctk.CTkLabel(self, text=f"Absensi Karyawan: {self.user['username']}", font=("Roboto Medium", 20)).pack(anchor="w", pady=(0, 20))
        
        # Status Card
        self.frame_status = ctk.CTkFrame(self)
        self.frame_status.pack(fill="x", pady=10)
        
        self.lbl_date = ctk.CTkLabel(self.frame_status, text=datetime.now().strftime("%A, %d %B %Y"), font=("Roboto", 16))
        self.lbl_date.pack(pady=5)
        
        self.lbl_status = ctk.CTkLabel(self.frame_status, text="Status: CHECKING...", font=("Roboto Medium", 24))
        self.lbl_status.pack(pady=10)
        
        self.btn_action = ctk.CTkButton(self.frame_status, text="CLOCK IN", command=self.do_action, height=50, font=("Roboto", 18))
        self.btn_action.pack(pady=20)
        
        # History
        ctk.CTkLabel(self, text="Riwayat Absensi Terakhir", font=("Roboto Medium", 16)).pack(anchor="w", pady=(20, 10))
        
        frame_table = ctk.CTkFrame(self)
        frame_table.pack(fill="both", expand=True)
        
        cols = ('date', 'user', 'in', 'out')
        self.tree = ttk.Treeview(frame_table, columns=cols, show='headings')
        self.tree.heading('date', text='Tanggal')
        self.tree.heading('user', text='Staff')
        self.tree.heading('in', text='Masuk')
        self.tree.heading('out', text='Pulang')
        self.tree.pack(fill="both", expand=True)
        
        self.load_history()

    def update_status(self):
        status = self.attendance_model.check_today(self.user['username'])
        if not status:
            self.lbl_status.configure(text="Status: BELUM ABSEN", text_color="orange")
            self.btn_action.configure(text="CLOCK IN", fg_color="#4CAF50", state="normal")
            self.current_state = "in"
        elif status['clock_in'] and not status['clock_out']:
             self.lbl_status.configure(text=f"Status: WORKING (In: {status['clock_in']})", text_color="#2196F3")
             self.btn_action.configure(text="CLOCK OUT", fg_color="#f44336", state="normal")
             self.current_state = "out"
        else:
            self.lbl_status.configure(text=f"Status: COMPLETED (Out: {status['clock_out']})", text_color="gray")
            self.btn_action.configure(text="SELESAI HARI INI", state="disabled", fg_color="gray")
            self.current_state = "done"

    def do_action(self):
        if self.current_state == "in":
            success, msg = self.attendance_model.clock_in(self.user['username'])
            if success:
                messagebox.showinfo("Success", f"Selamat Bekerja! {msg}")
                self.update_status()
                self.load_history()
            else:
                messagebox.showerror("Error", msg)
        elif self.current_state == "out":
            success, msg = self.attendance_model.clock_out(self.user['username'])
            if success:
                messagebox.showinfo("Success", f"Hati-hati di jalan! {msg}")
                self.update_status()
                self.load_history()
            else:
                messagebox.showerror("Error", msg)

    def load_history(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = self.attendance_model.get_history()
        for r in rows:
            self.tree.insert('', 'end', values=(r[2], r[1], r[3], r[4] or "-"))
