# DexKasir 🏪

**DexKasir** is a modern, feature-rich Point of Sale (POS) application built with Python (`CustomTkinter`). It helps small to medium retail businesses manage sales, inventory, and customers efficiently.

![DexKasir Screenshot](https://via.placeholder.com/800x450?text=DexKasir+Dashboard)

## 🚀 Key Features

### 1. **Core Transaction System**
*   **Fast Checkout**: Scan barcodes or search products instantly.
*   **Cart Management**: Edit quantities, apply discounts per item or total.
*   **Flexible Payment**: Support CASH, QRIS, and TRANSFER methods.
*   **Receipt Printing**: Auto-generate text receipts (`.txt`) and Digital QR receipts (`.png`).

### 2. **Inventory Management**
*   **CRUD Products**: Add, edit, delete products easily.
*   **Barcode Support**: Scan existing barcodes or **Generate New Barcode Labels**.
*   **Bulk Import**: Upload hundreds of products via **Excel/CSV**.
*   **Low Stock Alert**: Visual highlights when stock runs low (< 5).

### 3. **Membership & Loyalty** 💎
*   **Member Database**: Register customers by name & phone.
*   **Loyalty Points**: Auto-earn 1 point for every Rp 10,000 spent.
*   **Quick Lookup**: Find members by phone number during transaction.

### 4. **Business Intelligence (Profit & Ops)** 📈
*   **Profit Tracking**: Input **Cost Price (Modal)** and track **Net Profit** automatically.
*   **Shift Management**: "Open Shift" to record start cash and "Close Shift" to verify actual cash vs system.
*   **Reports**: Monthly sales report, export to **PDF & Excel**.
*   **Analytics**: Visual charts for Sales Trend (7 Days) and Top Products.

### 5. **Marketing & Customization** 🎨
*   **Promo Codes**: Create discount codes (Percentage or Fixed Amount) to boost sales (e.g., `DISKON50`).
*   **Receipt Branding**: Customize receipt **Header** (Greeting) and **Footer** (Thank You Message).
*   **Themes**: Switch between Light, Dark, or System theme.

## 🛠️ Installation

1.  **Clone Repository**
    ```bash
    git clone https://github.com/dexpie/DexKasir.git
    cd DexKasir
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Requirements: customtkinter, pillow, matplotlib, pandas, openpyxl, reportlab, qrcode, python-barcode)*

3.  **Run Application**
    ```bash
    python main.py
    ```

## 🔐 Accounts (Default)
*   **Username**: `admin`
*   **Password**: `admin123`

## 📂 Project Structure
*   `main.py`: Entry point.
*   `views/`: UI Components (Transaction, History, Settings, etc.).
*   `models/`: Database logic (Product, User, Transaction, Member, etc.).
*   `utils/`: Helpers (Printer, PDF Generator, Migrations).
*   `database/`: SQLite connection & initialization.
*   `receipts/`: Saved receipt files.
*   `backups/`: Database backups.

## 🤝 Contributing
Feel free to open issues or submit pull requests for new features!

---
*Created by [Dexpie](https://github.com/dexpie)*
