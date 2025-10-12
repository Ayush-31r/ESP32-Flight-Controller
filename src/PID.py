# pid_tuner.py (with text fields and style fix)
import tkinter as tk
from tkinter import ttk
import socket

# --- Configuration ---
ESP32_IP = "192.168.4.1"
UDP_PORT = 1234

# --- PID Names ---
pid_names = ["Pitch Angle P", "Roll Angle P",
             "Pitch Rate P", "Pitch Rate I", "Pitch Rate D",
             "Roll Rate P", "Roll Rate I", "Roll Rate D",
             "Yaw Rate P", "Yaw Rate I", "Yaw Rate D"]

# --- Setup UDP Socket ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ESP32_IP, UDP_PORT)
print(f"✅ PID Tuner started. Will send data to {ESP32_IP}:{UDP_PORT}")

# --- GUI Functions ---
def send_pid_values():
    """Gathers values from all text fields and sends them over UDP."""
    current_pid_values = []
    try:
        for entry in entries:
            value_str = entry.get()
            if not value_str:
                value_str = "0.0"
            current_pid_values.append(float(value_str))

        pid_str = "PID," + ",".join(f"{val:.4f}" for val in current_pid_values)
        sock.sendto(pid_str.encode(), server_address)
        print("\nPID values sent:")
        print(pid_str)
        
        # --- STYLE FIX ---
        # Apply the 'Success.TLabel' style (green text)
        status_label.config(text="PID values sent successfully!", style="Success.TLabel")

    except ValueError:
        print("❌ Error: Invalid input. Please enter numbers only.")
        # --- STYLE FIX ---
        # Apply the 'Error.TLabel' style (red text)
        status_label.config(text="Error: Enter valid numbers in all fields.", style="Error.TLabel")
        
    except Exception as e:
        print(f"❌ Error sending PID values: {e}")
        # --- STYLE FIX ---
        # Apply the 'Error.TLabel' style (red text)
        status_label.config(text=f"Error: {e}", style="Error.TLabel")

# --- Create the Main Window ---
root = tk.Tk()
root.title("Drone PID Tuner")

# --- STYLE FIX: Create a Style object and define custom styles ---
style = ttk.Style()
# Style for successful messages (green text)
style.configure("Success.TLabel", foreground="green")
# Style for error messages (red text)
style.configure("Error.TLabel", foreground="red")


main_frame = ttk.Frame(root, padding="15")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

entries = []

# --- Create a Label and a Text Field for Each PID Value ---
for i, name in enumerate(pid_names):
    ttk.Label(main_frame, text=name).grid(column=0, row=i, sticky=tk.W, padx=5, pady=5)
    entry = ttk.Entry(main_frame, width=12, font=('Helvetica', 10))
    entry.grid(column=1, row=i, sticky=tk.W, padx=5, pady=5)
    entry.insert(0, "0.0")
    entries.append(entry)

# --- Send Button and Status Label ---
send_button = ttk.Button(main_frame, text="Send PID Values to Drone", command=send_pid_values)
send_button.grid(column=0, row=len(pid_names), columnspan=2, pady=20)

status_label = ttk.Label(main_frame, text="Adjust values and click send.", anchor="center")
status_label.grid(column=0, row=len(pid_names) + 1, columnspan=2)

# --- Start the GUI Event Loop ---
root.mainloop()

# --- Cleanup ---
print("\nExiting PID tuner.")
sock.close()