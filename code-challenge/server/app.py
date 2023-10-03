#!/usr/bin/env python3
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    migrate = Migrate(app, db)

    db.init_app(app)

    # Define routes here

    @app.route('/')
    def home():
        return ''

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        hero_list = []
        for hero in heroes:
            hero_list.append({
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            })
        return jsonify(hero_list)

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero_by_id(id):
        hero = Hero.query.get(id)
        if hero is None:
            return jsonify({'error': 'Hero not found'}), 404
        return jsonify({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        })

    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        power_list = []
        for power in powers:
            power_list.append({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        return jsonify(power_list)

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power_by_id(id):
        power = Power.query.get(id)
        if power is None:
            return jsonify({'error': 'Power not found'}), 404
        return jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power_description(id):
        power = Power.query.get(id)
        if power is None:
            return jsonify({'error': 'Power not found'}), 404

        data = request.get_json()
        new_description = data.get('description')

        if not new_description:
            return jsonify({'error': 'Description is required'}), 400

        power.description = new_description
        db.session.commit()

        return jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()

        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        strength = data.get('strength')

        if not hero_id or not power_id or not strength:
            return jsonify({'error': 'Missing data'}), 400

        hero = Hero.query.get(hero_id)
        if hero is None:
            return jsonify({'error': 'Hero not found'}), 404

        power = Power.query.get(power_id)
        if power is None:
            return jsonify({'error': 'Power not found'}), 404

        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        return jsonify({
            'hero_id': hero_id,
            'power_id': power_id,
            'strength': strength
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555)
