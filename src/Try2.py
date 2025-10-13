import pygame
import socket
import time

# --- Configuration ---
ESP32_IP = "192.168.4.1"  # The IP of your ESP32 hotspot
UDP_PORT = 1234
CONTROLLER_DEADZONE = 0.15 # Helps prevent drift from worn-out joysticks

# --- Setup UDP Socket ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ESP32_IP, UDP_PORT)
print(f"✅ UDP client started. Will send data to {ESP32_IP}:{UDP_PORT}")

# --- Initialize Pygame and find the Joystick ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No controller detected! Please connect an Xbox controller and restart the script.")
    exit()

controller = pygame.joystick.Joystick(0)
controller.init()
print(f"✅ Controller '{controller.get_name()}' detected.")
print("\n--- Controls ---")
print("🕹️ Left Stick UP/DOWN: Throttle")
print("🔘 X Button: Run sequential motor test (first-time only)")
print("🔘 Menu Button: ARM/DISARM toggle")
print("----------------")
print("Press Ctrl+C in this window to exit.")


def map_range(x, in_min, in_max, out_min, out_max):
    """A helper function to map a value from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

try:
    # This is the main loop that runs continuously
    while True:
        # Pygame reads all controller events
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Menu button (button 7) for ARM/DISARM toggle
                if event.button == 7:
                    print("\nMENU BUTTON PRESSED - Toggling Arm State")
                    message = "SWITCH"
                    sock.sendto(message.encode(), server_address)
                
                # 'X' button (button 2) for Sequential Motor Test
                if event.button == 2:
                    print("\n'X' BUTTON PRESSED - Running Sequential Motor Test")
                    message = "X"
                    sock.sendto(message.encode(), server_address)

        # --- Read Joystick and Apply Throttle Logic ---
        left_stick_y = controller.get_axis(1)
        throttle = 1000

        if left_stick_y < -CONTROLLER_DEADZONE:
            throttle = map_range(left_stick_y, 0.0, -1.0, 1000, 2000)
        
        pitch_val, roll_val, yaw_val = 0, 0, 0

        # --- Format and Send the UDP Packet ---
        control_message = f"C,{throttle},{pitch_val},{roll_val},{yaw_val}"
        sock.sendto(control_message.encode(), server_address)

        print(f"\rThrottle: {throttle} | Sending: '{control_message}'   ", end="")
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nExiting controller script. Sending disarm signal...")
    
finally:
    sock.sendto(b"C,1000,0,0,0", server_address)
    sock.close()
    pygame.quit()