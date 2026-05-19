import os
import requests

if __name__ == "__main__":
    text = "✅ 测试消息\n这是从 GitHub 发送的测试\n请检查是否收到"

    webhook = os.getenv("LARK_WEBHOOK")
    if webhook:
        payload = {
            "msg_type": "text",
            "content": {"text": text}
        }
        requests.post(webhook, json=payload)
        print("已尝试发送")
