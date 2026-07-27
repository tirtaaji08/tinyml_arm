import serial
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque

# ================= KONFIGURASI =================
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 921600
WINDOW_SIZE = 300  # jumlah sampel raw yang ditampilkan (~6 detik di 50Hz)

# ================= INISIALISASI =================
raw_data = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

# Variabel untuk menyimpan data terakhir
current_bpm = 0.0
total_cycles = 0
active_cycles = 0
idle_cycles = 0

# Setup Serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"Terhubung ke {SERIAL_PORT}")
except Exception as e:
    print(f"Gagal konek ke serial: {e}")
    exit()

# Setup Matplotlib – dua subplot: atas grafik, bawah info
fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor('#1a1a2e')

# --- Subplot Atas: Gelombang PPG ---
ax1 = plt.subplot(2, 1, 1)
ax1.set_facecolor('#16213e')
ax1.set_title('Photoplethysmogram (PPG) Real-time', color='white', fontsize=14)
ax1.set_xlabel('Sampel ke-', color='#a0aec0')
ax1.set_ylabel('Amplitude (A.U.)', color='#a0aec0')
ax1.tick_params(colors='#a0aec0')
ax1.grid(True, color='#a0aec0', linestyle='--', alpha=0.3)
line, = ax1.plot(range(WINDOW_SIZE), [0]*WINDOW_SIZE, color='#00ffcc', linewidth=2)

# --- Subplot Bawah: Angka BPM + Info Cycle ---
ax2 = plt.subplot(2, 1, 2)
ax2.axis('off')  # matikan sumbu

# Teks BPM besar di tengah
bpm_text = ax2.text(0.5, 0.65, '-- BPM', 
                    ha='center', va='center', 
                    fontsize=70, color='#e0ffff', 
                    fontweight='bold', family='monospace')

# Teks info cycle di bawah (lebih kecil)
cycle_text = ax2.text(0.5, 0.2, ' Total Cycles: -- ', 
                      ha='center', va='center', 
                      fontsize=16, color='#88ccff', 
                      family='monospace')

# Tambahan info koneksi di pojok
fig.text(0.02, 0.98, f'Connected to {SERIAL_PORT} @ {BAUDRATE} baud', 
         color='gray', fontsize=10, verticalalignment='top')

# ================= FUNGSI UPDATE =================
def update_plot(frame):
    global current_bpm, total_cycles, active_cycles, idle_cycles, raw_data

    # Baca semua data yang tersedia di buffer serial
    while ser.in_waiting > 0:
        try:
            line_raw = ser.readline().decode('utf-8').strip()
        except UnicodeDecodeError:
            continue

        if not line_raw:
            continue

        # Parsing data RAW
        if line_raw.startswith('R:'):
            try:
                value = float(line_raw.split(':')[1])
                raw_data.append(value)
            except ValueError:
                pass

        # Parsing data lengkap
        elif line_raw.startswith('B:'):
            try:
                # Pisahkan berdasarkan ';'
                parts = line_raw.split(';')
                for part in parts:
                    if part.startswith('B:'):
                        current_bpm = float(part.split(':')[1])
                    elif part.startswith('T:'):
                        total_cycles = int(part.split(':')[1])
                
                # Update teks BPM dan Cycle
                bpm_text.set_text(f'{current_bpm:.0f} BPM')
                cycle_text.set_text(f'Total Cycles: {total_cycles}')
            except (ValueError, IndexError):
                pass

    # Update garis grafik
    if len(raw_data) == WINDOW_SIZE:
        line.set_ydata(list(raw_data))
    else:
        temp_list = list(raw_data)
        if len(temp_list) < WINDOW_SIZE:
            temp_list = [0] * (WINDOW_SIZE - len(temp_list)) + temp_list
        line.set_ydata(temp_list)

    # Auto-scale Y
    if len(raw_data) > 10:
        max_val = max(raw_data)
        min_val = min(raw_data)
        range_val = max_val - min_val
        if range_val < 1:
            range_val = 1
        ax1.set_ylim(min_val - range_val*0.1, max_val + range_val*0.1)

    return line, bpm_text, cycle_text

# ================= JALANKAN =================
ani = animation.FuncAnimation(fig, update_plot, interval=20, blit=True, save_count=100)
plt.tight_layout()
plt.show()

# Tutup serial saat program di-close
ser.close()