import customtkinter as ctk
from views.login_view import LoginView
from database.db import Database
from models.settings import SettingsModel

if __name__ == "__main__":
    # Ensure database is initialized
    db = Database()
    db.init_db()
    
    # Load settings to apply theme
    settings = SettingsModel()
    theme = settings.get("theme")
    ctk.set_appearance_mode(theme) # "System", "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue" (standard), "green", "dark-blue"

    app = LoginView()
    app.mainloop()
