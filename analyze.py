import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

if __name__ == "__main__":
    report = f"""🚀 AI 硬件爆发趋势日报
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

这是系统发送的第一封测试邮件。

如果收到这封邮件，说明邮件通知功能已成功！

后续将逐步加入 Google Trends、Amazon、Kickstarter 数据分析。"""

    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if email and password:
        msg = MIMEText(report, "plain", "utf-8")
        msg["Subject"] = "🚀 AI硬件趋势日报 - 测试"
        msg["From"] = email
        msg["To"] = email

        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(email, password)
            server.sendmail(email, email, msg.as_string())
            server.quit()
            print("✅ 邮件发送成功！请查收邮箱（包括垃圾邮件箱）")
        except Exception as e:
            print("❌ 邮件发送失败:", str(e))
    else:
        print("❌ 未找到 EMAIL_ADDRESS 或 EMAIL_PASSWORD，请检查 Secret")
