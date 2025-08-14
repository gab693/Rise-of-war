
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import time
import json
import os
from replit import db

app = Flask(__name__)
app.secret_key = 'warfare_game_secret_key_2024'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False
from datetime import timedelta
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

class WarfareGame:
    def __init__(self):
        self.ages = {
            0: {
                "name": "Neolithic", 
                "weapons": ["Stone Axe", "Wooden Spear", "Sling"], 
                "armor": ["Leather Hide", "Fur Cloak", "Bone Shield"],
                "countries": ["Cave Dwellers", "Nomadic Tribes", "Settlers"],
                "scroll_cost": 50
            },
            1: {
                "name": "Bronze Age", 
                "weapons": ["Bronze Sword", "Bronze Spear", "Bow"], 
                "armor": ["Bronze Breastplate", "Bronze Helmet", "Bronze Shield"],
                "countries": ["Bronze Kingdoms", "Classical Rome", "Han Dynasty"],
                "scroll_cost": 100
            },
            2: {
                "name": "Iron Age", 
                "weapons": ["Iron Sword", "Crossbow", "Catapult"], 
                "armor": ["Iron Mail", "Iron Helmet", "Reinforced Shield"],
                "countries": ["Sparta", "Celtic Tribes", "Germanic Clans"],
                "scroll_cost": 200
            },
            3: {
                "name": "Medieval", 
                "weapons": ["Steel Sword", "Longbow", "Trebuchet"], 
                "armor": ["Chainmail", "Knight's Plate", "Tower Shield"],
                "countries": ["Vikings", "England", "Holy Roman Empire"],
                "scroll_cost": 400
            },
            4: {
                "name": "Renaissance", 
                "weapons": ["Musket", "Cannon", "Pike"], 
                "armor": ["Steel Cuirass", "Morion Helmet", "Pavise Shield"],
                "countries": ["Spain", "French Empire", "Ottoman Empire"],
                "scroll_cost": 800
            },
            5: {
                "name": "Industrial", 
                "weapons": ["Rifle", "Artillery", "Machine Gun"], 
                "armor": ["Military Uniform", "Steel Helmet", "Trench Armor"],
                "countries": ["British Empire", "German Reich", "Russian Empire"],
                "scroll_cost": 1600
            },
            6: {
                "name": "Modern", 
                "weapons": ["Assault Rifle", "Tank", "Fighter Jet"], 
                "armor": ["Kevlar Vest", "Combat Helmet", "Riot Shield"],
                "countries": ["United States", "Soviet Union", "NATO Alliance"],
                "scroll_cost": 3200
            },
            7: {
                "name": "Sci-Fi", 
                "weapons": ["Laser Rifle", "Mech Suit", "Plasma Cannon"], 
                "armor": ["Energy Shield", "Nano Armor", "Power Suit"],
                "countries": ["Galactic Federation", "Cyber Collective", "Space Colonies"],
                "scroll_cost": 6400
            }
        }

        self.default_player = {
            "name": "",
            "age": 0,
            "money": 100,
            "scrolls": 0,
            "experience": 0,
            "level": 1,
            "wins": 0,
            "losses": 0,
            "donation_progress": 0,
            "soldiers": 0,
            "last_soldier_income": 0,
            "country": "",
            "armor": "",
            "player_x": 7.5,
            "player_y": 9.0
        }

        self.donation_required = 1000
        
        # Soldier attributes based on country
        self.soldier_attributes = {
            "Cave Dwellers": {"advantage": "Stealth", "weakness": "Low Defense"},
            "Nomadic Tribes": {"advantage": "Mobility", "weakness": "Weak Offense"},
            "Settlers": {"advantage": "Defense", "weakness": "Slow"},
            "Bronze Kingdoms": {"advantage": "Armor", "weakness": "Less Agile"},
            "Classical Rome": {"advantage": "Tactics", "weakness": "Vulnerable to Range"},
            "Han Dynasty": {"advantage": "Archery Skills", "weakness": "Close Combat"},
            "Sparta": {"advantage": "Strength", "weakness": "Stamina Issues"},
            "Celtic Tribes": {"advantage": "Bravery", "weakness": "Unorganized"},
            "Germanic Clans": {"advantage": "Ferocity", "weakness": "Discipline"},
            "Vikings": {"advantage": "Nautical Skills", "weakness": "Land Battles"},
            "England": {"advantage": "Archery", "weakness": "Cavalry Weak"},
            "Holy Roman Empire": {"advantage": "Armor Training", "weakness": "Heavy Equipment"},
            "Spain": {"advantage": "Cavalry", "weakness": "Bad Supply Lines"},
            "French Empire": {"advantage": "Artillery", "weakness": "Mobility"},
            "Ottoman Empire": {"advantage": "Infantry", "weakness": "Slow to Reload"},
            "British Empire": {"advantage": "Firepower", "weakness": "Limited Resources"},
            "German Reich": {"advantage": "Technology", "weakness": "Resource Intensive"},
            "Russian Empire": {"advantage": "Endurance", "weakness": "Logistics"},
            "United States": {"advantage": "Firearms", "weakness": "Overconfident"},
            "Soviet Union": {"advantage": "Tank Warfare", "weakness": "Fuel Dependence"},
            "NATO Alliance": {"advantage": "Coalition Forces", "weakness": "Conflicting Tactics"},
            "Galactic Federation": {"advantage": "Advanced Tech", "weakness": "Unfamiliar Terrain"},
            "Cyber Collective": {"advantage": "Cyber Defense", "weakness": "Physical Combat"},
            "Space Colonies": {"advantage": "Adaptability", "weakness": "Limited Resources"},
        }

    def get_player_data(self):
        if 'player_id' not in session:
            session['player_id'] = f"player_{int(time.time() * 1000)}"
        
        player_id = session['player_id']
        
        try:
            if player_id in db:
                return json.loads(db[player_id])
            else:
                player = self.default_player.copy()
                db[player_id] = json.dumps(player)
                return player
        except:
            # Fallback to session if db fails
            if 'player' not in session:
                session['player'] = self.default_player.copy()
            return session['player']

    def save_player_data(self, player_data):
        if 'player_id' in session:
            try:
                db[session['player_id']] = json.dumps(player_data)
            except:
                session['player'] = player_data
        else:
            session['player'] = player_data

    def get_soldier_info(self, country):
        return self.soldier_attributes.get(country, {"advantage": "None", "weakness": "None"})

