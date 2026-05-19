import os
import requests
from datetime import datetime

if __name__ == "__main__":
    report = f"""# 🚀 AI 硬件爆发趋势日报 ({datetime.now().strftime('%Y-%m-%d %H:%M')})

**✅ 系统测试成功！**  
飞书通知功能已正常工作。

当前为测试版，之后我会帮你加上：
- Google Trends（美国搜索热度）
- Amazon AI 硬件热销榜单
- Kickstarter 爆发众筹项目

**每日北京时间下午 4 点** 将自动发送完整报告。"""

    webhook = os.getenv("LARK_WEBHOOK")
    if webhook:
        payload = {
            "msg_type": "markdown",
            "content": {"text": report}
        }
        try:
            r = requests.post(webhook, json=payload, timeout=15)
            print("发送状态码:", r.status_code)
            print("返回内容:", r.text[:300])
            if r.status_code == 200:
                print("✅ 飞书发送成功！")
            else:
                print("❌ 发送失败，状态码:", r.status_code)
        except Exception as e:
            print("发送异常:", e)
    else:
        print("❌ 未找到 LARK_WEBHOOK Secret")
