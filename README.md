# DexKasir 🏪

**DexKasir** is a modern, feature-rich Point of Sale (POS) application built with Python (`CustomTkinter`). It is designed for enterprise-level retail management with strong security, AI features, and dual-screen support.

![DexKasir Screenshot](https://via.placeholder.com/800x450?text=DexKasir+Dashboard)

## 🚀 Key Features

### 1. **Core Transaction System (with Dual Screen)** 🖥️
*   **Customer Facing Display (CFD)**: Open a second window for customers to see cart items and total in real-time.
*   **Fast Checkout**: Scan barcodes or search products instantly.
*   **Flexible Payment**: Support CASH, QRIS, and TRANSFER methods.
*   **WhatsApp Share**: Send digital receipts directly to customer's WhatsApp.

### 2. **Artificial Intelligence (AI)** 🤖
*   **Sales Forecasting**: Uses Linear Regression to predict sales trend for the next 7 days based on history.
*   **Smart Dashboard**: Overview card showing predicted vs actual performance.

### 3. **Security & Loss Prevention** 👮‍♂️
*   **Audit Logger**: Records every sensitive action (Login, Delete Product, Void) with timestamp and user details. 🆕
*   **Stock Opname**: Feature to reconcile Physical Stock vs System Stock and automatically adjust variances. 🆕

### 4. **Inventory Management**
*   **CRUD Products**: Add, edit, delete products easily.
*   **Barcode Generator**: Generate and print custom barcode labels.
*   **Bulk Import**: Upload hundreds of products via **Excel/CSV**.
*   **Low Stock Alert**: Visual highlights and dashboard widgets.

### 5. **Business Intelligence (Profit & Ops)** 📈
*   **Command Center Dashboard**: Real-time stats for Omzet, Transactions, and Stock.
*   **Profit Tracking**: Track Net Profit (Revenue - Cost).
*   **Shift Management**: Manage Cash Drawer sessions (Open/Close).
*   **Reports**: Export to PDF & Excel.

### 6. **Marketing & Branding** 🎨
*   **Promo Management**: Manage discount codes (`DISKON50`).
*   **Receipt Branding**: Customize receipt Header/Footer.
*   **Themes**: Light / Dark Mode.

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

---
*Created by [Dexpie](https://github.com/dexpie)*
