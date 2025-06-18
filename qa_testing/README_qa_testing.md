# 有机电催化问答测试脚本

这个项目包含多个测试脚本，用于生成英文有机电催化领域的问题，获取回答并进行引用分析。

## 脚本说明

### 1. 完整测试脚本 (`test_organic_electrocatalysis_qa.py`)

**功能：** 测试10个完整的有机电催化问题，使用真实的API调用生成答案

**特点：**
- 使用真实的专家系统生成答案
- 包含完整的引用分析
- 生成详细的测试报告
- 支持JSON和文本格式输出

**使用方法：**
```bash
python3 test_organic_electrocatalysis_qa.py
```

**输出：**
- `test_output/` 目录
- 每个问题的答案文件 (`answer_01.md`, `answer_02.md`, ...)
- 每个问题的引用分析 (`citation_analysis_01.txt`, `citation_analysis_02.txt`, ...)
- 汇总报告 (`test_summary.json`, `test_summary_report.txt`)

### 2. 快速测试脚本 (`quick_test_qa.py`)

**功能：** 快速测试前3个问题，减少API调用次数

**特点：**
- 只测试前3个问题
- 适合快速验证功能
- 减少API使用量

**使用方法：**
```bash
python3 quick_test_qa.py
```

**输出：**
- `quick_test_output/` 目录
- 3个问题的答案和引用分析
- 快速汇总报告

### 3. 演示脚本 (`demo_qa_test.py`)

**功能：** 使用模拟数据演示引用分析功能

**特点：**
- 不依赖API调用
- 使用预设的模拟数据
- 展示不同引用覆盖率的情况
- 快速演示功能

**使用方法：**
```bash
python3 demo_qa_test.py
```

**输出：**
- `demo_output/` 目录
- 10个模拟问题的答案和引用分析
- 演示汇总报告

## 测试问题列表

脚本中包含以下10个英文有机电催化领域的问题：

1. **CO2电还原机制** - What are the key mechanisms of CO2 electroreduction on copper-based catalysts?
2. **配位环境影响** - How does the coordination environment affect the performance of nickel-based electrocatalysts for alcohol oxidation?
3. **C-H官能化进展** - What are the recent advances in electrochemical C-H functionalization of aromatic compounds?
4. **选择性改进** - How can we improve the selectivity of electrochemical reduction of carbonyl compounds?
5. **电解质添加剂** - What role do electrolyte additives play in organic electrocatalysis?
6. **表面结构影响** - How does the surface structure of platinum catalysts influence organic molecule oxidation?
7. **杂环化合物合成** - What are the challenges and solutions for electrochemical synthesis of heterocyclic compounds?
8. **高电流密度** - How can we achieve high current density in organic electrosynthesis?
9. **生物质氧化机理** - What are the mechanistic insights into electrochemical oxidation of biomass-derived compounds?
10. **pH影响** - How does the pH of electrolyte affect the reaction pathways in organic electrocatalysis?

## 输出文件说明

### 答案文件 (`answer_XX.md`)
- 包含问题和答案
- 格式化的Markdown文件
- 包含基本的分析信息

### 引用分析文件 (`citation_analysis_XX.txt`)
- 详细的引用分析报告
- 包含处理时间、上下文片段数等信息
- 被引用片段的详细信息
- 引用覆盖率统计

### 汇总报告
- **JSON格式** (`test_summary.json`, `demo_results.json`)：结构化的详细数据
- **文本格式** (`test_summary_report.txt`, `demo_summary.txt`)：人类可读的汇总报告

## 演示结果示例

### 引用覆盖率分布
```
📈 引用覆盖率分布:
   100%: 3 个问题
   80%: 3 个问题
   60%: 2 个问题
   40%: 2 个问题
```

### 平均统计
- **平均处理时间**: 0.000 秒（演示脚本）
- **平均引用覆盖率**: 74.00%
- **成功测试**: 10/10
- **失败测试**: 0/10

## 引用分析指标

### 1. 基本统计
- **总上下文片段数**: 检索到的所有片段数量
- **被引用的片段数**: 在答案中被引用的片段数量
- **引用覆盖率**: 被引用片段占总片段的百分比
- **未使用的片段数**: 未被引用的片段数量

### 2. 详细分析
- **被引用的片段详情**: 每个被引用片段的信息
  - 来源文件
  - 片段索引
  - 引用次数
  - 内容预览

### 3. 质量评估
- **完整性**: 是否充分利用了检索到的上下文
- **平衡性**: 引用是否均匀分布
- **相关性**: 引用的片段是否与问题相关

## 使用建议

### 1. 开发阶段
- 使用 `demo_qa_test.py` 快速验证功能
- 不依赖外部API，适合频繁测试

### 2. 功能验证
- 使用 `quick_test_qa.py` 进行小规模测试
- 验证API集成和引用分析功能

### 3. 完整评估
- 使用 `test_organic_electrocatalysis_qa.py` 进行全面测试
- 获取完整的性能指标和质量评估

## 注意事项

### 1. API限制
- 完整测试脚本会进行10次API调用
- 建议在API配额充足时使用
- 脚本包含延迟机制避免频率限制

### 2. 文件权限
- 确保有写入权限来创建输出目录
- 输出文件会覆盖同名文件

### 3. 依赖要求
- 需要正确配置专家系统
- 确保所有依赖包已安装
- 需要有效的API密钥（完整测试）

## 扩展功能

### 1. 自定义问题
可以修改脚本中的问题列表来测试不同的问题：

```python
self.questions = [
    "Your custom question here?",
    "Another custom question?",
    # ... 更多问题
]
```

### 2. 自定义分析
可以扩展分析功能来包含更多指标：

```python
# 在结果中添加自定义指标
result['custom_metric'] = calculate_custom_metric(answer, context)
```

### 3. 批量处理
可以修改脚本来处理大量问题：

```python
# 从文件读取问题列表
with open('questions.txt', 'r') as f:
    questions = [line.strip() for line in f.readlines()]
```

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥配置
   - 确认网络连接
   - 检查API配额

2. **文件保存失败**
   - 检查目录权限
   - 确认磁盘空间
   - 检查文件路径

3. **引用分析错误**
   - 检查上下文数据格式
   - 确认引用格式正确
   - 查看日志输出

### 调试模式

启用详细日志来调试问题：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

这些测试脚本为评估有机电催化专家系统的性能和质量提供了全面的工具，帮助了解系统在不同问题类型上的表现和引用分析能力。 