# Initialize game
game = WarfareGame()

@app.route('/')
def index():
    player = game.get_player_data()
    
    # If player has a name, show the game
    if player['name']:
        current_age = game.ages[player['age']]
        soldier_info = game.get_soldier_info(player['country']) if player['country'] else {"advantage": "None", "weakness": "None"}
        
        return render_template('game.html', 
                             player=player, 
                             current_age=current_age,
                             soldier_info=soldier_info,
                             game=game)
    else:
        # Show name selection
        return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    name = request.form.get('name', '').strip()
    if name:
        player = game.get_player_data()
        player['name'] = name
        game.save_player_data(player)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/battle', methods=['POST'])
def battle():
    player = game.get_player_data()
    current_age = game.ages[player['age']]
    
    # Improved battle mechanics - more balanced
    base_power = player['level'] * 15 + player['soldiers'] * 8 + 30  # Base 30 power
    player_power = base_power
    
    # Enemy power scales more reasonably
    enemy_base = 40 + player['age'] * 15
    enemy_power = random.randint(enemy_base - 20, enemy_base + 30)
    
    # Apply armor bonus
    if player['armor']:
        player_power += 15
    
    # Apply soldier advantages/weaknesses with clearer effects
    advantage_bonus = 0
    weakness_penalty = 0
    
    if player['country']:
        soldier_info = game.get_soldier_info(player['country'])
        if random.random() < 0.4:  # 40% chance for advantage
            advantage_bonus = 25
            player_power += advantage_bonus
        if random.random() < 0.25:  # 25% chance for weakness
            weakness_penalty = 15
            player_power -= weakness_penalty
    
    # Battle resolution
    power_difference = player_power - enemy_power
    
    if power_difference > 0:
        win = True
        # Better rewards for decisive victories
        victory_bonus = min(power_difference // 10, 30)
        money_gain = random.randint(25, 60) + player['age'] * 12 + victory_bonus
        exp_gain = random.randint(15, 35) + victory_bonus // 2
        
        player['money'] += money_gain
        player['experience'] += exp_gain
        player['wins'] += 1
        
        # Level up check
        if player['experience'] >= player['level'] * 100:
            player['level'] += 1
            player['experience'] = 0
            
        bonus_text = f" (Bonus: +{victory_bonus})" if victory_bonus > 0 else ""
        advantage_text = f" [Advantage: +{advantage_bonus}]" if advantage_bonus > 0 else ""
        weakness_text = f" [Weakness: -{weakness_penalty}]" if weakness_penalty > 0 else ""
        
        result = f"Victory! Gained {money_gain} gold and {exp_gain} experience!{bonus_text}{advantage_text}{weakness_text}"
    else:
        win = False
        money_loss = min(player['money'], random.randint(8, 25))
        player['money'] -= money_loss
        player['losses'] += 1
        
        weakness_text = f" [Weakness: -{weakness_penalty}]" if weakness_penalty > 0 else ""
        result = f"Defeat! Lost {money_loss} gold. (Power: {player_power} vs {enemy_power}){weakness_text}"
    
    game.save_player_data(player)
    return jsonify({'success': True, 'result': result, 'win': win})

@app.route('/buy_scroll', methods=['POST'])
def buy_scroll():
    player = game.get_player_data()
    current_age = game.ages[player['age']]
    cost = current_age['scroll_cost']
    
    if player['money'] >= cost:
        player['money'] -= cost
        player['scrolls'] += 1
        game.save_player_data(player)
        return jsonify({'success': True, 'message': f'Bought scroll for {cost} gold!'})
    else:
        return jsonify({'success': False, 'message': 'Not enough gold!'})

@app.route('/donate', methods=['POST'])  
def donate():
    player = game.get_player_data()
    donation_amount = int(request.form.get('amount', 0))
    
    if player['money'] >= donation_amount:
        player['money'] -= donation_amount
        player['donation_progress'] += donation_amount
        
        if player['donation_progress'] >= game.donation_required and player['age'] < 7:
            # Check if player has a scroll for advancing
            if player['scrolls'] >= 1:
                old_age = game.ages[player['age']]['name']
                player['age'] += 1
                player['donation_progress'] = 0
                player['scrolls'] -= 1  # Consume one scroll
                
                # All soldiers become outdated in the new era
                outdated_soldiers = player['soldiers']
                player['soldiers'] = 0
                player['country'] = ""  # Reset country selection
                player['armor'] = ""    # Reset armor selection
                
                new_age = game.ages[player['age']]['name']
                message = f"🎉 Advanced from {old_age} to {new_age}! {outdated_soldiers} soldiers were outdated and dismissed. 1 scroll consumed. Choose new country and armor!"
            else:
                message = f"❌ You need at least 1 scroll to advance to the next age! Donation progress: {player['donation_progress']}/{game.donation_required}. Buy scrolls first!"
        elif player['age'] >= 7:
            message = f"🏆 You've reached the maximum age! Donated {donation_amount} gold anyway."
        else:
            needed = game.donation_required - player['donation_progress']
            message = f"💰 Donated {donation_amount} gold! Need {needed} more gold to advance. (Also need 1 scroll!)"
            
        game.save_player_data(player)
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': 'Not enough gold!'})

@app.route('/recruit_soldier', methods=['POST'])
def recruit_soldier():
    player = game.get_player_data()
    cost = 50 + (player['age'] * 25)
    
    if player['money'] >= cost:
        player['money'] -= cost
        player['soldiers'] += 1
        game.save_player_data(player)
        return jsonify({'success': True, 'message': f'Recruited soldier for {cost} gold!'})
    else:
        return jsonify({'success': False, 'message': 'Not enough gold!'})

@app.route('/collect_income', methods=['POST'])
def collect_income():
    player = game.get_player_data()
    current_time = int(time.time())
    
    if current_time - player['last_soldier_income'] >= 60:  # 1 minute cooldown
        income = player['soldiers'] * 5
        player['money'] += income
        player['last_soldier_income'] = current_time
        game.save_player_data(player)
        return jsonify({'success': True, 'message': f'Collected {income} gold from soldiers!'})
    else:
        remaining = 60 - (current_time - player['last_soldier_income'])
        return jsonify({'success': False, 'message': f'Wait {remaining} seconds!'})

@app.route('/choose_country', methods=['POST'])
def choose_country():
    player = game.get_player_data()
    country = request.form.get('country')
    current_age = game.ages[player['age']]
    
    if country in current_age['countries']:
        player['country'] = country
        game.save_player_data(player)
        soldier_info = game.get_soldier_info(country)
        return jsonify({
            'success': True, 
            'message': f'Joined {country}!',
            'advantage': soldier_info['advantage'],
            'weakness': soldier_info['weakness']
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid country!'})

@app.route('/choose_armor', methods=['POST'])
def choose_armor():
    player = game.get_player_data()
    armor = request.form.get('armor')
    current_age = game.ages[player['age']]
    
    if armor in current_age['armor']:
        player['armor'] = armor
        game.save_player_data(player)
        return jsonify({'success': True, 'message': f'Equipped {armor}!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid armor!'})

@app.route('/enter_battlefield', methods=['POST'])
def enter_battlefield():
    player = game.get_player_data()
    
    if player['soldiers'] <= 0:
        return jsonify({'success': False, 'message': 'You need soldiers to enter the battlefield!'})
    
    # Ensure player has position data (for existing players)
    if 'player_x' not in player:
        player['player_x'] = 7.5
    if 'player_y' not in player:
        player['player_y'] = 9.0
    
    # Generate battlefield map
    battlefield_map = generate_battlefield_map(player['soldiers'])
    
    return jsonify({
        'success': True, 
        'soldiers': player['soldiers'],
        'battlefield_map': battlefield_map,
        'player_x': player['player_x'],
        'player_y': player['player_y'],
        'message': 'Entering battlefield...'
    })

def generate_battlefield_map(soldier_count):
    # Create a larger endless battlefield grid
    width, height = 30, 20
    battlefield = []
    
    # Generate soldier positions (green dots) around the player
    soldier_positions = []
    for _ in range(min(soldier_count, 20)):  # Max 20 soldiers on map
        x = random.randint(5, 10)  # Near player starting position
        y = random.randint(7, 12)
        soldier_positions.append({'x': x, 'y': y, 'type': 'soldier', 'alive': True})
    
    # Generate enemy positions (red dots) scattered across the map
    enemy_count = random.randint(15, 25)
    enemy_positions = []
    for _ in range(enemy_count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        # Avoid spawning too close to player start position
        if abs(x - 7.5) > 3 or abs(y - 9) > 3:
            enemy_positions.append({'x': x, 'y': y, 'type': 'enemy', 'alive': True})
    
    return {
        'width': width,
        'height': height,
        'soldiers': soldier_positions,
        'enemies': enemy_positions
    }

@app.route('/move_player', methods=['POST'])
def move_player():
    player = game.get_player_data()
    
    x = float(request.form.get('x', 0))
    y = float(request.form.get('y', 0))
    
    # Update player position
    player['player_x'] = x
    player['player_y'] = y
    
    game.save_player_data(player)
    return jsonify({'success': True})

@app.route('/end_battlefield', methods=['POST'])
def end_battlefield():
    player = game.get_player_data()
    
    enemies_killed = int(request.form.get('enemies_killed', 0))
    time_survived = int(request.form.get('time_survived', 0))
    gold_earned = int(request.form.get('gold_earned', 0))
    retreated = request.form.get('retreated') == 'true'
    
    # Award the gold earned
    player['money'] += gold_earned
    
    # Award experience based on performance
    exp_gain = enemies_killed * 5 + time_survived // 2
    player['experience'] += exp_gain
    
    # Level up check
    while player['experience'] >= player['level'] * 100:
        player['level'] += 1
        player['experience'] -= (player['level'] - 1) * 100
    
    # Update battle stats
    player['wins'] += enemies_killed
    if not retreated:
        player['losses'] += 1
        player['soldiers'] = 0  # All soldiers died
        message = f"All soldiers perished! Earned {gold_earned} gold, {exp_gain} XP. Killed {enemies_killed} enemies in {time_survived}s."
    else:
        message = f"Retreated safely! Earned {gold_earned} gold, {exp_gain} XP. Killed {enemies_killed} enemies in {time_survived}s."
    
    game.save_player_data(player)
    return jsonify({'success': True, 'message': message})

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('player', None)
    return jsonify({'success': True, 'message': 'Game reset successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
