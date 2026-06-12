"""
NexaEdge Node Client — Beta P4
Heartbeat reporter + Task executor (simulated)

Usage:
    python node_client.py --token NXT-XXXX-XXXX-XXXX

Install deps:
    pip install supabase psutil
"""

import argparse
import time
import sys
import platform
import random
import hashlib
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
import os
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: set SUPABASE_URL and SUPABASE_KEY environment variables first.")
    sys.exit(1)
HEARTBEAT_INTERVAL = 30   # seconds
TASK_POLL_INTERVAL = 10   # seconds — check for new tasks every 10s

# ══════════════════════════════════════
# DEVICE STATS
# ══════════════════════════════════════
def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)

def get_temperature() -> float:
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return 0.0
        for key in ["coretemp", "cpu_thermal", "k10temp", "acpitz"]:
            if key in temps:
                return temps[key][0].current
        first = list(temps.values())
        if first:
            return first[0][0].current
    except Exception:
        pass
    return 0.0

def get_battery() -> int:
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

# ══════════════════════════════════════
# SIMULATED TASK EXECUTION
# ══════════════════════════════════════
def simulate_slm_inference(payload: str) -> str:
    """Simulate SLM inference (Phi-3 mini style)."""
    time.sleep(random.uniform(0.5, 1.5))  # simulate compute time
    input_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    return f"[SIM] slm_inference OK | input_hash={input_hash} | tokens=128 | latency={random.uniform(2.1, 4.8):.1f}ms"

def simulate_rlhf_validation(payload: str) -> str:
    """Simulate RLHF label validation."""
    time.sleep(random.uniform(0.3, 0.8))
    score = round(random.uniform(0.72, 0.99), 4)
    return f"[SIM] rlhf_validation OK | score={score} | chunks=32 | consensus=True"

def simulate_zk_proof(payload: str) -> str:
    """Simulate ZK proof generation."""
    time.sleep(random.uniform(1.0, 2.5))
    proof_hash = hashlib.sha256((payload + str(time.time())).encode()).hexdigest()[:32]
    return f"[SIM] zk_proof OK | proof={proof_hash} | verified=True"

TASK_EXECUTORS = {
    "slm_inference":  simulate_slm_inference,
    "rlhf_validation": simulate_rlhf_validation,
    "zk_proof":       simulate_zk_proof,
}

def execute_task(task_type: str, payload: str) -> str:
    executor = TASK_EXECUTORS.get(task_type)
    if executor:
        return executor(payload or "default_payload")
    return f"[SIM] unknown_task_type={task_type}"

# ══════════════════════════════════════
# NODE / HEARTBEAT
# ══════════════════════════════════════
def validate_token(supabase, token: str) -> bool:
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
    try:
        supabase.table("nodes").update({
            "status": "offline",
            "last_seen": datetime.now(timezone.utc).isoformat(),
        }).eq("node_token", token).execute()
        print("\n  [·] Node marked offline. Goodbye.")
    except Exception as e:
        print(f"  [!] Failed to set offline: {e}")

def send_heartbeat(supabase, token: str, tasks: int) -> bool:
    try:
        cpu  = get_cpu_usage()
        temp = get_temperature()
        batt = get_battery()

        supabase.table("heartbeats").insert({
            "node_token":      token,
            "cpu_usage":       cpu,
            "temperature":     temp,
            "battery_level":   batt,
            "tasks_completed": tasks,
            "reported_at":     datetime.now(timezone.utc).isoformat(),
        }).execute()

        supabase.table("nodes").update({
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "status": "online",
        }).eq("node_token", token).execute()

        warn = " ⚠ TEMP HIGH — task queue paused" if temp >= 39 else ""
        print(
            f"  [{datetime.now().strftime('%H:%M:%S')}] ♥  "
            f"CPU {cpu:4.1f}%  "
            f"Temp {temp:4.1f}°C{warn}  "
            f"Batt {batt}%  "
            f"Tasks done: {tasks}"
        )
        return True, temp

    except Exception as e:
        print(f"  [!] Heartbeat failed: {e}")
        return False, 0.0

