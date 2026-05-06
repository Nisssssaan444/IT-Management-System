import argparse
import sys
from src.db import init_db
from src.onboarding import onboard_user
from src.offboarding import offboard_user
from src.assets import add_asset, list_unassigned_assets, generate_report
from src.audit import view_audit_logs, export_audit_logs

def main():
    init_db()
    
    parser = argparse.ArgumentParser(description="IT Onboarding & Offboarding Toolkit")
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

    # Onboard
    onboard_parser = subparsers.add_parser('onboard', help='Onboard a new employee')
    onboard_parser.add_argument('--name', required=True, help="Full name of the employee")
    onboard_parser.add_argument('--dept', required=True, help="Department")
    onboard_parser.add_argument('--manager', required=True, help="Manager email")

    # Offboard
    offboard_parser = subparsers.add_parser('offboard', help='Offboard an employee')
    offboard_parser.add_argument('--user', required=True, help="User email to offboard")

    # Assets
    asset_parser = subparsers.add_parser('asset', help='Manage IT assets')
    asset_parser.add_argument('--add', action='store_true', help='Add a new asset')
    asset_parser.add_argument('--name', help='Asset name')
    asset_parser.add_argument('--assigned-to', help='Username the asset is assigned to')
    asset_parser.add_argument('--type', help='Asset type (e.g., laptop)')
    asset_parser.add_argument('--serial', help='Serial number')
    asset_parser.add_argument('--list', action='store_true', help='List assets')
    asset_parser.add_argument('--unassigned', action='store_true', help='Filter list to unassigned')
    asset_parser.add_argument('--report', action='store_true', help='Generate asset CSV report')

    # Audit
    audit_parser = subparsers.add_parser('audit', help='View action audits')
    audit_parser.add_argument('--last', type=int, help='Show last N events')
    audit_parser.add_argument('--user', help='Filter audits by username/email')
    audit_parser.add_argument('--export', help='Export to CSV filename')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.command == 'onboard':
        onboard_user(args.name, args.dept, args.manager)
    
    elif args.command == 'offboard':
        offboard_user(args.user)
        
    elif args.command == 'asset':
        if args.add:
            if not all([args.name, args.type, args.serial]):
                print("❌ --name, --type, and --serial are required to add an asset.")
                return
            add_asset(args.name, args.type, args.serial, args.assigned_to)
        elif args.list and args.unassigned:
            list_unassigned_assets()
        elif args.report:
            generate_report()
            
    elif args.command == 'audit':
        if args.export:
            export_audit_logs(args.user, args.export)
        elif args.last:
            view_audit_logs(args.last)
        else:
            view_audit_logs()

if __name__ == '__main__':
    main()
