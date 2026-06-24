import time
import cv2
import numpy as np
import mss
import serial

W, H = 160, 80

ser = serial.Serial("COM6", 921600, timeout=1)
time.sleep(2)

with mss.MSS() as sct:
    monitor = sct.monitors[1]

    while True:
        try:
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

            h, w = frame.shape[:2]

            # ---- FIXED STRETCHING: FORCE A PERFECT 2:1 CROP MATRIX ----
            target_w = int(h * (2 / 1))
            if target_w > w:
                target_w = w
                target_h = int(w * (1 / 2))
                y = (h - target_h) // 2
                frame = frame[y:y + target_h, :]
            else:
                x = (w - target_w) // 2
                frame = frame[:, x:x + target_w]

            # ---- FORCE RESIZE TO SCREEN RESOLUTION ----
            frame = cv2.resize(frame, (W, H), interpolation=cv2.INTER_AREA)

            # ---- RGB565 CONVERSION (KEPT MATCHING YOUR CORRECT COLOR MATRIX) ----
            r = (frame[:, :, 0] >> 3).astype(np.uint16)
            g = (frame[:, :, 1] >> 2).astype(np.uint16)
            b = (frame[:, :, 2] >> 3).astype(np.uint16)

            rgb565 = (r << 11) | (g << 5) | b
            raw = rgb565.astype("<u2").tobytes()

            ser.write(b"START")
            ser.write(len(raw).to_bytes(4, "big"))
            ser.write(raw)

            time.sleep(0.03)
            
        except KeyboardInterrupt:
            ser.close()
            break
        except Exception:
            ser.close()
            break