# ══════════════════════════════════════
# TASK QUEUE
# ══════════════════════════════════════
def poll_and_execute_task(supabase, token: str) -> bool:
    """
    Poll for one pending task, claim it, execute it, upload result.
    Returns True if a task was executed.
    """
    try:
        # 1. Fetch one pending task not yet assigned
        res = (supabase.table("tasks")
               .select("*")
               .eq("status", "pending")
               .is_("assigned_to", "null")
               .limit(1)
               .execute())

        if not res.data:
            return False  # no tasks available

        task = res.data[0]
        task_id   = task["id"]
        task_type = task.get("task_type", "slm_inference")
        payload   = task.get("payload", "")

        # 2. Claim the task (set assigned_to = our token)
        supabase.table("tasks").update({
            "status":      "assigned",
            "assigned_to": token,
        }).eq("id", task_id).execute()

        print(f"  [{datetime.now().strftime('%H:%M:%S')}] ▶  Task #{task_id} claimed — type: {task_type}")

        # 3. Execute
        result = execute_task(task_type, payload)

        # 4. Upload result
        supabase.table("tasks").update({
            "status":       "completed",
            "result":       result,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", task_id).execute()

        print(f"  [{datetime.now().strftime('%H:%M:%S')}] ✓  Task #{task_id} completed")
        print(f"              └─ {result}")
        return True

    except Exception as e:
        print(f"  [!] Task execution error: {e}")
        return False

def inject_demo_task(supabase):
    """Insert a demo task so the node has something to execute."""
    try:
        task_types = ["slm_inference", "rlhf_validation", "zk_proof"]
        supabase.table("tasks").insert({
            "task_type": random.choice(task_types),
            "status":    "pending",
            "payload":   f"demo_payload_{random.randint(1000,9999)}",
        }).execute()
    except Exception:
        pass

# ══════════════════════════════════════
# MAIN
# ══════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="NexaEdge Node Client — Beta P4"
    )
    parser.add_argument(
        "--token", "-t",
        required=True,
        help="Your node token (e.g. NXT-6AM9-GG5H-UKES)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Auto-inject demo tasks every 60s for testing"
    )
    args = parser.parse_args()
    token = args.token.strip().upper()

    print()
    print("  ●  NexaEdge Node Client — Beta P4")
    print("  ─────────────────────────────────────")
    print(f"  Token   : {token}")
    print(f"  Device  : {platform.node()} ({platform.system()} {platform.release()})")
    print(f"  Heartbeat: every {HEARTBEAT_INTERVAL}s")
    print(f"  Task poll: every {TASK_POLL_INTERVAL}s")
    if args.demo:
        print("  Mode    : DEMO (auto-injecting tasks)")
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
        print("  Token not found. Check your token at the Node Portal.")
        sys.exit(1)
    print("OK")

    # Set online
    set_node_online(supabase, token)
    print("  Status : ONLINE ✓")
    print()
    print("  Running — heartbeat + task executor (Ctrl+C to stop):")
    print()

    tasks_done      = 0
    last_heartbeat  = 0
    last_task_poll  = 0
    last_demo_inject = 0

    try:
        while True:
            now = time.time()

            # ── Heartbeat ──────────────────────────
            if now - last_heartbeat >= HEARTBEAT_INTERVAL:
                ok, temp = send_heartbeat(supabase, token, tasks_done)
                last_heartbeat = now
                thermal_pause = temp >= 39
            else:
                thermal_pause = False

            # ── Demo task injection ────────────────
            if args.demo and (now - last_demo_inject >= 60):
                inject_demo_task(supabase)
                last_demo_inject = now

            # ── Task polling ───────────────────────
            if not thermal_pause and (now - last_task_poll >= TASK_POLL_INTERVAL):
                executed = poll_and_execute_task(supabase, token)
                if executed:
                    tasks_done += 1
                last_task_poll = now

            time.sleep(1)

    except KeyboardInterrupt:
        set_node_offline(supabase, token)

if __name__ == "__main__":
    main()
