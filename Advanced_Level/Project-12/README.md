# 🔍 Network Scanner

> TCP port scanner built with raw socket programming · concurrent scanning · banner grabbing · Google Colab

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Sockets](https://img.shields.io/badge/stdlib-socket-4B8BBE?style=flat-square)
![Colab](https://img.shields.io/badge/Run%20on-Google%20Colab-F9AB00?style=flat-square&logo=googlecolab)

---

## ⚠️ Legal & ethical use

Only scan hosts and networks **you own, or have explicit written permission to test**. Unauthorized scanning can violate laws like the U.S. Computer Fraud and Abuse Act (and equivalents elsewhere) and most providers' acceptable use policies, even without causing damage. This project defaults to `127.0.0.1` and includes an authorization prompt before every scan — it's built as a socket-programming learning exercise, not a tool for scanning infrastructure you don't control.

---

## 🚀 Features

- **TCP Connect Scanning** — full 3-way handshake per port using nothing but Python's built-in `socket` module
- **Concurrent Scanning** — a thread pool scans up to 100 ports in parallel instead of one at a time
- **Banner Grabbing** — captures service greetings (FTP, SSH, SMTP, etc.) from open ports where available
- **Common Ports Database** — 20+ well-known ports mapped to their typical services out of the box
- **Custom Port Ranges** — scan any range (e.g. 1–1024) instead of just the common list
- **Multi-Host Sweeps** — check one specific port across a small list of hosts on a subnet you own
- **Authorization Gate** — an explicit yes/no confirmation before any scan runs, as a guard against accidental misuse
- **JSON Reports** — exports scan results (open ports, services, banners) to a structured file
- **Zero Local Setup** — runs entirely inside one Colab notebook, nothing to install on your machine

---

## 📁 Project Structure

```
network_scanner/
├── Network_Scanner.ipynb    # The entire project — one notebook, run top to bottom
└── README.md
```

Since this is built specifically to run in Google Colab, it's structured as a single notebook rather than a package of scripts. Each section below corresponds to a group of cells inside it:

```
Network_Scanner.ipynb
├── 1. Imports                    # socket, concurrent.futures, ipaddress
├── 2. confirm_authorization()    # explicit yes/no gate before scanning
├── 3. Port lists                 # COMMON_PORTS map + port_range() helper
├── 4. scan_port() + grab_banner()   # single-port TCP connect + banner read
├── 5. scan_target()              # threaded scan across many ports
├── 6. Run a scan                 # default: 127.0.0.1, common ports
├── 7. sweep_hosts()              # check one port across multiple hosts
└── 8. save_report()              # export results to scan_report.json
```

---

## ⚙️ Setup

```bash
# 1. Open the notebook in Google Colab
# (upload Network_Scanner.ipynb, or open it directly from Drive/GitHub)

# 2. No installs needed — everything used is Python's standard library
```

No API keys, accounts, or third-party packages required.

---

## ▶️ Usage

All usage happens by running notebook cells in order, no command line involved.

```python
# Scan the default target (your own Colab VM) on common ports
TARGET = "127.0.0.1"
confirm_authorization(TARGET)
results = scan_target(TARGET, list(COMMON_PORTS.keys()), timeout=0.5)

# Scan a custom port range instead
results = scan_target(TARGET, port_range(1, 1024), timeout=0.3)

# Sweep several hosts on one port (only hosts you control)
hosts = [str(ip) for ip in ipaddress.ip_network('192.168.1.0/29').hosts()]
sweep_hosts(hosts, port=80)

# Save results to a JSON report
save_report(TARGET, results)
```

### Key settings

| Setting        | Default        | Description                                              |
|-----------------|-----------------|-------------------------------------------------------------|
| `TARGET`         | `127.0.0.1`     | Host to scan — change only for hosts you're authorized to test |
| `timeout`        | `0.5`           | Seconds to wait per port before marking it closed/filtered  |
| `max_workers`    | `100`           | Thread pool size for concurrent scanning                    |
| `COMMON_PORTS`   | 20+ entries     | Port → service name mapping used for reporting              |

---

## 📊 Output Files

```
scan_report.json      # target, timestamp, and every open port + service + banner found
```

---

## ⚠️ Disclaimer

> This project is for **educational purposes only** — a hands-on introduction to how port scanning works at the socket level.
> Colab's sandboxed VM has its own network restrictions and shared IP ranges, so scanning arbitrary external hosts from Colab may also violate Google's terms of service. Stick to `localhost`, a host on a network you control, or an intentionally vulnerable practice target (e.g. a local `Metasploitable`/`DVWA` VM or a sanctioned CTF range).

For real-world security assessments, a purpose-built and properly authorized tool like `nmap` is far more capable than this notebook.

---

## 📄 License

AGPL-3.0 License — see [LICENSE](LICENSE)