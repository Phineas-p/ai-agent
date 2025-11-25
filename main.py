#uvicorn main:app --reload
from fastapi import FastAPI 
app = FastAPI()

@app.get("/")
def home():
    return {"msg":"hello"}

import requests, os
from fastapi import HTTPException
from dotenv import load_dotenv
from city_map import city_code #搜天气接口，把编码改成汉字

load_dotenv()
#搜索某天天气接口
WEATHER_KEY = os.getenv("WEATHER_KEY")
@app.get("/weather")
def weather(city: str):
    city = city_code.get(city, city)
    url=f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={WEATHER_KEY}"
    try:
        r = requests.get(url, timeout = 5)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    if not data.get("lives"):
        raise HTTPException(status_code=404, detail="城市编码错误或暂无数据")
    return data["lives"][0]

# ---------- 百度 AI 搜索 v2 ----------
BAIDU_APP_KEY = os.getenv("BAIDU_APP_KEY")
@app.get("/search")
def search(q:str, num: int = 5):
    BAIDU_SEARCH_URL = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    headers={
        "Content-Type": "application/json",            
        "Authorization": f"Bearer {BAIDU_APP_KEY}"
    }
    payload = {
        "messages": [{"role": "user", "content": q}],   
        "search_source": "baidu_search_v2",          
        "resource_type_filter": [{"type": "web", "top_k": min(num, 20)}]  
    }
    try:                                  
        r = requests.post(BAIDU_SEARCH_URL,            # 13 真正的“敲门”动作：POST+地址
                          json=payload,                # 14 把payload转成JSON发出去
                          headers=headers,             # 15 带上钥匙+Content-Type
                          timeout=5)                   # 16 最多等5秒，防止卡死
        r.raise_for_status()                           # 17 如果HTTP状态不是200就抛异常
        data = r.json()                                # 18 把百度返回的JSON转成Python字典
    except Exception as e:                             # 19 任何失败（网络、404、500）都进这里
        raise HTTPException(status_code=422, detail=str(e))  # 20 转成FastAPI友好错误，前端收到422
     # ⑬ 高德没数据时 lives 字段是空的，提前拦截
    if not data.get("references"):
        raise HTTPException(status_code=404, detail="未找到结果")
    return [{"title": it["title"], "url": it["url"]} for it in data["references"]]
    # ⑭ 只拿第一条实时天气（lives[0]）返回给前端，其余字段不要
    return data["lives"][0]