# LaTeX Git Contribution Counter

A Python tool to **count character or word contributions** of each author in a LaTeX project, based on `git blame`.

This is particularly useful for collaborative textbook or research note projects where authorship and writing effort need to be measured quantitatively.

如果你需要[[简体中文]](./readme_cn.md)版ReadMe点[这里](./readme_cn.md)。

---

## ✨ Features

- ✅ Counts by **actual authorship** using `git blame`
- ✅ Supports both **words** (default) and **characters** (`--char`)
- ✅ Removes LaTeX syntax when requested
- ✅ Reads `.fls` to trace all `.tex` files recursively
- ✅ Automatically compiles `.tex` with `-recorder` if `.fls` is missing
- ✅ Outputs human-readable **table in terminal** 
- ✅ Logs results to `count_word.log`
- ✅ Outputs CSV (`count_word.csv`) for plotting or analysis

---

## 🚀 Usage

### 1. Installation

Install dependencies:

```bash
pip install tabulate
````

### 2. Compile your LaTeX project (optional)

If `.fls` file is not found, the script will automatically run `xelatex` or `pdflatex` twice.

You may also pre-compile manually:

```bash
xelatex -recorder main.tex
# or
pdflatex -recorder main.tex
```

### 3. Run the script

```bash
python count_latex_contrib.py main.tex
```

### Optional flags:

| Flag         | Description                         |
| ------------ | ----------------------------------- |
| `--char`     | Count characters instead of words   |
| `--nocsv`    | Disable output of `count_word.csv`  |
| `--pdflatex` | Use `pdflatex` instead of `xelatex` |
| `--fls`      | Manually specify `.fls` path        |

---

## 📂 Output

### Terminal :

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

### Log files:

* `count_word.log`: Plain text result with timestamp
* `count_word.csv`: Optional CSV (`Author,Plain,Raw`) for Excel/plotting

---

## 📄 License

MIT License. Use freely, attribution appreciated.

---

## 👤 Author

Created by [PhotonYan](https://github.com/PhotonYan) for collaborative academic writing and fair contribution analysis.

Contributions and suggestions welcome!

