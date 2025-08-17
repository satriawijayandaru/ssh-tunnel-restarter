import os
import subprocess
import paramiko
from dotenv import load_dotenv
import time
from datetime import datetime


print = lambda *args, **kwargs: __builtins__.print(*args, **{**kwargs, "flush": True})


load_dotenv()

monitor_ip = os.getenv("MONITOR_IP")
ports = [int(p.strip()) for p in os.getenv("PORTS", "").split(",") if p.strip()]

ssh_host = os.getenv("SSH_HOST")
ssh_user = os.getenv("SSH_USER")
ssh_pass = os.getenv("SSH_PASS")
ssh_port = int(os.getenv("SSH_PORT", 22))

interval = int(os.getenv("INTERVAL", 60))


def log(msg):
    """Log with timestamp"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def check_port(ip, port):
    """Check if a port is open using nc (netcat). Returns True if open, False if closed."""
    try:
        result = subprocess.run(
            ["nc", "-zv", ip, str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def reload_supervisor(ip, ssh_port, username, password):
    """SSH into server and reload supervisor."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=ssh_port, username=username, password=password)

        stdin, stdout, stderr = client.exec_command("sudo supervisorctl reload")
        log("Supervisorctl reload executed.")
        log("Output: " + stdout.read().decode().strip())
        err = stderr.read().decode().strip()
        if err:
            log("Error: " + err)
        client.close()
    except Exception as e:
        log(f"SSH connection failed: {e}")


def main():
    while True:
        closed_ports = []
        for port in ports:
            if check_port(monitor_ip, port):
                log(f"Port {port} on {monitor_ip} is OPEN")
            else:
                log(f"Port {port} on {monitor_ip} is CLOSED")
                closed_ports.append(port)

        if closed_ports:
            log(f"[!] Closed ports detected: {closed_ports}")
            reload_supervisor(ssh_host, ssh_port, ssh_user, ssh_pass)
        else:
            log(f"[✓] All monitored ports on {monitor_ip} are open.")

        log(f"Sleeping for {interval} seconds...\n")
        time.sleep(interval)


if __name__ == "__main__":
    main()
