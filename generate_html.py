# -*- coding: utf-8 -*-
import pandas as pd
import os
from urllib.parse import quote_plus
import html

# --- 全局配置 ---
# 将所有可配置项放在这里，方便未来修改
CONFIG = {
    "csv_path": "data.csv",
    "output_dir": "dist",
    "output_filename": "index.html",
    "repo_url": "https://github.com/Lab4AI-Hub/PaperHub",
    "issue_template": "1_paper_suggestion.yml" # 确保你的Issue模板文件名正确
}

def create_github_issue_url(title):
    """为论文标题创建一个直接跳转到Issue模板并预填写标题的链接"""
    base_url = f"{CONFIG['repo_url']}/issues/new"
    template = CONFIG['issue_template']
    # 对标题进行URL编码，以防标题中有特殊字符
    encoded_title = quote_plus(f"[选题申请] {title}")
    return f"{base_url}?template={template}&title={encoded_title}"

def generate_html_from_csv(df):
    """根据DataFrame生成HTML表格的行"""
    html_rows = []
    # 遍历DataFrame的每一行
    for _, row in df.iterrows():
        # --- 核心部分：严格按照您的表头安全地读取数据 ---
        paper_title = html.escape(str(row.get('论文名称', '')))
        authors = html.escape(str(row.get('论文作者', '')))
        conference = html.escape(str(row.get('来源标签（会议期刊）', '')))
        year = str(row.get('论文年份', ''))
        paper_link = str(row.get('论文链接', ''))
        github_link = str(row.get('github链接', ''))
        form = str(row.get('形式', '')) # 读取“形式”列
        status = str(row.get('认领状态', '待认领'))
        
        # 组合需要合并显示的字段
        title_authors_html = f"{paper_title}<br><em style='color:#57606a;'>{authors}</em>"
        
        # 格式化论文链接和GitHub链接
        paper_link_html = f'<a href="{paper_link}" target="_blank">原文</a>' if paper_link else 'N/A'
        github_link_html = f'<a href="{github_link}" target="_blank">代码</a>' if github_link else 'N/A'
        links_html = f"{paper_link_html} | {github_link_html}"

        # 根据状态决定显示“申请任务”按钮还是状态文本
        if status == '待认领':
            claim_url = create_github_issue_url(paper_title)
            action_button_html = f'<a href="{claim_url}" class="claim-btn" target="_blank">📝 申请任务</a>'
        else:
            action_button_html = f'<span class="status-claimed">{status}</span>'

        # 拼接成一行HTML表格
        html_rows.append(f"""
        <tr>
            <td>{title_authors_html}</td>
            <td>{conference}</td>
            <td>{year}</td>
            <td>{form}</td>
            <td>{links_html}</td>
            <td>{action_button_html}</td>
        </tr>
        """)
    
    return "".join(html_rows)

def main():
    """主函数，读取CSV，生成完整的HTML页面"""
    print("开始生成网页...")
    try:
        # 使用 utf-8-sig 编码自动处理BOM头，解决KeyError问题
        df = pd.read_csv(CONFIG['csv_path'], encoding='utf-8-sig')
        df = df.fillna('')  # 将所有NaN空值替换为空字符串
    except FileNotFoundError:
        print(f"错误：源文件 {CONFIG['csv_path']} 未找到！")
        return

    table_content = generate_html_from_csv(df)
    
    # 完整的HTML页面模板
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lab4AI 待复现论文清单</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 1em; background-color: #f6f8fa; color: #24292f; }}
            .container {{ max-width: 95%; margin: 0 auto; background-color: #ffffff; padding: 2em; border: 1px solid #d0d7de; border-radius: 8px; box-shadow: 0 4px 12px rgba(27,31,36,0.08); }}
            header {{ text-align: center; margin-bottom: 2em; }}
            header h1 {{ font-size: 2em; margin-bottom: 0.5em; }}
            header p {{ font-size: 1.2em; color: #57606a; }}
            header a {{ color: #0969da; text-decoration: none; font-weight: bold; }}
            table.dataTable {{ border-collapse: collapse !important; }}
            table.dataTable thead th {{ background-color: #f6f8fa; border-bottom: 2px solid #d0d7de; }}
            .claim-btn {{ background-color: #238636; color: white; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-weight: bold; white-space: nowrap; display: inline-block; }}
            .claim-btn:hover {{ background-color: #2ea043; }}
            .status-claimed {{ font-weight: bold; color: #8B4513; white-space: nowrap; }}
            div.dataTables_wrapper {{ width: 100%; margin: 0 auto; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Lab4AI 待复现论文清单</h1>
                <p>在申请任务前，请务必仔细阅读我们的 <a href="{CONFIG['repo_url']}/blob/main/CONTRIBUTING.md" target="_blank">贡献流程和奖励规则</a>。</p>
            </header>
            <table id="paperTable" class="display" style="width:100%">
                <thead>
                    <tr>
                        <th>论文名称 & 作者</th>
                        <th>会议/期刊</th>
                        <th>年份</th>
                        <th>形式</th>
                        <th>相关链接</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {table_content}
                </tbody>
            </table>
        </div>
        <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
        <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function() {{
                $('#paperTable').DataTable({{
                    "pageLength": 25,
                    "order": [],
                    "language": {{
                        "search": "🔍 搜索:", "lengthMenu": "每页显示 _MENU_ 条", "info": "显示第 _START_ 到 _END_ 条，共 _TOTAL_ 条",
                        "infoEmpty": "暂无数据", "infoFiltered": "(从 _MAX_ 条总记录中筛选)",
                        "paginate": {{ "first": "首页", "last": "末页", "next": "下一页", "previous": "上一页" }},
                        "zeroRecords": "没有找到匹配的记录"
                    }}
                }});
            }});
        </script>
    </body>
    </html>
    """

    output_dir = CONFIG['output_dir']
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, CONFIG['output_filename'])
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"网页已成功生成到: {output_path}")

if __name__ == '__main__':
    main()
if __name__ == '__main__':
    main()
