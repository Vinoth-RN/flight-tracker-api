import subprocess
import os
import sys
import json

# Adding project root to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

def run_spider(flight_number: str, flight_date: str):
    print(f"[run_spider]  Launching subprocess for flight_number={flight_number}, flight_date={flight_date}")
    
    # Set PYTHONPATH so subprocess can import `app` properly
    env = os.environ.copy()
    env["PYTHONPATH"] = BASE_DIR

    try:
        result = subprocess.run(
            [
                sys.executable,
                os.path.join(BASE_DIR, "app", "scraper", "run_spider_entry.py"),
                flight_number,
                flight_date
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
            env=env
        )
        print("[run_spider] Subprocess completed successfully")
        print("[run_spider] STDOUT:")
        print(result.stdout.strip())

        try:
            return json.loads(result.stdout.strip()) 
        except Exception as e:
            print(f"[run_spider]  Failed to parse JSON output: {e}")
            return None

    except subprocess.TimeoutExpired:
        print("[run_spider]  Subprocess timed out!")
    except subprocess.CalledProcessError as e:
        print(f"[run_spider]  Subprocess failed with stderr:\n{e.stderr}")
    except Exception as e:
        print(f"[run_spider]  Unexpected error: {e}")

    return None
