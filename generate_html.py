# -*- coding: utf-8 -*-
import pandas as pd
import sys

def main():
    """主函数，读取CSV并进行诊断"""
    
    csv_path = "data.csv"
    print(f"--- 开始诊断：正在尝试读取 {csv_path} ---")
    
    try:
        # 使用 utf-8-sig 编码自动处理BOM头
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print("✅ CSV文件读取成功！")
        
        # --- 核心诊断步骤 ---
        print("\n--- 诊断报告：Pandas识别到的表头列表 ---")
        print("请将下面这行 `Index([...` 的完整内容截图或复制发给我们。")
        print(df.columns)
        print("--- 诊断报告结束 ---\n")
        
        # 检查关键列是否存在
        required_columns = ['论文名称', '论文作者', '来源标签（会议期刊）', '论文年份', '论文链接', '认领状态']
        
        # 标记是否有缺失的列
        missing_columns = False
        for col in required_columns:
            if col not in df.columns:
                print(f"❌ 错误：在识别出的表头中，找不到必需的列: '{col}'")
                missing_columns = True
        
        if missing_columns:
            print("\n脚本因缺少必要的列而终止。请根据上面的诊断报告修正脚本或CSV文件。")
            sys.exit(1) # 以错误码退出，让Action失败
        else:
            print("✅ 所有必需的列都已找到，表头匹配成功！")
            # 在这里，您可以继续执行生成HTML的逻辑，但为了诊断，我们暂时只打印成功信息。
            # 真正的生成逻辑我们将在拿到诊断报告后放入。
            print("\n诊断完成，脚本正常退出。")

    except Exception as e:
        print(f"\n❌ 在读取或处理CSV文件时发生致命错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
