import random
import string

class GameEngine:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.tasks = {}
        self.task_id_counter = 1
        self.logs = []
        self.tool_types = [
            "Password Reset", "DNS Editor", "Malware Scanner",
            "Firewall Console", "DDoS Mitigator", "Backup/Restore"
        ]
        self.first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
        self.last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        self.companies = ["CyberX", "NetSecure", "CloudTech", "DataSafe", "Virtux", "ProxyFlare", "NeuroHost", "GridOps"]
        self.generate_tasks()

    def generate_username(self, first, last):
        return f"{first[0].lower()}{last.lower()}"

    def generate_task_notes(self, tool, username, hostname, ip, scan_path, restore_path):
        return {
            "Password Reset": f"User {username} is locked out and needs a password reset immediately.",
            "DNS Editor": f"DNS record for {hostname} is incorrect and must be updated to IP {ip}.",
            "Malware Scanner": f"The system at {scan_path} is acting strange. Perform a malware scan.",
            "Firewall Console": f"User {username} reported blocked service. Adjust firewall to allow correct port.",
            "DDoS Mitigator": f"{hostname} is under heavy traffic—check for signs of DDoS and mitigate.",
            "Backup/Restore": f"Critical data loss on {hostname}. Restore from backup in {restore_path}."
        }.get(tool, "No task notes provided.")

    def generate_tasks(self):
        self.tasks = {}
        self.task_id_counter = 1
        for _ in range(5):
            first = random.choice(self.first_names)
            last = random.choice(self.last_names)
            company = random.choice(self.companies)
            username = self.generate_username(first, last)
            email = f"{username}@{company.lower()}.com"
            ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
            hostname = f"{username}.{company.lower()}.com"
            scan_path = f"/home/{username}/scan"
            restore_path = f"/home/{username}/backup"
            tool = random.choice(self.tool_types)
            notes = self.generate_task_notes(tool, username, hostname, ip, scan_path, restore_path)

            task = {
                "title": f"{tool} (T{self.tool_types.index(tool) + 1})",
                "completed": False,
                "tool_required": tool,
                "account": {
                    "name": f"{first} {last}",
                    "email": email,
                    "username": username,
                    "company": company,
                    "ip": ip,
                    "hostname": hostname,
                    "scan_path": scan_path,
                    "restore_path": restore_path,
                    "notes": notes
                }
            }
            self.tasks[f"task{self.task_id_counter}"] = task
            self.task_id_counter += 1

    def complete_task(self, task_id):
        if task_id in self.tasks and not self.tasks[task_id]["completed"]:
            self.tasks[task_id]["completed"] = True
            tool = self.tasks[task_id]["tool_required"]
            xp_gain = (self.tool_types.index(tool) + 1) * 5 + 5
            self.xp += xp_gain
            if self.xp >= 100:
                self.level += 1
                self.xp = 0

    def log_event(self, message):
        self.logs.insert(0, f"[{self.current_time()}] {message}")
        self.logs = self.logs[:10]

    def current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "level": self.level,
            "xp": self.xp,
            "tasks": self.tasks,
            "logs": self.logs
        }

    def from_dict(self, data):
        self.level = data.get("level", 1)
        self.xp = data.get("xp", 0)
        self.tasks = data.get("tasks", {})
        self.logs = data.get("logs", [])
