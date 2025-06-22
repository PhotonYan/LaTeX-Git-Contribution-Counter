# LaTeX Git 作者贡献统计工具（LaTeX Git Contribution Counter）

这是一个基于 `git blame` 的 Python 工具，能够统计多人协作编写的 LaTeX 项目中，各位作者所贡献的**字符数或词数**。

非常适用于教材编写、课程讲义、科研文稿等需要明确作者写作投入比例的协作项目。

[English Version](./readme_cn.md)

---

## ✨ 功能特色

* ✅ 基于 `git blame` 实现**真实的作者归属行统计**
* ✅ 支持统计**词数**（默认）或**字符数**（通过 `--char` 切换）
* ✅ 可选择**剥除 LaTeX 命令**以获得纯净统计（“干净”内容 vs 原始总字数）
* ✅ 自动读取 `.fls` 文件，**递归获取所有实际参与编译的 .tex 文件**
* ✅ 若缺 `.fls` 文件，可自动调用 `xelatex` 或 `pdflatex` 补全
* ✅ 在终端输出**美观的表格统计**
* ✅ 自动保存日志文件 `count_word.log`
* ✅ 可选输出 `count_word.csv`，方便在 Excel / Python 中分析或绘图

---

## 🚀 使用方法

### 1. 安装依赖

```bash
pip install tabulate
```

### 2. 编译你的 LaTeX 工程（可选）

程序会自动调用 `xelatex` 或 `pdflatex` 编译生成 `.fls` 文件。你也可以手动执行：

```bash
xelatex -recorder main.tex
# 或
pdflatex -recorder main.tex
```

### 3. 运行脚本

```bash
python count_latex_contrib.py main.tex
```

### 可选参数：

| 参数           | 功能说明                          |
| ------------ | ----------------------------- |
| `--char`     | 将默认的“词数统计”切换为“字符数统计”          |
| `--nocsv`    | 不输出 `count_word.csv` 文件       |
| `--pdflatex` | 使用 `pdflatex` 而非 `xelatex` 编译 |
| `--fls`      | 手动指定 `.fls` 文件路径              |

---

## 📂 输出说明

### 终端输出：

```
=== Total Contributions (Without LaTeX Grammar) ===
╒══════════════════╤══════════════╤══════════╕
│ Author           │ Characters   │ Percent  │
╞══════════════════╪══════════════╪══════════╡
│ Photon           │ 131025       │ 44.85%   │
│ LittlePhoton     │ 52291        │ 17.90%   │
│ ...              │ ...          │ ...      │
╘══════════════════╧══════════════╧══════════╛
```

### 日志输出：

* `count_word.log`：文本格式日志，附时间戳
* `count_word.csv`：CSV 表格格式，格式为 `Author,Plain,Raw`，可用于 Excel 或数据分析

---

欢迎 PR 和建议！
