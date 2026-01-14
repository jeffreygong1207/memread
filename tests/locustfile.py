from locust import HttpUser, task, between
import random

class ChatUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def ingest_chat(self):
        payload = {
            "provider": "chatgpt.com",
            "thread_id": f"thread_{random.randint(1, 1000)}",
            "api_key": "demo-user-key",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"},
                {"role": "assistant", "content": "I am fine, thank you."}
            ]
        }
        self.client.post("/v1/ingest", json=payload)

    @task(1)
    def get_context(self):
        self.client.get("/v1/context?query=python")
