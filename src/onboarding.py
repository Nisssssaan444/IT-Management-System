import random
import string
import yaml
from src.db import get_connection, log_action

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def onboard_user(name, department, manager):
    config = load_config()
    domain = config['company']['domain']
    
    # Simple username generation (e.g. John Doe -> john.doe)
    username = name.lower().replace(" ", ".")
    email = f"{username}@{domain}"
    password = generate_password(config.get('default_password_length', 12))
    
    conn = get_connection()
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO users (name, username, email, department, manager, status)
                     VALUES (?, ?, ?, ?, ?, ?)''', (name, username, email, department, manager, 'Active'))
        conn.commit()
        
        details = f"Created user {name} ({email}) in {department}"
        log_action("ONBOARD_USER", details)
        
        print(f"✅ User {name} onboarded successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Temporary Password: {password}")
        print(f"🏢 Department: {department}")
        print(f"👤 Manager: {manager}")
        
        print("\n--- Simulated Welcome Email ---")
        print(f"To: {email}")
        print(f"Subject: Welcome to {config['company']['name']}!")
        print(f"Hello {name},\nWelcome to the team! Your manager {manager} is excited to have you.\nYour IT setup is complete.")
        print("-------------------------------")
        
    except Exception as e:
        print(f"❌ Error onboarding user: {e}")
    finally:
        conn.close()
