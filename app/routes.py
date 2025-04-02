from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.game_engine import GameEngine
from app.save_manager import save_game, load_game

bp = Blueprint('main', __name__)
game = GameEngine()

@bp.route('/')
def index():
    return render_template('index.html', game=game)

@bp.route('/complete_task', methods=['POST'])
def complete_task():
    flash('Tasks must be completed through the correct tool now.', 'warning')
    return redirect(url_for('main.index'))

@bp.route('/save', methods=['POST'])
def save():
    save_game(game)
    flash('Game saved successfully.')
    return redirect(url_for('main.index'))

@bp.route('/load', methods=['POST'])
def load():
    loaded_game = load_game()
    if loaded_game:
        game.from_dict(loaded_game.to_dict())
        flash('Game loaded successfully.')
    else:
        flash('Failed to load game.')
    return redirect(url_for('main.index'))

def verify_and_complete_task(tool_name, field_name, user_input, xp_reward, extra_match=None):
    user_input = user_input.strip().strip("'\"").lower()
    matched = False

    for task_id, task in game.tasks.items():
        if not task["completed"] and task["tool_required"] == tool_name:
            target_val = str(task["account"].get(field_name, "")).strip().lower()

            if tool_name == "Firewall Console":
                if user_input in task["account"].get("ports", []):
                    game.complete_task(task_id)
                    game.log_event(f"✅ Firewall rule applied for port {user_input} (task: {task_id})")
                    flash(f"Firewall rule applied for port {user_input}!", "success")
                    matched = True
                    break
            elif tool_name == "DDoS Mitigator":
                valid_targets = task["account"].get("targets", [])
                if user_input in [t.lower() for t in valid_targets]:
                    game.complete_task(task_id)
                    game.log_event(f"✅ DDoS mitigated for {user_input} (task: {task_id})")
                    flash(f"DDoS mitigation successful for {user_input}!", "success")
                    matched = True
                    break
            else:
                if user_input == target_val:
                    game.complete_task(task_id)
                    game.log_event(f"✅ {tool_name} success for {user_input} (task: {task_id})")
                    flash(f"{tool_name} completed for {user_input}!", "success")
                    matched = True
                    break

    if not matched:
        game.log_event(f"❌ {tool_name} failed - bad input '{user_input}'")
        game.xp = max(0, game.xp - 5)
        flash(f"{tool_name} failed. Incorrect input or no matching task. (-5 XP)", "danger")

@bp.route('/tool/password_reset', methods=['POST'])
def password_reset_tool():
    username = request.form.get('username')
    if username:
        from app.tools import password_reset
        password_reset.run_tool()
        verify_and_complete_task("Password Reset", "username", username, 10)
    else:
        flash("Username is required.", "danger")
    return redirect(url_for('main.index'))

@bp.route('/tool/dns_editor', methods=['POST'])
def dns_editor_tool():
    hostname = request.form.get('hostname', '').strip().lower()
    ip_address = request.form.get('ip_address', '').strip()

    matched = False
    for task_id, task in game.tasks.items():
        if not task["completed"] and task["tool_required"] == "DNS Editor":
            if hostname == task["account"].get("hostname", "").lower() and ip_address == task["account"].get("ip", ""):
                game.complete_task(task_id)
                game.log_event(f"✅ DNS updated for {hostname} (task: {task_id})")
                flash(f"DNS updated for {hostname}!", "success")
                matched = True
                break
    if not matched:
        game.log_event(f"❌ DNS Editor failed - bad input '{hostname}'")
        game.xp = max(0, game.xp - 5)
        flash("DNS Editor failed. Incorrect input or no matching task. (-5 XP)", "danger")

    return redirect(url_for('main.index'))

@bp.route('/tool/malware_scanner', methods=['POST'])
def malware_scanner_tool():
    scan_path = request.form.get('scan_path')
    if scan_path:
        from app.tools import malware_scanner
        malware_scanner.run_tool()
        verify_and_complete_task("Malware Scanner", "scan_path", scan_path, 20)
    else:
        flash("Scan path required.", "danger")
    return redirect(url_for('main.index'))

@bp.route('/tool/firewall_console', methods=['POST'])
def firewall_console_tool():
    port = request.form.get('port')
    action = request.form.get('action')
    if port and action:
        from app.tools import firewall_console
        firewall_console.run_tool()
        verify_and_complete_task("Firewall Console", "port", port, 25)
    else:
        flash("Port and action are required.", "danger")
    return redirect(url_for('main.index'))

@bp.route('/tool/ddos_mitigator', methods=['POST'])
def ddos_mitigator_tool():
    target = request.form.get('target')
    if target:
        from app.tools import ddos_mitigator
        ddos_mitigator.run_tool()
        verify_and_complete_task("DDoS Mitigator", "target", target, 30)
    else:
        flash("Target is required.", "danger")
    return redirect(url_for('main.index'))

@bp.route('/tool/backup_restore', methods=['POST'])
def backup_restore_tool():
    target_user = request.form.get('username')
    if target_user:
        from app.tools import backup_restore
        backup_restore.run_tool()
        verify_and_complete_task("Backup/Restore", "username", target_user, 35)
    else:
        flash("Username is required.", "danger")
    return redirect(url_for('main.index'))

@bp.route('/game_state', methods=['GET'])
def game_state():
    return jsonify(game.to_dict())
