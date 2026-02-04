"""PPP CLI entrypoint."""

import sys
import argparse
from .runner import PPPRunner
from .storage.progress import ProgressStore


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Public Participation Probe (PPP) v0 - Policy-governed autonomous agent harness"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run PPP")
    run_parser.add_argument("--all", action="store_true", help="Run all agents")
    run_parser.add_argument("--agent", type=str, help="Run specific agent")
    run_parser.add_argument("--config", type=str, default="configs/ppp/ppp.run.yaml", help="Config path")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show run status")
    status_parser.add_argument("--run-id", type=str, help="Specific run ID")
    status_parser.add_argument("--db", type=str, default="data/ppp_progress.db", help="Database path")
    
    args = parser.parse_args()
    
    if args.command == "run":
        runner = PPPRunner(args.config)
        exit_code = runner.run_all()
        return exit_code
    
    elif args.command == "status":
        store = ProgressStore(args.db)
        
        if args.run_id:
            status = store.get_run_status(args.run_id)
            if status:
                print(f"Run: {status['run_id']}")
                print(f"  Agent: {status['agent_id']}")
                print(f"  Policy: {status['policy_id']}")
                print(f"  Started: {status['started_at']}")
                print(f"  Status: {status['status']}")
            else:
                print(f"Run not found: {args.run_id}")
        else:
            runs = store.list_runs()
            if runs:
                print("Recent runs:")
                for run in runs[:10]:
                    print(f"  {run['run_id']} [{run['status']}] - {run['agent_id']}")
            else:
                print("No runs found")
        
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
