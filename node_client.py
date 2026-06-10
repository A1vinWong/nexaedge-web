"""
NexaEdge Node Client — Beta P3
Heartbeat reporter: sends device stats to Supabase every 30 seconds.

Usage:
    python node_client.py --token NXT-XXXX-XXXX-XXXX

Install deps:
    pip install supabase psutil
"""

import argparse
import time
import sys
import platform
from datetime import datetime, timezone

try:
    import psutil
except ImportError:
    print("Missing dependency. Run: pip install psutil supabase")
    sys.exit(1)

try:
    from supabase import create_client
except ImportError:
    print("Missing dependency. Run: pip install supabase psutil")
    sys.exit(1)

# ══════════════════════════════════════
# CONFIG
# ══════════════════════════════════════
SUPABASE_URL = "https://nfafzigmcdybgbxdtymf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mYWZ6aWdtY2R5YmdieGR0eW1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5ODE3NTMsImV4cCI6MjA5NjU1Nzc1M30.ZIX3sByZ8yQSDGFr-o24CjIXwZ5UsB4rMB3jculLtv0"
HEARTBEAT_INTERVAL = 30  # seconds

# ══════════════════════════════════════
# HELPERS
# ══════════════════════════════════════
def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)

def get_temperature() -> float:
    """Get CPU temperature. Returns 0.0 if not available (Windows/some Mac)."""
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return 0.0
        # Try common keys
        for key in ["coretemp", "cpu_thermal", "k10temp", "acpitz"]:
            if key in temps:
                return temps[key][0].current
        # Fallback: first available
        first = list(temps.values())
        if first:
            return first[0][0].current
    except Exception:
        pass
    return 0.0

def get_battery() -> int:
    """Get battery level 0-100. Returns 100 if on desktop (no battery)."""
    try:
        batt = psutil.sensors_battery()
        if batt:
            return int(batt.percent)
    except Exception:
        pass
    return 100

def get_device_info() -> dict:
    return {
        "device_model": platform.node() or "unknown",
        "os_version": f"{platform.system()} {platform.release()}",
    }

def validate_token(supabase, token: str) -> bool:
    """Check that this token exists in the nodes table."""
    try:
        res = (supabase.table("nodes")
               .select("id")
               .eq("node_token", token)
               .execute())
        return len(res.data) > 0
    except Exception as e:
        print(f"  [!] Token validation error: {e}")
        return False

def set_node_online(supabase, token: str):
    """Update node status to online and record device info."""
    try:
        info = get_device_info()
        supabase.table("nodes").update({
            "status": "online",
            "device_model": info["device_model"],
            "os_version": info["os_version"],
            "last_seen": datetime.now(timezone.utc).isoformat(),
        }).eq("node_token", token).execute()
    except Exception as e:
        print(f"  [!] Failed to set online: {e}")

def set_node_offline(supabase, token: str):
    """Update node status to offline on clean exit."""
    try:
        supabase.table("nodes").update({
            "status": "offline",
            "last_seen": datetime.now(timezone.utc).isoformat(),
        }).eq("node_token", token).execute()
        print("\n  [·] Node marked offline. Goodbye.")
    except Exception as e:
        print(f"  [!] Failed to set offline: {e}")

def send_heartbeat(supabase, token: str, tasks: int) -> bool:
    """Send one heartbeat row to the heartbeats table."""
    try:
        cpu   = get_cpu_usage()
        temp  = get_temperature()
        batt  = get_battery()

        supabase.table("heartbeats").insert({
            "node_token":        token,
            "cpu_usage":         cpu,
            "temperature":       temp,
            "battery_level":     batt,
            "tasks_completed":   tasks,
            "reported_at":       datetime.now(timezone.utc).isoformat(),
        }).execute()

        # Update last_seen on nodes table
        supabase.table("nodes").update({
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "status": "online",
        }).eq("node_token", token).execute()

        # Thermal warning
        warn = " ⚠ TEMP HIGH" if temp >= 39 else ""
        print(
            f"  [{datetime.now().strftime('%H:%M:%S')}] "
            f"CPU {cpu:4.1f}%  "
            f"Temp {temp:4.1f}°C{warn}  "
            f"Batt {batt}%  "
            f"Tasks {tasks}"
        )
        return True

    except Exception as e:
        print(f"  [!] Heartbeat failed: {e}")
        return False

# ══════════════════════════════════════
# MAIN
# ══════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="NexaEdge Node Client — heartbeat reporter"
    )
    parser.add_argument(
        "--token", "-t",
        required=True,
        help="Your node token (e.g. NXT-6AM9-GG5H-UKES)"
    )
    args = parser.parse_args()
    token = args.token.strip().upper()

    print()
    print("  ●  NexaEdge Node Client — Beta P3")
    print("  ─────────────────────────────────")
    print(f"  Token  : {token}")
    print(f"  Device : {platform.node()} ({platform.system()} {platform.release()})")
    print(f"  Interval: {HEARTBEAT_INTERVAL}s")
    print()

    # Connect
    print("  Connecting to Supabase...", end=" ")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("OK")
    except Exception as e:
        print(f"FAILED\n  Error: {e}")
        sys.exit(1)

    # Validate token
    print("  Validating token...", end=" ")
    if not validate_token(supabase, token):
        print("INVALID")
        print()
        print("  This token was not found in the database.")
        print("  Please check your token at the Node Portal.")
        sys.exit(1)
    print("OK")

    # Set online
    set_node_online(supabase, token)
    print("  Status: ONLINE ✓")
    print()
    print("  Sending heartbeats (Ctrl+C to stop):")
    print()

    tasks = 0
    try:
        while True:
            ok = send_heartbeat(supabase, token, tasks)
            if ok:
                tasks += 1
            time.sleep(HEARTBEAT_INTERVAL)

    except KeyboardInterrupt:
        set_node_offline(supabase, token)

if __name__ == "__main__":
    main()
