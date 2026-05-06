from src.db import get_connection, log_action
import csv

def add_asset(name, type_, serial, assigned_to=None):
    conn = get_connection()
    c = conn.cursor()
    status = 'Assigned' if assigned_to else 'Unassigned'
    
    try:
        c.execute('''INSERT INTO assets (name, type, serial, assigned_to, status)
                     VALUES (?, ?, ?, ?, ?)''', (name, type_, serial, assigned_to, status))
        conn.commit()
        log_action("ADD_ASSET", f"Added {type_} {name} (SN: {serial})")
        print(f"✅ Asset {name} (SN: {serial}) added successfully!")
    except Exception as e:
        print(f"❌ Error adding asset: {e}")
    finally:
        conn.close()

def update_asset_assignment(serial, assigned_to=None):
    conn = get_connection()
    c = conn.cursor()
    status = 'Assigned' if assigned_to else 'Unassigned'
    
    c.execute("UPDATE assets SET assigned_to=?, status=? WHERE serial=?", (assigned_to, status, serial))
    conn.commit()
    conn.close()

def list_unassigned_assets():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, type, serial FROM assets WHERE status='Unassigned'")
    assets = c.fetchall()
    
    if not assets:
        print("No unassigned assets found.")
        return
        
    print(f"{'Name':<20} | {'Type':<15} | {'Serial'}")
    print("-" * 55)
    for asset in assets:
        print(f"{asset[0]:<20} | {asset[1]:<15} | {asset[2]}")
    conn.close()

def generate_report():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, type, serial, assigned_to, status FROM assets")
    assets = c.fetchall()
    
    filename = "asset_report.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Type', 'Serial', 'Assigned To', 'Status'])
        writer.writerows(assets)
        
    print(f"📄 Asset report generated: {filename}")
    log_action("ASSET_REPORT", "Generated full asset inventory report")
    conn.close()
