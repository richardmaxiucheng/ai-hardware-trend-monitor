import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

if __name__ == "__main__":
    report = f"""🚀 AI 硬件爆发趋势日报
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

系统已成功运行！
这是第一封测试邮件。

后续将自动添加：
- Google Trends 搜索热度
- Amazon 热销 AI 硬件
- Kickstarter 爆发项目

每天北京时间下午4点自动发送。"""

    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if email and password:
        msg = MIMEText(report, "plain", "utf-8")
        msg["Subject"] = "🚀 AI硬件趋势日报"
        msg["From"] = email
        msg["To"] = email

        try:
            # QQ邮箱使用 smtp.qq.com
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(email, password)
            server.sendmail(email, email, msg.as_string())
            server.quit()
            print("✅ 邮件发送成功！请查收邮箱")
        except Exception as e:
            print("❌ 邮件发送失败:", e)
    else:
        print("❌ 未找到邮箱 Secret")
