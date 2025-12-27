import os
from datetime import datetime
from utils.helpers import format_rupiah
import qrcode

class ReceiptPrinter:
    def __init__(self, settings_model):
        self.settings = settings_model

    def print_receipt(self, transaction_id, cashier_name, items, subtotal, discount, tax, total, payment_method="CASH"):
        store_name = self.settings.get("store_name")
        address = self.settings.get("store_address")
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        header_msg = self.settings.get("receipt_header") or "Selamat Datang"
        footer_msg = self.settings.get("receipt_footer") or "Terima Kasih"

        # Basic text receipt formatting
        receipt_lines = []
        receipt_lines.append(f"{store_name.center(32)}")
        receipt_lines.append(f"{address.center(32)}")
        receipt_lines.append(f"{header_msg.center(32)}")
        receipt_lines.append("-" * 32)
        receipt_lines.append(f"Date: {date_str}")
        receipt_lines.append(f"TxID: {transaction_id}")
        receipt_lines.append(f"Cashier: {cashier_name}")
        receipt_lines.append(f"Method : {payment_method}")
        receipt_lines.append("-" * 32)
        
        for item in items:
            name = item['name'][:16] # Truncate
            qty = item['qty']
            price = item['price']
            total_item = item['subtotal']
            receipt_lines.append(f"{name:<16} x{qty} {total_item:>8,.0f}")
            
        receipt_lines.append("-" * 32)
        receipt_lines.append(f"Subtotal : {subtotal:>15,.0f}")
        if discount > 0:
            receipt_lines.append(f"Discount : -{discount:>14,.0f}")
        receipt_lines.append(f"Tax      : {tax:>15,.0f}")
        receipt_lines.append(f"TOTAL    : {total:>15,.0f}")
        receipt_lines.append("-" * 32)
        receipt_lines.append(f"{footer_msg.center(32)}")
        
        receipt_lines.append("-" * 32)
        receipt_lines.append("Scan for digital receipt:")
        
        receipt_text = "\n".join(receipt_lines)
        
        # Save to file
        if not os.path.exists("receipts"):
            os.makedirs("receipts")
            
        filename = f"receipts/tx_{transaction_id}_{int(datetime.now().timestamp())}.txt"
        qr_filename = filename.replace(".txt", ".png")
        
        try:
            with open(filename, "w") as f:
                f.write(receipt_text)
                
            # Generate QR Code
            qr_data = f"RECEIPT\n{store_name}\nTx: {transaction_id}\nTotal: {total}\nDate: {date_str}"
            qr = qrcode.make(qr_data)
            qr.save(qr_filename)
            
            return True, f"{filename}\n(QR Saved: {qr_filename})"
        except Exception as e:
            print(f"Print error: {e}")
            return False, str(e)
