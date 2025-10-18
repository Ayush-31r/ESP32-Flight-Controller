import socket

ESP32_IP = "192.168.4.1"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_command(cmd):
    sock.sendto(cmd.encode(), (ESP32_IP, UDP_PORT))
    print(f"Sent: {cmd}")

# Interactive menu

while True:
    print("\n=== ESC Calibration Menu ===")
    print("1. Start calibration (CALSTART)")
    print("2. Stop calibration (CALSTOP)")
    print("3. Test all motors at 1100µs")
    print("4. Test all motors at 1200µs")
    print("5. Test Motor 1 at 1150µs")
    print("6. Stop all motors (STOP)")
    print("7. Check status (STATUS)")
    print("0. Exit")
    
    choice = input("\nEnter choice: ")
    
    if choice == "1":
        send_command("CALSTART")
    elif choice == "2":
        send_command("CALSTOP")
    elif choice == "3":
        send_command("TEST,1100")
    elif choice == "4":
        send_command("TEST,1200")
    elif choice == "5":
        send_command("TESTM1,1150")
    elif choice == "6":
        send_command("STOP")
    elif choice == "7":
        send_command("STATUS")
    elif choice == "0":
        send_command("STOP")
        break

sock.close()