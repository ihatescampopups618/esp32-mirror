import time
import cv2
import numpy as np
import mss
import serial
import ctypes
from ctypes import wintypes

# ---- HIGH-SPEED WINDOWS CURSOR STRUCTURES ----
class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

class CURSORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hCursor", wintypes.HANDLE),
        ("ptScreenPos", POINT)
    ]

def get_mouse_pos():
    cursor_info = CURSORINFO()
    cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
    if ctypes.windll.user32.GetCursorInfo(ctypes.byref(cursor_info)):
        if cursor_info.flags == 1: # 1 means the cursor is visible/active
            return cursor_info.ptScreenPos.x, cursor_info.ptScreenPos.y
    return None

# ---- SCREEN & DISPLAY CONFIGURATION ----
W, H = 160, 80
ser = serial.Serial("COM6", 921600, timeout=1)
time.sleep(2)

with mss.MSS() as sct:
    monitor = sct.monitors[1]

    while True:
        try:
            # Grab the raw desktop frame buffer
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            h, w = frame.shape[:2]

            # ---- INJECT HARDWARE CURSOR ----
            pos = get_mouse_pos()
            if pos is not None:
                mx, my = pos
                # Check if the cursor is within the current monitor bounds
                if 0 <= mx < w and 0 <= my < h:
                    # Draw a solid bright red circle where your cursor is pointing
                    cv2.circle(frame, (mx, my), 12, (255, 0, 0), -1)

            # ---- PERFECT 2:1 CROP MATRIX (Your stable cropping code) ----
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

            # ---- RGB565 HIGH-SPEED TRANSFORMATION ----
            r = (frame[:, :, 0] >> 3).astype(np.uint16)
            g = (frame[:, :, 1] >> 2).astype(np.uint16)
            b = (frame[:, :, 2] >> 3).astype(np.uint16)

            rgb565 = (r << 11) | (g << 5) | b
            raw = rgb565.astype("<u2").tobytes()

            # ---- WRITE PACKET FRAMES ----
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