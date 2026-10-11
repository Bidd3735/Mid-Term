
import socket
from datetime import datetime

COMMON_PORTS = [21, 22, 80, 443]


def scan_port(host, port, timeout=0.5):
    """Return True if a TCP connection to the port succeeds."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except (socket.gaierror, OSError):
        return False


def scan_ports(host, ports):
    """Scan the specified TCP ports and report open ports."""
    print(f"\nScanning {host}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 45)

    open_ports = []

    for port in ports:
        print(f"Checking port {port}...", end=" ")

        if scan_port(host, port):
            print("OPEN")
            open_ports.append(port)
        else:
            print("CLOSED or FILTERED")

    print("-" * 45)
    print(f"Scan complete. Open ports: {open_ports}")
    return open_ports


def parse_port_list(text):
    """Convert comma-separated port numbers into a sorted list."""
    ports = sorted(set(int(item.strip()) for item in text.split(",")))

    if not ports or any(port < 1 or port > 65535 for port in ports):
        raise ValueError("Ports must be between 1 and 65535.")

    return ports


def main():
    while True:
        print("\n===== Python Port Scanner =====")
        print("1. Scan common ports on localhost")
        print("2. Scan a custom port range on localhost")
        print("3. Scan selected ports on scanme.nmap.org")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        try:
            if choice == "1":
                scan_ports("127.0.0.1", COMMON_PORTS)

            elif choice == "2":
                start = int(input("Enter starting port: "))
                end = int(input("Enter ending port: "))

                if not (1 <= start <= end <= 65535):
                    print("Invalid range. Use ports 1-65535.")
                    continue

                if end - start > 4999:
                    print("Please scan no more than 5000 ports per run.")
                    continue

                scan_ports("127.0.0.1", range(start, end + 1))

            elif choice == "3":
                print("Scanning the authorized Nmap practice host.")
                ports = parse_port_list(
                    input("Enter selected ports (e.g., 22,80,443): ")
                )
                scan_ports("scanme.nmap.org", ports)

            elif choice == "4":
                print("Port scanner closed.")
                break

            else:
                print("Invalid choice. Select 1, 2, 3, or 4.")

        except ValueError as error:
            print(f"Invalid input: {error}")

        except KeyboardInterrupt:
            print("\nScan interrupted.")

            
if __name__ == "__main__":
    main()
    