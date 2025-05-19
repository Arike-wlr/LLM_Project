# LLM 多功能助手 

## 环境依赖

运行此项目需要以下环境和依赖：

- **Python 版本**: 3.8 或更高（我使用3.13.2版本）

- **依赖库**:

  - os（python标准库模块，不需安装）

  - datetime（python标准库模块，不需安装）

  - json(python标准库模块，不需安装)

  - requests

  - python-dotenv

  - sympy

  - numpy

    ###### 一键安装项目依赖（若安装失败可多次尝试）：

    ```bash
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
├── analyse_movies.py
├── finance_analyse.py       # 股票查询
├── mathenatics.py           # 计算工具
├── movies.json              #电影信息文件
├── movie_info
│  └──movie(1~10).json
├── short_comments
│  └──comments(1~30).json
├── requirements.txt         #需安装的python库
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
  -也可以获取当前时间
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
#### 单电影分析工具
- **文件**：`analyse_movie.py`  
- **功能**：  
  - 支持查询豆瓣Top10电影的基本信息
  - 支持查询豆瓣Top10电影的部分短评。  
  - **限制**：一次提问仅涉及一部电影，暂不支持同时分析多部电影。  
- **数据来源**：本地存储的豆瓣Top10电影及每部电影的60条短评，以JSON文件存储（已提前爬取）。  
- **运行方法**：  
  
  ```bash
  python analyse_movie.py
  ```

#### 多个电影综合分析工具
- **文件**：`analyse_movies.py`  
- **功能**：  
  - 支持查询并比较分析豆瓣Top10电影的基本信息
- **数据来源**：本地存储的豆瓣Top10电影JSON文件。  
- **运行方法**：  
  
  ```bash
  python analyse_movie.py
  ```

---

### 3. 股票查询工具
- **文件**：`finance_analyse.py`  

- **功能**：  
  - 按日期和股票代码查询股票数据。
- **运行方法**：  
  
  ```bash
  python finance_analyse.py 
  ```

---

### 4. 数学计算工具
- **文件**：`mathenatics.py`  
- **功能**：  
  - 支持大数运算、三角函数等初等函数运算（如“2^100”或“sin(pi/6)”）。
  - 支持数学分析相关运算：极限，一元函数求导（默认x->0），一元函数积分（默认0~正无穷）
  - 支持线性代数相关矩阵运算：求逆，求行列式，求两个矩阵的乘积
- **运行方法**：  
  
  ```bash
  python mathenatics.py
  ```

---

### 5. 总入口（集成所有功能）
- **文件**：`main.py`  
- **功能**：  
  - 集成以上所有功能：时间/天气/电影/股票/计算，直接输出最终回答。
**运行方法**：  

```bash
python main.py 	
```
