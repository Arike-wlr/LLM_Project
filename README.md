# LLM 多功能助手 

## 环境依赖

运行此项目需要以下环境和依赖：

- **Python 版本**: 3.8 或更高（我使用3.13.2版本）

- **依赖库**:

  - os（python标准库模块）

  - datetime（python标准库模块）

  - requests

  - json

  - python-dotenv

  - sympy

  - numpy

    ###### 一键安装项目依赖：

    ```
    python -m pip install -r requirements.txt
    ```

- **IDE**: PyCharm 2024.3.5（推荐）

---

## 项目结构
```bash
├── main.py                  # 集成所有功能的LLM助手
├── current_weather_3_ans.py # 天气查询,根据文档要求实现的最基础的三轮调用出结果，输出每轮结果
├── current_weather.py       # 天气查询简化版，两轮调用（直接输出最终回答，以下均同）
├── analyse_movie.py         # 电影问答
├── finance_analyse.py       # 股票查询
├── mathenatics.py           # 计算工具
└── README.md                # 说明文档
```

---

## 功能说明与运行步骤

### 1. 天气查询工具
#### 基础三轮调用（完整日志）
- **文件**：`current_weather_3_ans.py`  
- **功能**：  
  1. 第一轮：提取用户输入中的城市（由于免费api限制，只能获取当前天气）。  
  2. 第二轮：调用天气API获取实时数据。  
  3. 第三轮：生成自然语言回复。  
- **运行方法**：  
  
  ```bash
  python current_weather_3_ans.py
  ```

#### 简化版两轮调用（直接输出）
- **文件**：`current_weather.py`  
- **区别**：隐藏中间日志，直接返回最终自然语言结果。  
- **运行方法**：  
  
  ```bash
  python current_weather.py
  ```

---

### 2. 电影问答工具
- **文件**：`analyse_movie.py`  
- **功能**：  
  - 支持查询豆瓣Top10电影的基本信息
  - 支持查询豆瓣Top10电影的部分短评。  
  - **限制**：一次提问仅设计一部电影，暂不支持同时分析多部电影。  
- **数据来源**：本地存储的豆瓣Top10电影JSON文件（已提前爬取）。  
- **运行方法**：  
  
  ```bash
  python analyse_movie.py
  ```

---

### 3. 股票查询工具
- **文件**：`stock_query/daily_stock.py`  

- **功能**：  
  - 按日期和股票代码查询股票数据。  
  
- **输出示例**：  
  ```python
  腾讯控股(0700.HK) 2023-10-11 收盘价：320.5港元，涨幅：+1.2%。
  ```

---

### 4. 数学计算工具
- **文件**：`calculator/safe_calculate.py`  
- **功能**：  
  - 支持大数运算、三角函数等（如“2^100”或“sin(pi/6)”）。  
  - **安全机制**：白名单限制可用的函数和运算符。  
- **输出示例**：  
  ```python
  2^100 = 1267650600228229401496703205376
  ```

---

### 5. 总入口（集成所有功能）
- **文件**：`main.py`  
- **功能**：  
  - 通过命令行选择工具类型（天气/电影/股票/计算）。  
  - 示例运行：  
    ```bash
    python main.py 
    ```

