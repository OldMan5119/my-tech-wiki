#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
from pathlib import Path

def remove_advertisement_from_filename(filename):
    """
    从文件名中删除广告内容
    """
    # 定义要删除的广告模式（正则表达式）
    ad_patterns = [
        r'【更多资源[^】]*】',          # 匹配【更多资源...】
        r'【微[^】]*】',               # 匹配【微...】
        r'【资源[^】]*】',             # 匹配【资源...】
        r'【获取[^】]*】',             # 匹配【获取...】
        r'【联系[^】]*】',             # 匹配【联系...】
        r'【微信号[^】]*】',           # 匹配【微信号...】
        r'【QQ[^】]*】',               # 匹配【QQ...】
        r'【AG\d+】',                  # 匹配【AG数字】
        r'【微AG\d+】',                # 匹配【微AG数字】
        r'【更多资源.*微AG\d+】',      # 匹配完整的广告模式
        r'_\d{1,2}$',                  # 匹配末尾的数字（可能是序号）
    ]
    
    original_name = filename
    new_name = filename
    
    # 应用所有广告模式
    for pattern in ad_patterns:
        new_name = re.sub(pattern, '', new_name, flags=re.IGNORECASE)
    
    # 清理多余的下划线和连字符
    new_name = re.sub(r'_{2,}', '_', new_name)  # 多个下划线变一个
    new_name = re.sub(r'-{2,}', '-', new_name)  # 多个连字符变一个
    new_name = new_name.strip(' _-')            # 去除首尾的空格、下划线、连字符
    
    # 如果文件名以点开头（可能是隐藏文件），确保点不被删除
    if original_name.startswith('.') and not new_name.startswith('.'):
        new_name = '.' + new_name
    
    return new_name

def rename_files_recursively(directory, dry_run=False, verbose=False):
    """
    递归重命名目录中的所有文件
    """
    renamed_count = 0
    error_count = 0
    
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = Path(root) / filename
            new_filename = remove_advertisement_from_filename(filename)
            
            # 如果文件名有变化
            if new_filename != filename:
                new_file_path = Path(root) / new_filename
                
                try:
                    if dry_run:
                        print(f"[DRY RUN] 将会重命名: '{filename}' -> '{new_filename}'")
                    else:
                        # 检查目标文件是否已存在
                        if new_file_path.exists():
                            print(f"[警告] 文件已存在，跳过: {new_file_path}")
                            error_count += 1
                            continue
                        
                        # 重命名文件
                        file_path.rename(new_file_path)
                        if verbose:
                            print(f"[成功] 重命名: '{filename}' -> '{new_filename}'")
                        renamed_count += 1
                        
                except Exception as e:
                    print(f"[错误] 无法重命名 {file_path}: {e}")
                    error_count += 1
    
    return renamed_count, error_count

def main():
    parser = argparse.ArgumentParser(description='递归删除文件名中的广告内容')
    parser.add_argument('directory', help='要处理的目录路径')
    parser.add_argument('--dry-run', '-n', action='store_true', 
                       help='试运行，不实际重命名文件')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误: 目录 '{args.directory}' 不存在")
        return
    
    print(f"开始处理目录: {args.directory}")
    if args.dry_run:
        print("模式: 试运行（不实际重命名文件）")
    
    # 执行重命名
    renamed_count, error_count = rename_files_recursively(
        args.directory, args.dry_run, args.verbose
    )
    
    # 输出结果
    print(f"\n处理完成!")
    print(f"成功重命名: {renamed_count} 个文件")
    print(f"错误数量: {error_count}")
    
    if args.dry_run:
        print("\n注意: 这是试运行模式，没有实际重命名任何文件。")
        print("如果要实际执行，请移除 --dry-run 参数")

if __name__ == "__main__":
    main()