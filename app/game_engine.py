import time
import threading
import random

class GameEngine:
    def __init__(self):
        self.xp = 0
        self.level = 1
        self.tasks = {}
        self.task_counter = 1
        self.lock = threading.Lock()
        self.generate_initial_tasks()
        self.running = True
        # Start background threads for task escalation and auto-generation
        threading.Thread(target=self.simulate_escalation, daemon=True).start()
        threading.Thread(target=self.auto_generate_tasks, daemon=True).start()

    def generate_initial_tasks(self):
        # Initial tasks available at level 1 and 2
        self.add_task("Reset user password (T1)", xp=10, level_required=1, escalation_time=60)
        self.add_task("Edit DNS settings (T1)", xp=15, level_required=1, escalation_time=90)
        self.add_task("Run malware scan (T2)", xp=20, level_required=2, escalation_time=120)

    def add_task(self, description, xp, level_required, escalation_time):
        with self.lock:
            task_id = f"task{self.task_counter}"
            self.task_counter += 1
            self.tasks[task_id] = {
                "description": description,
                "xp": xp,
                "level_required": level_required,
                "completed": False,
                "time_created": time.time(),
                "escalation_time": escalation_time,
                "escalated": False
            }

    def complete_task(self, task_id):
        with self.lock:
            task = self.tasks.get(task_id)
            if task and not task["completed"]:
                task["completed"] = True
                xp_reward = task["xp"]
                self.xp += xp_reward
                self.check_level_up()
                return xp_reward
            return 0

    def check_level_up(self):
        new_level = (self.xp // 50) + 1
        if new_level > self.level:
            self.level = new_level
            # Unlock new tasks based on level advancement
            if self.level == 2:
                self.add_task("Configure Firewall rules (T2+)", xp=25, level_required=2, escalation_time=150)
            elif self.level == 3:
                self.add_task("Mitigate DDoS attack (T3+)", xp=30, level_required=3, escalation_time=180)
            elif self.level == 4:
                self.add_task("Perform Backup/Restore (T4)", xp=35, level_required=4, escalation_time=210)

    def simulate_escalation(self):
        """Periodically mark tasks as escalated if they have exceeded their escalation time."""
        while self.running:
            current_time = time.time()
            with self.lock:
                for task in self.tasks.values():
                    if not task["completed"] and not task["escalated"]:
                        if current_time - task["time_created"] > task["escalation_time"]:
                            task["escalated"] = True
                            # Optionally reduce the XP reward if escalated
                            task["xp"] = int(task["xp"] * 0.5)
            time.sleep(5)

    def auto_generate_tasks(self):
        """Automatically generate new tasks if there are fewer than 3 active tasks."""
        while self.running:
            with self.lock:
                active_tasks = [t for t in self.tasks.values() if not t["completed"]]
                if len(active_tasks) < 3:
                    task_options = [
                        ("Reset user password (T1)", 10, 1, 60),
                        ("Edit DNS settings (T1)", 15, 1, 90),
                        ("Run malware scan (T2)", 20, 2, 120),
                        ("Configure Firewall rules (T2+)", 25, 2, 150),
                        ("Mitigate DDoS attack (T3+)", 30, 3, 180),
                        ("Perform Backup/Restore (T4)", 35, 4, 210)
                    ]
                    available = [opt for opt in task_options if opt[2] <= self.level]
                    if available:
                        description, xp, lvl_req, esc_time = random.choice(available)
                        self.add_task(description, xp, lvl_req, esc_time)
            time.sleep(30)

    def to_dict(self):
        with self.lock:
            return {
                "xp": self.xp,
                "level": self.level,
                "tasks": self.tasks,
                "task_counter": self.task_counter
            }
    
    def from_dict(self, data):
        with self.lock:
            self.xp = data.get("xp", 0)
            self.level = data.get("level", 1)
            self.tasks = data.get("tasks", {})
            self.task_counter = data.get("task_counter", 1)
