from src.db import get_connection, log_action
from src.assets import update_asset_assignment

def offboard_user(email):
    conn = get_connection()
    c = conn.cursor()
    
    # Check if user exists
    c.execute("SELECT username, name FROM users WHERE email=? AND status='Active'", (email,))
    user = c.fetchone()
    
    if not user:
        print(f"❌ User with email {email} not found or already disabled.")
        return
        
    username, name = user
    
    # Disable user
    c.execute("UPDATE users SET status='Disabled' WHERE email=?", (email,))
    
    # Reclaim assets
    c.execute("SELECT name, serial FROM assets WHERE assigned_to=?", (username,))
    assets = c.fetchall()
    
    for asset in assets:
        c.execute("UPDATE assets SET assigned_to=NULL, status='Unassigned' WHERE serial=?", (asset[1],))
        
    conn.commit()
    conn.close()
    
    log_action("OFFBOARD_USER", f"Disabled user {email} and reclaimed {len(assets)} assets")
    
    print(f"🛑 User {name} ({email}) has been successfully offboarded.")
    print("✓ Account status set to disabled")
    print("✓ Revoked group memberships (simulated)")
    
    if assets:
        print("\n📦 Reclaimed Assets:")
        for asset in assets:
            print(f"  - {asset[0]} (SN: {asset[1]})")
    else:
        print("\n📦 No assets were assigned to this user.")
        
    print("\n--- Simulated Offboarding Checklist ---")
    print(f"[X] Disable M365 account for {email}")
    print(f"[X] Remove AD group licenses")
    print(f"[X] Archive user home directory")
    print(f"[X] Unassign IT hardware")
    print("---------------------------------------")
