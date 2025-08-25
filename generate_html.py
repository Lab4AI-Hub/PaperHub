# -*- coding: utf-8 -*-
import pandas as pd
import os
from urllib.parse import quote_plus
import html

# --- 全局配置 ---
CONFIG = {
    "csv_path": "data.csv",
    "output_dir": "dist",
    "output_filename": "index.html",
    "repo_url": "https://github.com/Lab4AI-Hub/PaperHub",
    "issue_template": "1_paper_suggestion.yml"
}

def create_github_issue_url(title):
    """为论文标题创建一个直接跳转到Issue模板的链接"""
    base_url = f"{CONFIG['repo_url']}/issues/new"
    template = CONFIG['issue_template']
    encoded_title = quote_plus(f"[选题申请] {title}")
    return f"{base_url}?template={template}&title={encoded_title}"

def generate_html_from_csv(df):
    """根据DataFrame生成HTML表格的行"""
    html_rows = []
    for _, row in df.iterrows():
        paper_title = html.escape(str(row.get('论文名称', '')))
        authors = html.escape(str(row.get('作者', '')))
        conference = html.escape(str(row.get('会议来源', '')))
        year = str(row.get('年份', ''))
        paper_link = str(row.get('论文链接', ''))
        status = str(row.get('认领状态', '待认领'))
        
        title_authors_html = f"{paper_title}<br><em style='color:#57606a;'>{authors}</em>"
        
        # **修正点**: 认领按钮的逻辑修正
        if status == '待认领':
            claim_url = create_github_issue_url(paper_title)
            action_button_html = f'<a href="{claim_url}" class="claim-btn" target="_blank">📝 申请任务</a>'
        else:
            # 对于已认领或已完成的状态，只显示文本
            action_button_html = f'<span class="status-claimed">{status}</span>'

        # **修正点**: 表格行结构修正
        html_rows.append(f"""
        <tr>
            <td>{title_authors_html}</td>
            <td>{conference}</td>
            <td>{year}</td>
            <td><a href="{paper_link}" target="_blank">查看论文</a></td>
            <td>{status}</td>
            <td>{action_button_html}</td>
        </tr>
        """)
    
    return "".join(html_rows)

def main():
    """主函数，读取CSV，生成完整的HTML页面"""
    print("开始生成网页...")
    try:
        df = pd.read_csv(CONFIG['csv_path'], encoding='utf-8-sig')
        df = df.fillna('')
    except FileNotFoundError:
        print(f"错误：源文件 {CONFIG['csv_path']} 未找到！")
        return

    table_content = generate_html_from_csv(df)
    
    # **修正点**: 优化了CSS和表格头部
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
            table.dataTable thead th {{ background-color: #f6f8fa; border-bottom: 2px solid #d0d7de; }}
            .claim-btn {{ background-color: #238636; color: white; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-weight: bold; white-space: nowrap; display: inline-block; }}
            .claim-btn:hover {{ background-color: #2ea043; }}
            .status-claimed {{ font-weight: bold; color: #8B4513; white-space: nowrap; }}
            /* **修正点**: 增加这个样式确保在小屏幕上可以水平滚动 */
            .dataTables_wrapper {{ overflow-x: auto; }}
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
                        <th>会议来源</th>
                        <th>年份</th>
                        <th>论文链接</th>
                        <th>认领状态</th>
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
                        "search": "🔍 搜索:",
                        "lengthMenu": "每页显示 _MENU_ 条",
                        "info": "显示第 _START_ 到 _END_ 条，共 _TOTAL_ 条",
                        "infoEmpty": "暂无数据",
                        "infoFiltered": "(从 _MAX_ 条总记录中筛选)",
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
