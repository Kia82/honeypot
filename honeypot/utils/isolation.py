import subprocess
import os

def apply_firewall_rules():
    # Apply firewall rules using iptables
    rules = [
        "iptables -P OUTPUT DROP", # Drop all outgoing traffic by default
        "iptables -A OUTPUT -p udp --dport 53 -j ACCEPT", # Allow DNS queries
        "iptables -A INPUT -p tcp --dport 22 -j ACCEPT", # Allow SSH traffic
        "iptables -A INPUT -p tcp --dport 80 -j ACCEPT", # Allow HTTP traffic
        "iptables -A INPUT -p tcp --dport 21 -j ACCEPT" # Allow FTP traffic
    ]
    for rule in rules:
        try:
            subprocess.run(rule.split(), check=True)
            print(f"[*] Applied rule: {rule}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to apply rule: {rule}. Error: {e}")

# Function to block a specific IP address
# Call this function in alerting system
def block_ip(ip):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check = True)
        print(f"[*] Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to block IP: {ip}. Error: {e}")

# Check if the script is running as root
def is_root():
    return os.geteuid() == 0

# Function to create a Docker network for isolation
# This function can be called to set up a network for the honeypot
def create_docker_network(network_name = "honeynet"):
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={network_name}", "--format", "{{.Name}}"],
            stdout=subprocess.PIPE,
            text=True)
        if result.stdout.strip() == network_name:
            print(f"[*] Docker network '{network_name}' already exists.")
        else:
            subprocess.run(["docker", "network", "create", "--driver", "bridge", network_name], check=True)
            print(f"[*] Created Docker network: {network_name}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to create Docker network '{network_name}'. Error: {e}")

if __name__ == "__main__":
    if is_root():
        print("[*] Running isolation setup...")
        print("[*] Setting up Docker network...")
        create_docker_network()
        print("[*] Applying firewall rules...")
        apply_firewall_rules()
    else:
        print("[!] This script must be run as root (try sudo).")