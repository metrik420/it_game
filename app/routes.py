from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.game_engine import GameEngine
from app.save_manager import save_game, load_game

bp = Blueprint('main', __name__)

# Global game engine instance
game = GameEngine()

@bp.route('/')
def index():
    return render_template('index.html', game=game)

@bp.route('/complete_task', methods=['POST'])
def complete_task():
    task_id = request.form.get('task_id')
    if task_id:
        xp_reward = game.complete_task(task_id)
        flash(f'Task completed! Gained {xp_reward} XP.')
    else:
        flash('No task selected.')
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

@bp.route('/game_state', methods=['GET'])
def game_state():
    return jsonify(game.to_dict())
