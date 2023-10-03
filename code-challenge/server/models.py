from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) == 0:
            raise ValueError("Name must not be empty")
        return name

    @validates('description')
    def validate_description(self, key, description):
        if len(description.strip()) == 0:
            raise ValueError("Description must not be empty")
        return description

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(10), nullable=False)

    @validates('strength')
    def validate_strength(self, key, strength):
        allowed_strengths = ["Strong", "Weak", "Average"]
        if strength not in allowed_strengths:
            raise ValueError("Strength must be one of 'Strong', 'Weak', 'Average'")
        return strength
