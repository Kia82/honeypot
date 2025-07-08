### Malware Boys 
# 🐍 Honeypot: A Beginner-Friendly Cybersecurity Trap

Welcome to my Honeypot project! This is a lightweight and educational honeypot designed to simulate vulnerable services, log attacker behavior, and help you learn how intrusions happen in the wild.

## 🚀 What Is a Honeypot?

A **honeypot** is a decoy system designed to lure attackers, detect unauthorized access attempts, and gather information about threat actors — all while keeping your real systems safe.

---

## 🛠️ Features

### ✅ Basic Features
- **Service Emulation**: Fake SSH/HTTP/FTP services to mimic real systems.
- **Logging & Monitoring**: Captures IPs, timestamps, commands, and full request data.
- **Deception**: Includes dummy files like `/etc/passwd`, fake credentials, and time delays to appear real.
- **Isolation**: Runs in a container or virtual machine to protect your host system.
- **Alerting**: Notifies on suspicious activity (console-based or optional integrations).
- **Persistence**: Secure logging to local or remote systems for later analysis.

---

## 🧰 Tech Stack

| Feature              | Tool/Language     |
|----------------------|------------------|
| Service Emulation    | Python (`socket`, `http.server`) |
| Logging              | Python `logging` module |
| Containerization     | Docker |
| Monitoring           | JSON log files |
| Isolation            | iptables / Docker networking |

---

## 🧠 Future Improvements

- 🌍 Geolocate attacker IPs
- 📁 Trap malicious file uploads
- 🐚 Detect reverse shell attempts
- 🔒 Encrypt and ship logs to S3 or remote servers
- 🚫 Auto-block repeated intrusions by IP

---

## ⚠️ Security Notice

**⚠️ Never run a honeypot on a production or personal machine.**  
Always isolate it in a **VM**, **container**, or behind strict **firewall rules**. Honeypots attract real attackers.

---

## 🏁 Getting Started

```bash
# Clone this repo
git clone https://github.com/Kia82/malware-boys-pentesting.git
cd honeypot

# Run the honeypot
cd honeypot
python3 honeypot.py
```

## 🗂️ Package Structure

```
honeypot/
│
├── honeypot/                  # Core package
│   ├── __init__.py
│   ├── main.py                # Entry point
│   ├── config.py              # Config loader (ports, services, flags)
│   ├── logger.py              # Logging setup
│   ├── alert.py               # Alerting logic (email, webhook)
│   │
│   ├── services/              # Each protocol honeypot in its own module
│   │   ├── __init__.py
│   │   ├── ssh.py             # Fake SSH server
│   │   ├── http.py            # Fake HTTP server
│   │   └── ftp.py             # Fake FTP server
│   │   
│   └── utils/
│       ├── isolation.py       # Docker/VPN/firewall helpers
│       └── geoip.py           # IP geolocation
│
├── logs/                      # Structured logs stored here
│   └── ...
│
├── data/                      # Dummy payloads, fake files (e.g. /etc/passwd)
│   └── fake_passwd.txt
│
├── Dockerfile                 # Containerized deployment
├── requirements.txt           # Dependencies
├── README.md                  # Project overview
└── run.py                     # Thin wrapper for CLI entry

```