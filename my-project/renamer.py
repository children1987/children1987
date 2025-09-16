import os
import re

def rename_files_and_directories():
    print("📂 当前目录内容：")
    items = os.listdir('.')
    for item in items:
        print(f"   {item}")
    print("\n🔄 开始重命名...")

    for item in items:
        # 更强健的正则：允许 UUID 在扩展名前，或无扩展名
        # 匹配：空格 + 32位十六进制 + 可选的扩展名
        match = re.search(r'^(.*?)( [a-fA-F0-9]{32})(\.[^.]+)?$', item)
        if match:
            prefix = match.group(1)      # 前缀部分（如“笔记”）
            uuid_part = match.group(2)   # 空格+UUID（如“ 8ebf...”）
            ext = match.group(3) or ''   # 扩展名（如“.md”，没有则为空）

            new_name = prefix + ext

            old_path = os.path.join('.', item)
            new_path = os.path.join('.', new_name)

            if os.path.exists(new_path):
                print(f'⚠️  跳过 "{item}" → "{new_name}"（目标已存在）')
                continue

            try:
                os.rename(old_path, new_path)
                print(f'✅ 成功重命名: "{item}" → "{new_name}"')
            except Exception as e:
                print(f'❌ 失败: "{item}" → "{new_name}" | 错误: {e}')
        else:
            print(f'🔍 未匹配（跳过）: "{item}"')

if __name__ == "__main__":
    rename_files_and_directories()
    print("\n🎉 处理完成！")