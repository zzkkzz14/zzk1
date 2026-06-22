import requests

url = "http://127.0.0.1:8000/skills/process"
headers = {"Content-Type": "application/json; charset=utf-8"}

# 测试中文查询
test_queries = [
    "写",
    "代码",
    "帮我写一个登录功能的代码",
    "实现一个API",
    "研究人工智能",
    "分析数据"
]

for query in test_queries:
    payload = {"query": query}
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        print(f"查询: '{query}' -> 匹配 Skill: {result.get('matched_skill', 'N/A')} ({result.get('skill_name', 'N/A')})")
    except Exception as e:
        print(f"查询: '{query}' -> 错误: {e}")
