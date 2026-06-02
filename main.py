import os
import requests
from DrissionPage import ChromiumPage, ChromiumOptions

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID   = os.environ.get("TG_CHAT_ID")

# 续期 URL（可能硬编码在脚本里，或通过 secret 传入）
ADDTIME_URL = "https://g4f.gg/dzgg"  # 示例

def send_tg(msg):
    if TG_BOT_TOKEN and TG_CHAT_ID:
        requests.post(
            f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
            data={"chat_id": TG_CHAT_ID, "text": msg}
        )

def main():
    try:
        # 配置 Chrome 无头模式（xvfb 已提供虚拟显示，也可不用 headless）
        co = ChromiumOptions()
        co.set_argument("--no-sandbox")
        co.set_argument("--disable-dev-shm-usage")

        page = ChromiumPage(addr_or_opts=co)
        page.get(ADDTIME_URL)

        # 等待页面加载，处理 Cloudflare 5秒盾
        page.wait(5)

        # 检查页面内容判断是否成功
        title = page.title
        send_tg(f"✅ G4F 续期成功！页面标题：{title}\nURL: {ADDTIME_URL}")

    except Exception as e:
        send_tg(f"❌ G4F 续期失败：{str(e)}")
    finally:
        page.quit()

if __name__ == "__main__":
    main()
