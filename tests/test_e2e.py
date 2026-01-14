import requests
import time
import sys

API_URL = "http://localhost:8000/v1"

def test_ingest_and_verify():
    print("1. Sending Chat Log...")
    payload = {
        "provider": "test_provider",
        "thread_id": "test_thread_123",
        "api_key": "e2e_test_user",
        "messages": [
            {"role": "user", "content": "My secret code is 42."}
        ]
    }
    
    try:
        res = requests.post(f"{API_URL}/ingest", json=payload)
        res.raise_for_status()
        task_id = res.json().get("task_id")
        print(f"   Success! Task ID: {task_id}")
    except Exception as e:
        print(f"   Failed to ingest: {e}")
        sys.exit(1)

    print("\n2. Waiting for Worker to Process (5s)...")
    time.sleep(5)

    print("\n3. Verifying Context Retrieval...")
    try:
        res = requests.get(f"{API_URL}/context?query=secret")
        res.raise_for_status()
        context = res.json().get("context")
        print(f"   Context Retrieved: {context}")
        # Note: Since we haven't implemented the actual vector search yet, 
        # this returns the placeholder. In a real test, we'd verify the content.
    except Exception as e:
        print(f"   Failed to get context: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_ingest_and_verify()
