import os
import re
import datetime
import subprocess
from collections import defaultdict
import argparse
from tabulate import tabulate

def strip_latex_commands(line):
    line = re.sub(r'\$.*?\$', '', line) 
    line = re.sub(r'\\[a-zA-Z@]+(\[[^\]]*\])?(\{[^}]*\})*', '', line)
    return line

def count_chars(text):
    if count_char:
        cleaned = re.sub(r'\s+', '', text)
        return len(cleaned)
    else:
        return len(re.findall(r'\b\w+\b', text))

def get_blame_authors(filename):
    """
    Return a dict mapping line numbers (1-based) to author names using git blame.
    """
    cmd = [
    'git', 'blame',
    '-w', '-e',
    '-M',      
    '-C', '-C',
    '--line-porcelain',
    filename
    ]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    authors = {}
    current_line = 0
    current_author = None
    for line in out.splitlines():
        if line.startswith('author '):
            current_author = line[len('author '):]
        elif line.startswith('\t'):
            current_line += 1
            authors[current_line] = current_author
    return authors

def aggregate_contributions(file_list):
    total_counts = defaultdict(int)
    total_counts_all = defaultdict(int)
    log_lines = []

    for filepath in file_list:
        authors = get_blame_authors(filepath)
        if not authors:
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        per_file_counts = defaultdict(int)
        per_file_counts_all = defaultdict(int)

        for i, raw_line in enumerate(lines, start=1):
            author = authors.get(i, 'Unknown')
            text = strip_latex_commands(raw_line)
            text_all = raw_line
            chars = count_chars(text)
            chars_all = count_chars(text_all)
            per_file_counts[author] += chars
            total_counts[author] += chars
            per_file_counts_all[author] += chars_all
            total_counts_all[author] += chars_all

        print(f"File: {os.path.relpath(filepath)}")
        for author, chars in sorted(per_file_counts.items(), key=lambda x: -x[1]):
            print(f"  {author}: {chars} characters")
        print(f"Count every char:")
        for author, chars in sorted(per_file_counts_all.items(), key=lambda x: -x[1]):
            print(f"  {author}: {chars} characters")
        print()

    total_plain = sum(total_counts.values())
    total_raw = sum(total_counts_all.values())

    plain_table = []
    for author, chars in sorted(total_counts.items(), key=lambda x: -x[1]):
        ratio = chars / total_plain * 100 if total_plain else 0
        plain_table.append([author, chars, f"{ratio:.2f}%"])

    print("=== Total Contributions (Without LaTeX Grammar) ===")
    print(tabulate(plain_table, headers=["Author", "Characters", "Percent"], tablefmt="fancy_grid"))

    # 构建“含所有符号”的原始表格
    raw_table = []
    for author, chars in sorted(total_counts_all.items(), key=lambda x: -x[1]):
        ratio = chars / total_raw * 100 if total_raw else 0
        raw_table.append([author, chars, f"{ratio:.2f}%"])

    print("=== Total Contributions ===")
    print(tabulate(raw_table, headers=["Author", "Characters", "Percent"], tablefmt="fancy_grid"))

    print("=== Total Characters Count ===")
    print(f"Plain: {total_plain}, Raw: {total_raw}.")



    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_lines.append(f"=== Total Contributions (Without LaTeX Grammar) ({timestamp}) ===")
    for author, chars in sorted(total_counts.items(), key=lambda x: -x[1]):
        ratio = chars / total_plain * 100 if total_plain else 0
        log_lines.append(f"{author}: {chars} characters ({ratio:.2f}%)")

    log_lines.append(f"=== Total Contributions ({timestamp}) ===")
    for author, chars in sorted(total_counts_all.items(), key=lambda x: -x[1]):
        ratio = chars / total_raw * 100 if total_raw else 0
        log_lines.append(f"{author}: {chars} characters ({ratio:.2f}%)")
    
    log_lines.append("=== Total Characters Count ===")
    log_lines.append(f"Plain: {total_plain}, Raw: {total_raw}.")

    with open("count_word.log", "w", encoding="utf-8") as f:
        f.write('\n'.join(log_lines) + '\n')
    
    if csv_log == False:
        with open("count_word.csv", "w", encoding="utf-8") as f:
            f.write("Author,Plain,Raw\n")
            for author in sorted(set(total_counts) | set(total_counts_all)):
                f.write(f"{author},{total_counts.get(author, 0)},{total_counts_all.get(author, 0)}\n")


def files_from_fls(fls_path, root_dir='.', main_tex=None):
    
    if not os.path.exists(fls_path):
        assert main_tex != None, "Both TeX file and fls file NOT FOUND."
        if pdflatex:
            print(f"[files_from_fls] {fls_path} not found, running pdflatex...")
            try:
                subprocess.run(["pdflatex", "-interaction=nonstopmode", "-recorder", main_tex], check=True)
                subprocess.run(["pdflatex", "-interaction=nonstopmode", "-recorder", main_tex], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] pdflatex failed: {e}")
                return []
        else:
            print(f"[files_from_fls] {fls_path} not found, running xelatex...")
            try:
                subprocess.run(["xelatex", "-interaction=nonstopmode", "-recorder", main_tex], check=True)
                subprocess.run(["xelatex", "-interaction=nonstopmode", "-recorder", main_tex], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] xelatex failed: {e}")
                return []
    seen = set()
    tex_files = []

    root_abs = os.path.abspath(root_dir)

    with open(fls_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('INPUT '):
                path = line[6:].strip()
                if not path.lower().endswith('.tex'):
                    continue
                abspath = os.path.abspath(path)

                if abspath.startswith(root_abs) and abspath not in seen and os.path.isfile(abspath):
                    seen.add(abspath)
                    tex_files.append(abspath)

    print(f"[files_from_fls] Loaded {len(tex_files)} project .tex files from .fls")
    return tex_files



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Git blame-based word/char counter for LaTeX projects.")
    parser.add_argument("main_tex", help="Main TeX file (e.g. whole_book.tex)")
    parser.add_argument("--fls", default=None, help="Path to .fls file (default: <main>.fls)")
    parser.add_argument("--char", action="store_true", help="Count characters instead of words")
    parser.add_argument("--nocsv", action="store_true", help="Do Not output csv log")
    parser.add_argument("--pdflatex", action="store_true", help="Use pdflatex rather than xelatex")
    args = parser.parse_args()

    count_char = args.char
    csv_log = args.nocsv
    pdflatex = args.pdflatex
    fls_file = args.fls if args.fls else os.path.splitext(args.main_tex)[0] + ".fls"

    files = files_from_fls(fls_file, main_tex=args.main_tex)
    for file in files:
        print(os.path.relpath(file))
    aggregate_contributions(files)
