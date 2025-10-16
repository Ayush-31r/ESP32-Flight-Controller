# pid_tuner.py (for Angle PID tuning)
import tkinter as tk
from tkinter import ttk
import socket

# --- Configuration ---
ESP32_IP = "192.168.4.1"
UDP_PORT = 1234

# --- PID Names (Angle Mode Only) ---
pid_names = [
    "Pitch & Roll Angle P",
    "Pitch & Roll Angle I",
    "Pitch & Roll Angle D",
    "Yaw Angle P",
    "Yaw Angle I",
    "Yaw Angle D"
]

# Default values matching your code
default_values = ["2.0", "0.0", "0.007", "2.0", "0.0", "0.007"]

# --- Setup UDP Socket ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ESP32_IP, UDP_PORT)
print(f"✅ PID Tuner started. Will send data to {ESP32_IP}:{UDP_PORT}")

# --- GUI Functions ---
def send_pid_values():
    """Gathers values from text fields and sends them over UDP."""
    try:
        # Get Pitch & Roll Angle PID values (indices 0-2)
        pitch_roll_p = float(entries[0].get())
        pitch_roll_i = float(entries[1].get())
        pitch_roll_d = float(entries[2].get())
        
        # Get Yaw Angle PID values (indices 3-5)
        yaw_p = float(entries[3].get())
        yaw_i = float(entries[4].get())
        yaw_d = float(entries[5].get())
        
        # Send Pitch & Roll Angle PID
        pidangle_str = f"PIDANGLE,{pitch_roll_p:.4f},{pitch_roll_i:.4f},{pitch_roll_d:.4f}"
        sock.sendto(pidangle_str.encode(), server_address)
        print(f"\n📤 Sent: {pidangle_str}")
        
        # Send Yaw Angle PID
        pidyaw_str = f"PIDYAW,{yaw_p:.4f},{yaw_i:.4f},{yaw_d:.4f}"
        sock.sendto(pidyaw_str.encode(), server_address)
        print(f"📤 Sent: {pidyaw_str}")
        
        # Update status label with success style
        status_label.config(
            text="✅ PID values sent successfully!",
            style="Success.TLabel"
        )

    except ValueError:
        print("❌ Error: Invalid input. Please enter numbers only.")
        status_label.config(
            text="❌ Error: Enter valid numbers in all fields.",
            style="Error.TLabel"
        )
        
    except Exception as e:
        print(f"❌ Error sending PID values: {e}")
        status_label.config(
            text=f"❌ Error: {e}",
            style="Error.TLabel"
        )

def reset_to_defaults():
    """Reset all fields to default values."""
    for i, entry in enumerate(entries):
        entry.delete(0, tk.END)
        entry.insert(0, default_values[i])
    status_label.config(
        text="🔄 Reset to default values.",
        style="Info.TLabel"
    )

# --- Create the Main Window ---
root = tk.Tk()
root.title("Drone PID Tuner - Angle Mode")
root.geometry("400x450")

# --- Create Style object and define custom styles ---
style = ttk.Style()
style.configure("Success.TLabel", foreground="green", font=('Helvetica', 10, 'bold'))
style.configure("Error.TLabel", foreground="red", font=('Helvetica', 10, 'bold'))
style.configure("Info.TLabel", foreground="blue", font=('Helvetica', 10))
style.configure("Title.TLabel", font=('Helvetica', 12, 'bold'))
style.configure("Header.TLabel", font=('Helvetica', 10, 'bold'), background='#e0e0e0')

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# --- Title ---
title_label = ttk.Label(
    main_frame,
    text="🚁 Drone PID Tuner",
    style="Title.TLabel"
)
title_label.grid(column=0, row=0, columnspan=2, pady=(0, 10))

# --- Info Label ---
info_label = ttk.Label(
    main_frame,
    text="Rate PID is hard-coded. Tune Angle PID only.",
    font=('Helvetica', 9, 'italic'),
    foreground='#555'
)
info_label.grid(column=0, row=1, columnspan=2, pady=(0, 15))

entries = []
current_row = 2

# --- Pitch & Roll Section ---
section1_label = ttk.Label(
    main_frame,
    text="Pitch & Roll Angle PID",
    style="Header.TLabel",
    padding=(5, 5)
)
section1_label.grid(column=0, row=current_row, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 5))
current_row += 1

for i in range(3):
    ttk.Label(main_frame, text=pid_names[i]).grid(
        column=0, row=current_row, sticky=tk.W, padx=5, pady=5
    )
    entry = ttk.Entry(main_frame, width=15, font=('Helvetica', 10))
    entry.grid(column=1, row=current_row, sticky=tk.W, padx=5, pady=5)
    entry.insert(0, default_values[i])
    entries.append(entry)
    current_row += 1

# --- Yaw Section ---
section2_label = ttk.Label(
    main_frame,
    text="Yaw Angle PID",
    style="Header.TLabel",
    padding=(5, 5)
)
section2_label.grid(column=0, row=current_row, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 5))
current_row += 1

for i in range(3, 6):
    ttk.Label(main_frame, text=pid_names[i]).grid(
        column=0, row=current_row, sticky=tk.W, padx=5, pady=5
    )
    entry = ttk.Entry(main_frame, width=15, font=('Helvetica', 10))
    entry.grid(column=1, row=current_row, sticky=tk.W, padx=5, pady=5)
    entry.insert(0, default_values[i])
    entries.append(entry)
    current_row += 1

# --- Buttons Frame ---
button_frame = ttk.Frame(main_frame)
button_frame.grid(column=0, row=current_row, columnspan=2, pady=20)

send_button = ttk.Button(
    button_frame,
    text="📤 Send to Drone",
    command=send_pid_values
)
send_button.grid(column=0, row=0, padx=5)

reset_button = ttk.Button(
    button_frame,
    text="🔄 Reset Defaults",
    command=reset_to_defaults
)
reset_button.grid(column=1, row=0, padx=5)

# --- Status Label ---
status_label = ttk.Label(
    main_frame,
    text="📝 Adjust values and click 'Send to Drone'.",
    anchor="center",
    style="Info.TLabel"
)
status_label.grid(column=0, row=current_row + 1, columnspan=2, pady=10)


# --- Connection Info ---
conn_label = ttk.Label(
    main_frame,
    text=f"🔗 Connected to {ESP32_IP}:{UDP_PORT}",
    font=('Helvetica', 8),
    foreground='#666'
)
conn_label.grid(column=0, row=current_row + 2, columnspan=2)

# --- Start the GUI Event Loop ---
root.mainloop()

# --- Cleanup ---
print("\n👋 Exiting PID tuner.")
sock.close()