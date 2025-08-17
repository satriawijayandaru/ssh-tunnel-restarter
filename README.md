  # Port Checker with Supervisor Reload  

This project provides a Python script packaged in Docker that:  
- Periodically checks whether specific ports on a target server are open.  
- If **any port is closed**, it connects via SSH to the server and runs `supervisorctl reload`.  
- Runs as a long-lived container controlled via Docker Compose.  

---

## 📦 Features
- Configurable via `.env` file  
- Logs port status with timestamps (open/closed)  
- Reloads supervisor **only when needed**  
- Auto-restart container with Docker Compose  

---

## ⚙️ Requirements
- Docker & Docker Compose installed  
- Target server running `supervisord`  
- SSH access from the container to the target server  

---

## 🚀 Setup

### 1. Clone project
```bash
git clone https://github.com/satriawijayandaru/ssh-tunnel-restarter.git
cd port-checker
```
### 2. Configure .env
⚠️ If your supervisord requires root, allow your SSH user to run supervisorctl without password:
```bash
echo "myuser ALL=(ALL) NOPASSWD: /usr/bin/supervisorctl" | sudo tee /etc/sudoers.d/99-supervisor

```
### 3. Simply run the compose file
```bash
docker compose up -d
```
