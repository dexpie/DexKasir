# DexKasir 🏪

**DexKasir** is a modern, feature-rich Point of Sale (POS) application built for businesses that demand efficiency, security, and smart insights.

![DexKasir Screenshot](https://via.placeholder.com/800x450?text=DexKasir+Dashboard)

## 🚀 Key Features

### 1. **Core Transaction & Finance** 💸
*   **Kasbon System**: Allow trusted members to **pay later**. Manage debts and payments directly in the app. 🆕
*   **Automated Email Reports**: Send daily sales recap PDF to the owner's email automatically on Shift Close. 🆕
*   **Flexible Payment**: CASH, QRIS, TRANSFER, and KASBON.

### 2. **Artificial Intelligence (AI)** 🤖
*   **Sales Forecasting**: Uses Linear Regression to predict sales trend for the next 7 days.
*   **Smart Dashboard**: Overview card showing predicted vs actual performance.

### 3. **Security & Loss Prevention** 👮‍♂️
*   **Audit Logger**: Records every sensitive action (Login, Delete Product, Void).
*   **Stock Opname**: Feature to reconcile Physical Stock vs System Stock.

### 4. **Hardware Support** 🖥️
*   **Dual Screen**: Customer Facing Display (CFD) for real-time cart visibility.
*   **Receipt Printer**: Auto-print receipt + Generate QR Code.

### 5. **Inventory Management**
*   **CRUD Products**: Add, edit, delete products easily.
*   **Barcode Generator**: Generate and print custom barcode labels.
*   **Bulk Import**: Upload hundreds of products via **Excel/CSV**.
*   **Low Stock Alert**: Visual highlights and dashboard widgets.

## 🛠️ Configuration (Email)
To use Automated Email Reports, go to **Settings** and configure:
*   **Email Sender**: Your Gmail address.
*   **App Password**: Google Account > Security > App Passwords (NOT your login password).
*   **Recipient**: Owner's email.

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

3.  **Run Application**
    ```bash
    python main.py
    ```

## 🔐 Accounts (Default)
*   **Username**: `admin`
*   **Password**: `admin123`

---
*Created by [Dexpie](https://github.com/dexpie)*
