import pandas as pd
from urllib.parse import quote_plus

def create_github_issue_url(title):
    """为论文标题创建一个预填写的GitHub Issue链接"""
    base_url = "https://github.com/Lab4AI-Hub/PaperHub/issues/new"
    # 使用我们为“选题申请”设计的模板
    template = "1_paper_suggestion.yml" 
    
    # 对标题进行URL编码，以防特殊字符
    encoded_title = quote_plus(f"[选题申请] {title}")
    
    # 拼接最终的URL
    return f"{base_url}?template={template}&title={encoded_title}"

def generate_html_table(csv_path):
    """读取CSV并生成HTML表格内容"""
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return "<p>错误：找不到 data.csv 文件。</p>"

    # 预处理数据
    if '论文名称' not in df.columns:
        return "<p>错误：CSV文件中缺少 '论文名称' 列。</p>"
    
    df = df.fillna('') # 填充空值为''
    
    html_rows = []
    for _, row in df.iterrows():
        # --- 核心修改部分：根据您的新表头读取数据 ---
        paper_title = str(row.get('论文名称', ''))
        authors = str(row.get('作者', ''))
        conference = str(row.get('会议来源', ''))
        year = str(row.get('年份', ''))
        paper_link = str(row.get('论文链接', ''))
        status = str(row.get('认领状态', '待认领'))
        
        # 将标题和作者合并，并用<br>换行
        title_authors_md = f"{paper_title}<br><em>{authors}</em>"
        # 将会议和年份合并
        conference_year_md = f"{conference} {year}"
        
        # 为“认领”按钮创建链接
        claim_url = create_github_issue_url(paper_title)

        # 根据状态显示不同的操作
        action_button = f'<a href="{claim_url}" class="claim-btn" target="_blank">🚀 认领任务</a>'
        if status != '待认领':
            action_button = f'<span class="status-{status.lower()}">{status}</span>'

        html_rows.append(f"""
        <tr>
            <td>{title_authors_md}</td>
            <td>{conference_year_md}</td>
            <td><a href="{paper_link}" target="_blank">查看论文</a></td>
            <td>{status}</td>
            <td>{action_button}</td>
        </tr>
        """)
    
    return "".join(html_rows)

def main():
    """主函数：生成完整的index.html"""
    
    # --- HTML模板头部 ---
    html_template_head = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lab4AI 待复现论文清单</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 20px; background-color: #f6f8fa; }
            .container { max-width: 1200px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1, p { text-align: center; }
            .intro-link { display: block; text-align: center; margin-bottom: 20px; font-size: 1.2em; }
            table { width: 100% !important; }
            th, td { text-align: left; padding: 12px; }
            .claim-btn { background-color: #238636; color: white; padding: 8px 12px; text-decoration: none; border-radius: 6px; font-weight: bold; }
            .claim-btn:hover { background-color: #2ea043; }
            .status-复现中, .status-已完成 { font-weight: bold; color: #8B4513; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Lab4AI 待复现论文清单</h1>
            <p class="intro-link">
                在认领任务前，请务必仔细阅读我们的 
                <a href="https://github.com/Lab4AI-Hub/PaperHub/blob/main/CONTRIBUTING.md" target="_blank"><strong>贡献流程和奖励规则</strong></a>。
            </p>
            <table id="paperTable" class="display">
                <thead>
                    <tr>
                        <th>论文名称 & 作者</th>
                        <th>会议来源 & 年份</th>
                        <th>论文链接</th>
                        <th>状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
    """

    # --- 生成表格内容 ---
    table_content = generate_html_table('data.csv')

    # --- HTML模板尾部 ---
    html_template_foot = """
                </tbody>
            </table>
        </div>
        <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.7.0.js"></script>
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function() {
                $('#paperTable').DataTable({
                    "pageLength": 25, // 每页显示25条
                    "language": {
                        "search": "搜索:",
                        "lengthMenu": "每页显示 _MENU_ 条记录",
                        "info": "显示第 _START_ 至 _END_ 条记录，共 _TOTAL_ 条",
                        "infoEmpty": "没有记录",
                        "infoFiltered": "(从 _MAX_ 条总记录中过滤)",
                        "paginate": {
                            "first": "首页",
                            "last": "末页",
                            "next": "下一页",
                            "previous": "上一页"
                        }
                    }
                });
            });
        </script>
    </body>
    </html>
    """

    # --- 拼接并保存为index.html ---
    full_html = html_template_head + table_content + html_template_foot
    
    # 创建一个名为 'dist' 的文件夹，如果它不存在的话
    output_dir = 'dist'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 将 index.html 保存到 'dist' 文件夹中
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == '__main__':
    main()
