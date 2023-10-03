# Import the random module
import random
from app import create_app, db, Hero, Power, HeroPower
# Import Session from SQLAlchemy
from sqlalchemy.orm import Session

# Create a Flask application instance
app = create_app()

# Push the application context to interact with the database
with app.app_context():
    # Create a session using the database engine
    session = Session(bind=db.engine)

    print("Seeding powers...")
    powers = [
    { "name": "super strength", "description": "gives the wielder super-human strengths" },
    { "name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed" },
    { "name": "super human senses", "description": "allows the wielder to use her senses at a super-human level" },
    { "name": "elasticity", "description": "can stretch the human body to extreme lengths" }
    ]

    for power_data in powers:
        # Check if the power with the same name exists
        existing_power = Power.query.filter_by(name=power_data['name']).first()
        
        if not existing_power:
            power = Power(**power_data)
            db.session.add(power)

    print("🦸‍♀️ Seeding heroes...")
    heroes = [
    { "name": "Kamala Khan", "super_name": "Ms. Marvel" },
    { "name": "Doreen Green", "super_name": "Squirrel Girl" },
    { "name": "Gwen Stacy", "super_name": "Spider-Gwen" },
    { "name": "Janet Van Dyne", "super_name": "The Wasp" },
    { "name": "Wanda Maximoff", "super_name": "Scarlet Witch" },
    { "name": "Carol Danvers", "super_name": "Captain Marvel" },
    { "name": "Jean Grey", "super_name": "Dark Phoenix" },
    { "name": "Ororo Munroe", "super_name": "Storm" },
    { "name": "Kitty Pryde", "super_name": "Shadowcat" },
    { "name": "Elektra Natchios", "super_name": "Elektra" }
    ]

    for hero_data in heroes:
        hero = Hero(**hero_data)
        db.session.add(hero)

    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]

    for hero in Hero.query.all():
        # Randomly assign 1 to 3 powers to each hero
        for _ in range(1, 4):
            # Generate a random power ID
            random_power_id = random.randint(1, len(powers))

            # Check if the power with the generated ID exists
            power = session.get(Power, random_power_id)

            # Check if the power was found
            if power is not None:
                strength = random.choice(strengths)
                hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=strength)
                db.session.add(hero_power)
            else:
                print(f"Power not found for hero {hero.id}")

    print("🦸‍♀️ Done seeding!")
    db.session.commit()
