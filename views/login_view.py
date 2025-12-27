import customtkinter as ctk
from tkinter import messagebox
from models.user import UserModel
from views.dashboard_view import DashboardView

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DexKasir - Login")
        self.geometry("400x450")
        self.resizable(False, False)
        
        self.user_model = UserModel()
        self.create_widgets()

    def create_widgets(self):
        # Center Frame
        frame = ctk.CTkFrame(self)
        frame.pack(pady=40, padx=40, fill="both", expand=True)

        # Title
        label_title = ctk.CTkLabel(frame, text="DexKasir POS", font=("Roboto Medium", 24))
        label_title.pack(pady=20)
        
        label_subtitle = ctk.CTkLabel(frame, text="Sign in to your account", font=("Roboto", 12))
        label_subtitle.pack(pady=(0, 20))

        # Username
        self.entry_username = ctk.CTkEntry(frame, placeholder_text="Username")
        self.entry_username.pack(pady=10, padx=20, fill="x")
        self.entry_username.focus()

        # Password
        self.entry_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10, padx=20, fill="x")
        
        # Bind Enter
        self.bind('<Return>', lambda event: self.handle_login())

        # Button
        btn_login = ctk.CTkButton(frame, text="Login", command=self.handle_login)
        btn_login.pack(pady=20, padx=20, fill="x")
        
        # Hint
        ctk.CTkLabel(frame, text="Default: admin/admin123 | kasir/kasir123", text_color="gray", font=("Roboto", 10)).pack(pady=5)

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Username and Password cannot be empty.")
            return

        user = self.user_model.login(username, password)
        if user:
            self.withdraw()
            # Pass reference to this window so dashboard can reopen it on logout
            dashboard = DashboardView(self, user)
            dashboard.grab_set()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
