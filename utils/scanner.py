import cv2
from pyzbar.pyzbar import decode
import time

class BarcodeScanner:
    def scan_one(self):
        """
        Opens camera, scans for a barcode, returns the data as string.
        Returns None if cancelled or timed out.
        """
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open video device.")
            return None

        found_barcode = None
        start_time = time.time()
        
        print("Scanning... Press 'q' to cancel.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Decode barcodes
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                found_barcode = obj.data.decode('utf-8')
                
                # Draw rectangle
                points = obj.polygon
                if len(points) == 4:
                    pts = points
                else:
                    pts = cv2.convexHull(points)
                # cv2.polylines(frame, [pts], True, (0, 255, 0), 3) # Requires numpy, skip drawing if possible or install numpy
                
                # We found one, break immediately
                break
            
            # Show the frame
            cv2.imshow("Barcode Scanner - Press 'q' to cancel", frame)
            
            if found_barcode:
                break

            # Exit on 'q' or timeout (e.g. 30 secs)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if time.time() - start_time > 30:
                print("Scan timed out.")
                break

        cap.release()
        cv2.destroyAllWindows()
        return found_barcode
