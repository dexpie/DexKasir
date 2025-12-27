# DexKasir - Aplikasi Kasir Python

Aplikasi Point of Sale (POS) sederhana untuk UMKM berbasis Python dan Tkinter.

## Fitur
- Login Multi-Role (Admin & Kasir)
- Manajemen Produk (CRUD)
- Transaksi Penjualan (Otomatis hitung, potong stok)
- Riwayat Transaksi

## Struktur Project
```
DexKasir/
├── database/     # Koneksi DB & Init
├── models/       # Logika Data (User, Product, Transaction)
├── views/        # Tampilan GUI (Login, Dashboard, dll)
├── utils/        # Helper functions
└── main.py       # Entry point
```

## Cara Menjalankan
1. Pastikan Python sudah terinstall.
2. Jalankan perintah berikut di terminal:
   ```bash
   python main.py
   ```

## Akun Default
Saat aplikasi pertama kali dijalankan, database akan otomatis membuat akun default:

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |
| Kasir | kasir    | kasir123 |

## Teknologi
- Python 3
- Tkinter (GUI)
- SQLite (Database)
