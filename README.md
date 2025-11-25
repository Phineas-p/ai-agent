# AI Agent Stage 1 - 天气 & 搜索接口

## 功能
- 实时天气查询 `/weather?city=北京`
- 实时网页搜索 `/search?q=人工智能`

## 一键运行（Windows 示例）
```powershell
# 1. 克隆项目
git clone https://github.com/<你的用户名>/ai-agent-stage1.git
cd ai-agent-stage1

# 2. 安装依赖（使用 uv）
uv pip install -r requirements.txt

# 3. 启动
uvicorn main:app --reload
