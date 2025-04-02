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

@bp.route('/tool/<tool_name>', methods=['GET'])
def run_tool(tool_name):
    try:
        tool_module = __import__(f"app.tools.{tool_name}", fromlist=['run_tool'])
        result = tool_module.run_tool()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

def verify_and_complete_task(tool_name, field_name, user_input, xp_reward):
    user_input = user_input.strip().strip("'\"").lower()
    matched = False
    for task_id, task in game.tasks.items():
        if not task["completed"] and task["tool_required"] == tool_name:
            task_value = task["account"].get(field_name, "").strip().lower()
            if user_input == task_value:
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
    if not username:
        flash("Username is required.", "danger")
    else:
        from app.tools import password_reset
        password_reset.run_tool()
        verify_and_complete_task("Password Reset", "username", username, 10)
    return redirect(url_for('main.index'))

@bp.route('/tool/dns_editor', methods=['POST'])
def dns_editor_tool():
    hostname = request.form.get('hostname', '').strip().strip("'\"").lower()
    ip_address = request.form.get('ip_address', '').strip().strip("'\"")

    matched = False
    for task_id, task in game.tasks.items():
        if not task["completed"] and task["tool_required"] == "DNS Editor":
            expected_hostname = task["account"].get("hostname", "").strip().lower()
            expected_ip = task["account"].get("ip", "").strip()
            if hostname == expected_hostname and ip_address == expected_ip:
                game.complete_task(task_id)
                game.log_event(f"✅ DNS updated for {hostname} (task: {task_id})")
                flash(f"DNS settings updated for {hostname}!", "success")
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
    if not scan_path:
        flash("Scan path required.", "danger")
    else:
        from app.tools import malware_scanner
        malware_scanner.run_tool()
        verify_and_complete_task("Malware Scanner", "scan_path", scan_path, 20)
    return redirect(url_for('main.index'))

@bp.route('/tool/firewall_console', methods=['POST'])
def firewall_console_tool():
    port = request.form.get('port')
    action = request.form.get('action')
    if not port or not action:
        flash("Port and action are required.", "danger")
    else:
        from app.tools import firewall_console
        firewall_console.run_tool()
        verify_and_complete_task("Firewall Console", "port", port, 25)
    return redirect(url_for('main.index'))

@bp.route('/tool/ddos_mitigator', methods=['POST'])
def ddos_mitigator_tool():
    target = request.form.get('target')
    if not target:
        flash("Target is required.", "danger")
    else:
        from app.tools import ddos_mitigator
        ddos_mitigator.run_tool()
        verify_and_complete_task("DDoS Mitigator", "target", target, 30)
    return redirect(url_for('main.index'))

@bp.route('/tool/backup_restore', methods=['POST'])
def backup_restore_tool():
    target_user = request.form.get('username')
    if not target_user:
        flash("Username is required for backup/restore.", "danger")
    else:
        from app.tools import backup_restore
        backup_restore.run_tool()
        verify_and_complete_task("Backup/Restore", "username", target_user, 35)
    return redirect(url_for('main.index'))

@bp.route('/game_state', methods=['GET'])
def game_state():
    return jsonify(game.to_dict())
