# LLM 多功能助手 

**环境依赖**：Python 3.8+, `requests`, `sympy`, `pandas`（根据实际依赖修改）

---

## 项目结构
```bash
.
├── main.py                  # 总入口：集成所有功能
├── weather_tools/           # 天气查询模块
│   ├── full_version.py      # 基础三轮调用（输出详细过程）
│   └── simplified.py        # 简化版两轮调用（直接输出结果）
├── movie_qa/                # 电影问答模块
│   └── douban_top10.py      # 豆瓣Top10电影短评问答
├── stock_query/             # 股票查询模块
│   └── daily_stock.py       # 按日期查询股票数据
├── calculator/              # 计算工具
│   └── safe_calculate.py    # 安全数学计算
└── README.md                # 说明文档
```

---

## 功能说明

### 1. 天气查询工具
#### 基础三轮调用（完整日志）
- **文件**：`weather_tools/full_version.py`  
- **功能**：  
  1. 第一轮：提取用户输入中的城市和日期（如“南京明天天气” → `location=南京, date=明天`）。  
  2. 第二轮：调用思知天气API获取实时数据。  
  3. 第三轮：生成自然语言回复。  
- **输出示例**：  
  ```python
  第一轮调用结果：{'location': '南京市', 'date': '明天'}
  工具输出信息：南京明天天气：多云，温度：25℃
  最终答案：南京明天预计多云，气温25℃，适合外出。
  ```

#### 简化版两轮调用（直接输出）
- **文件**：`weather_tools/simplified.py`  
- **区别**：跳过中间日志，直接返回最终结果。  
- **输出示例**：  
  ```python
  南京明天预计多云，气温25℃。
  ```

---

### 2. 电影问答工具
- **文件**：`movie_qa/douban_top10.py`  
- **功能**：  
  - 支持查询豆瓣Top10电影的短评（如“《肖申克的救赎》有哪些影评？”）。  
  - **限制**：暂不支持电影比较（如“A和B哪部评分更高”）。  
- **数据来源**：本地存储的豆瓣Top10电影JSON文件（需提前爬取）。  
- **输出示例**：  
  ```python
  《肖申克的救赎》热门短评：  
  1. 用户A：希望让人自由。  
  2. 用户B：经典中的经典。
  ```

---

### 3. 股票查询工具
- **文件**：`stock_query/daily_stock.py`  
- **功能**：  
  - 按日期查询股票数据（如“腾讯控股2023年10月股价”）。  
  - **API**：需替换为你的金融数据接口（如Tushare）。  
- **输出示例**：  
  ```python
  腾讯控股(0700.HK) 2023-10-11 收盘价：320.5港元，涨幅：+1.2%。
  ```

---

### 4. 安全计算工具
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

---

## 运行步骤
1. **安装依赖**：  
   ```bash
   pip install requests sympy pandas
   ```

2. **配置API密钥**：  
   - 在对应模块中替换为你的天气/股票API密钥（如思知天气、Tushare）。

3. **运行单个工具**：  
   ```bash
   python weather_tools/simplified.py
   ```

4. **运行总入口**：  
   ```bash
   python main.py --tool [weather|movie|stock|calc] --query "你的输入"
   ```

---

## 注意事项
1. **天气API限制**：免费版思知天气仅支持实时数据，历史日期需升级套餐。  
2. **电影数据**：确保`douban_top10.json`文件已放入`movie_qa/`目录。  
3. **股票数据**：若使用Tushare，需注册并获取Token。  
4. **计算安全**：禁止直接执行用户输入，始终使用`sympy`解析。

---

## 提交文件
- 压缩包内容：  
  ```
  学号_姓名_LLM助手.zip
  ├── main.py
  ├── weather_tools/
  ├── movie_qa/
  ├── stock_query/
  ├── calculator/
  ├── README.md
  └── 课程设计报告.docx
  ```****