import random
import string
from datetime import datetime

class GameEngine:
    def __init__(self):
        self.xp = 0
        self.level = 1
        self.log = []
        self.tasks = self.generate_tasks()

    def generate_tasks(self):
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        companies = ["CyberCorp", "NetLogic", "HostHero", "SecureNet"]
        ports_services = {"22": "SSH", "21": "FTP", "80": "HTTP", "443": "HTTPS", "3306": "MySQL"}
        tasks = {}

        for i in range(1, 6):
            full_name = random.choice(names) + " " + random.choice(["Smith", "Lee", "Johnson", "Nguyen"])
            username = full_name.lower().replace(" ", ".")
            domain = f"{username.split('.')[0]}.com"
            hostname = f"{username.split('.')[0]}.{random.choice(['net', 'com', 'org'])}"
            ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
            scan_path = f"/home/{username}/public_html"
            restore_path = f"/backups/{username}/"
            email = f"{username}@{domain}"
            company = random.choice(companies)

            tool = random.choice([
                "Password Reset", "DNS Editor", "Malware Scanner",
                "Firewall Console", "DDoS Mitigator", "Backup/Restore"
            ])

            account = {
                "full_name": full_name,
                "username": username,
                "email": email,
                "company": company,
                "ip": ip,
                "hostname": hostname,
                "scan_path": scan_path,
                "restore_path": restore_path
            }

            if tool == "Firewall Console":
                ports = random.sample(list(ports_services.keys()), k=random.randint(1, 2))
                account["ports"] = ports
                services = [ports_services[p] for p in ports]
                account["notes"] = f"Please allow access for {' and '.join(services)} (ports {', '.join(ports)})."
            elif tool == "DDoS Mitigator":
                targets = [ip, hostname, domain]
                account["targets"] = targets
                account["notes"] = f"We're seeing a major spike on {random.choice(targets)}. Please mitigate immediately."
            elif tool == "DNS Editor":
                account["notes"] = f"Customer needs DNS updated for {hostname} to point to {ip}."
            elif tool == "Malware Scanner":
                account["notes"] = f"Scan the directory {scan_path} for malware."
            elif tool == "Password Reset":
                account["notes"] = f"Customer forgot their password. Reset login for {username}."
            elif tool == "Backup/Restore":
                account["notes"] = f"Customer needs files restored from backup path {restore_path}."

            tasks[f"TASK-{i}"] = {
                "name": tool,
                "tool_required": tool,
                "account": account,
                "completed": False,
                "level": random.randint(1, 3),
                "xp": random.choice([10, 15, 20, 25])
            }

        return tasks

    def complete_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["completed"] = True
            self.xp += self.tasks[task_id]["xp"]
            self.level = 1 + self.xp // 100

    def log_event(self, message):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log.append(f"{timestamp} {message}")
        if len(self.log) > 100:
            self.log.pop(0)

    def to_dict(self):
        return {
            "xp": self.xp,
            "level": self.level,
            "log": self.log,
            "tasks": self.tasks
        }

    def from_dict(self, data):
        self.xp = data["xp"]
        self.level = data["level"]
        self.log = data["log"]
        self.tasks = data["tasks"]
