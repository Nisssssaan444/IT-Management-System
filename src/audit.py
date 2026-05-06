from src.db import get_connection
import csv

def view_audit_logs(limit=50):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT timestamp, action, details FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = c.fetchall()
    
    print(f"{'Timestamp':<25} | {'Action':<15} | {'Details'}")
    print("-" * 80)
    for log in logs:
        print(f"{log[0]:<25} | {log[1]:<15} | {log[2]}")
    conn.close()

def export_audit_logs(user=None, output_file="audit_report.csv"):
    conn = get_connection()
    c = conn.cursor()
    
    if user:
        # Search for details containing the user
        c.execute("SELECT timestamp, action, details FROM audit_logs WHERE details LIKE ? ORDER BY id DESC", (f'%{user}%',))
    else:
        c.execute("SELECT timestamp, action, details FROM audit_logs ORDER BY id DESC")
        
    logs = c.fetchall()
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Action', 'Details'])
        writer.writerows(logs)
        
    print(f"📄 Audit logs exported to {output_file}")
    conn.close()
