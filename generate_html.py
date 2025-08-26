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

def create_github_issue_url(title=""):
    """创建跳转到Issue模板的链接，如果提供标题则预填写"""
    base_url = f"{CONFIG['repo_url']}/issues/new"
    template = CONFIG['issue_template']
    
    if title:
        encoded_title = quote_plus(f"[选题申请] {title}")
        return f"{base_url}?template={template}&title={encoded_title}"
    else:
        # 如果没有提供标题，则只跳转到模板选择页
        return f"{base_url}?template={template}"

def generate_html_from_csv(df):
    """根据DataFrame生成HTML表格的行"""
    print(f"开始处理 {len(df)} 行数据...")
    html_rows = []
    for index, row in df.iterrows():
        try:
            # --- 严格按照您的表头安全地读取数据 ---
            paper_title = html.escape(str(row.get('论文名称', '')))
            authors = html.escape(str(row.get('论文作者', '')))
            conference = html.escape(str(row.get('来源标签（会议期刊）', '')))
            year = str(row.get('论文年份', ''))
            paper_link = str(row.get('论文链接', ''))
            github_link = str(row.get('github链接', ''))
            form = html.escape(str(row.get('形式', '')))
            status = str(row.get('认领状态', ''))

            # 组合显示字段
            title_authors_html = f"{paper_title}<br><em style='color:#57606a;'>{authors}</em>"
            
            links_html_parts = []
            if paper_link:
                links_html_parts.append(f'<a href="{paper_link}" target="_blank">原文</a>')
            if github_link:
                links_html_parts.append(f'<a href="{github_link}" target="_blank">代码</a>')
            links_html = ' | '.join(links_html_parts) if links_html_parts else 'N/A'

            # 根据状态决定“操作”列的内容
            if status == '待认领':
                claim_url = create_github_issue_url(paper_title)
                action_button_html = f'<a href="{claim_url}" class="claim-btn" target="_blank">📝 申请任务</a>'
            else:
                action_button_html = '' 

            html_rows.append(f"""
            <tr>
                <td>{title_authors_html}</td>
                <td>{conference}</td>
                <td>{year}</td>
                <td>{form}</td>
                <td>{links_html}</td>
                <td>{status}</td>
                <td>{action_button_html}</td>
            </tr>
            """)
        except Exception as e:
            print(f"处理第 {index + 2} 行数据时发生错误: {e}")
            print(f"该行数据: {row.to_dict()}")
            # 即使单行出错，也继续处理下一行
            continue
    
    print("所有数据行处理完毕。")
    return "".join(html_rows)

def main():
    """主函数，读取CSV，生成完整的HTML页面"""
    print("脚本开始运行...")
    try:
        df = pd.read_csv(CONFIG['csv_path'], encoding='utf-8-sig')
        df = df.fillna('')
        print(f"成功读取 {CONFIG['csv_path']} 文件，共 {len(df)} 条记录。")
    except FileNotFoundError:
        print(f"致命错误：源文件 {CONFIG['csv_path']} 未找到！脚本终止。")
        return
    except Exception as e:
        print(f"读取CSV文件时发生致命错误: {e}。脚本终止。")
        return

    table_content = generate_html_from_csv(df)
    
    # 获取全局的“推荐新论文”按钮链接
    propose_new_url = create_github_issue_url()

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
            .header-actions {{ margin-top: 1.5em; }}
            .propose-btn {{ background-color: #8957e5; color: white; padding: 10px 20px; font-size: 1.1em; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block; }}
            .propose-btn:hover {{ background-color: #6e44c2; }}
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
                <div class="header-actions">
                    <a href="{propose_new_url}" class="propose-btn" target="_blank">💡 推荐一篇新论文</a>
                </div>
            </header>
            <table id="paperTable" class="display" style="width:100%">
                <thead>
                    <tr>
                        <th>论文名称 & 作者</th>
                        <th>会议/期刊</th>
                        <th>年份</th>
                        <th>形式</th>
                        <th>相关链接</th>
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
