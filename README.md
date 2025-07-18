# ARP Spoofing Script

This tool performs ARP spoofing between a **target** and the **gateway** (router) to intercept packets.

> ⚠️ This tool is for educational purposes only. Do not use it on unauthorized networks.

## 🧠 What It Does

It sends spoofed ARP replies to a target and the router, tricking both into thinking the attacker is the other. This allows for a man-in-the-middle (MITM) attack.

## 🚀 Usage

```bash
sudo python3 spoof.py <target_ip> <router_ip>
```

Example:
```bash
sudo python3 spoof.py 192.168.0.104 192.168.0.1
```

## 🛠 Requirements

- Python 3.x
- Scapy

Install Scapy:
```bash
pip install scapy
```

## 📂 File Structure

- `spoof.py` → The main ARP spoofing script.

## 📌 Notes

- Make sure IP forwarding is enabled (required for packet forwarding):
  ```bash
  echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
  ```
- You can stop the attack anytime with `CTRL+C`.

## 🧠 Analysis

- `sudo python3 analysis.py` for anlaysis your attack
