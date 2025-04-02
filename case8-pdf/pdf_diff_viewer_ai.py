import fitz  # PyMuPDF
import diff_match_patch as dmp_module
import sys
from pathlib import Path
import pandas as pd
import html
from datetime import datetime

def extract_pdf_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    return [page.get_text() for page in doc]

def escape_and_format_html(text):
    if not text:
        return ""
    return html.escape(text).replace("\n", "<br>")

def compare_texts(old_text, new_text):
    dmp = dmp_module.diff_match_patch()
    diffs = dmp.diff_main(old_text, new_text)
    dmp.diff_cleanupSemantic(diffs)

    additions, deletions = [], []
    for op, data in diffs:
        clean_data = data.strip()
        if not clean_data:
            continue
        if op == dmp.DIFF_INSERT:
            additions.append(clean_data)
        elif op == dmp.DIFF_DELETE:
            deletions.append(clean_data)

    raw_html = dmp.diff_prettyHtml(diffs)
    # ✅ 正确方式：不再转义 <ins> / <del>，但清洗换行符
    clean_html = raw_html.replace('\n', '<br>')

    return additions, deletions, clean_html

def compare_pdf_versions_with_html(pdf_old_path, pdf_new_path):
    old_pages = extract_pdf_text_by_page(pdf_old_path)
    new_pages = extract_pdf_text_by_page(pdf_new_path)
    max_pages = max(len(old_pages), len(new_pages))

    results = []
    for i in range(max_pages):
        old_text = old_pages[i] if i < len(old_pages) else ""
        new_text = new_pages[i] if i < len(new_pages) else ""
        print(f"📘 正在比较第 {i+1} 页...")
        print(new_text)
        print(old_text)
        added, deleted, html_diff = compare_texts(old_text, new_text)

        if not added and not deleted:
            continue  # 跳过无变化页

        results.append({
            "Page": i + 1,
            "Added": "; ".join(added),
            "Deleted": "; ".join(deleted),
            "HTML Diff": html_diff
        })

    return pd.DataFrame(results)

def generate_full_html_report(results_df, output_file="diff_report.html", title="PDF 差异对比报告"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; line-height: 1.8; background: #f9f9f9; }}
    h1 {{ color: #333; }}
    h2 {{ color: #444; }}
    .toc {{ background: #fff; border: 1px solid #ccc; padding: 15px; border-radius: 10px; }}
    .toc summary {{ font-size: 18px; font-weight: bold; cursor: pointer; }}
    .toc ul {{ padding-left: 20px; }}
    .toc a {{ text-decoration: none; color: #2a7ae2; }}
    .diff-section {{ border: 1px solid #ddd; background: #fff; padding: 20px; border-radius: 12px; margin-top: 40px; }}
    .diff-section h2 {{ margin-top: 0; }}
    ins {{
      background-color: #c8facc;
      border: 1px solid #4caf50;
      padding: 2px 3px;
      text-decoration: none;
    }}
    del {{
      background-color: #fcb6b6;
      border: 1px solid #f44336;
      padding: 2px 3px;
      text-decoration: none;
    }}
    .top-link {{
      display: block;
      margin-top: 20px;
      text-align: right;
    }}
    .top-link a {{
      font-size: 14px;
      color: #999;
    }}
    footer {{
      margin-top: 80px;
      text-align: center;
      font-size: 13px;
      color: #aaa;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
  <hr/>

  <details class="toc" open>
    <summary>📑 差异目录导航</summary>
    <ul>
""")
        for _, row in results_df.iterrows():
            f.write(f'<li><a href="#page{row["Page"]}">第 {row["Page"]} 页</a></li>\n')

        f.write("</ul></details><hr/>")

        for _, row in results_df.iterrows():
            f.write(f'<section class="diff-section" id="page{row["Page"]}">\n')
            f.write(f'<h2>📄 第 {row["Page"]} 页 差异内容</h2>\n')
            f.write(f'<p>{row["HTML Diff"] or "<em>（本页无实际差异）</em>"}</p>')
            f.write(f'<div class="top-link"><a href="#top">↑ 返回顶部</a></div>\n')
            f.write('</section>\n')

        f.write(f"""<footer>
  PDF 差异比对工具生成 © {datetime.now().year} | 使用 ChatGPT + PyMuPDF + DiffMatchPatch 自动生成
</footer>
</body></html>""")

def main():
    if len(sys.argv) != 3:
        print("用法: python pdf_diff_viewer.py old_version.pdf new_version.pdf")
        sys.exit(1)

    pdf_old_path = Path(sys.argv[1])
    pdf_new_path = Path(sys.argv[2])

    if not pdf_old_path.exists() or not pdf_new_path.exists():
        print("❌ 错误：指定的PDF文件不存在。")
        sys.exit(1)

    print(f"🔍 正在比较以下PDF版本：\n📄 旧版本：{pdf_old_path}\n📄 新版本：{pdf_new_path}\n")

    results = compare_pdf_versions_with_html(pdf_old_path, pdf_new_path)

    if results.empty:
        print("🎉 两个文档完全一致，无任何内容变更。")
        return

    for _, row in results.iterrows():
        print(f"📘 第 {row['Page']} 页差异：")
        print(f"  ➕ 新增: {row['Added'][:100]}{'...' if len(row['Added']) > 100 else ''}")
        print(f"  ➖ 删除: {row['Deleted'][:100]}{'...' if len(row['Deleted']) > 100 else ''}")

    generate_full_html_report(results)
    print("\n✅ 差异HTML报告已生成：diff_report.html（可用浏览器打开查看完整对比）")

if __name__ == "__main__":
    main()