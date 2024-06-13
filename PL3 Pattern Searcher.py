import os
import re
from tkinter import Tk, filedialog
from collections import defaultdict

def select_directory():
    """GUIを使用してディレクトリを選択する"""
    root = Tk()
    root.withdraw()  # GUIを隠す
    directory = filedialog.askdirectory(title="Select Directory")
    return directory

def search_patterns_in_file(file_path, patterns):
    """指定されたファイル内でパターンに一致する部分文字列を検索する"""
    matches = []
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('ISO-8859-1')
            for pattern in patterns:
                matches.extend(re.findall(pattern, content))
    except UnicodeDecodeError as e:
        print(f"Unicode decode error in file {file_path}: {e}")
    except IOError as e:
        print(f"IO error reading file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error reading file {file_path}: {e}")
    return matches

def write_log_file(results, log_file_path):
    """検索結果をログファイルに書き込む"""
    try:
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            for file_path, matches in results.items():
                log_file.write(f"File: {file_path}\n")
                log_file.write(f"References ({len(matches)} times):\n")
                unique_matches = set(matches)
                if len(unique_matches) > 1:
                    log_file.write("  Different references found:\n")
                for match in unique_matches:
                    count = matches.count(match)
                    log_file.write(f"  {match} (count: {count})\n")
                log_file.write("\n")
        print(f"Log file has been created: {log_file_path}")
    except IOError as e:
        print(f"IO error writing log file: {e}")
    except Exception as e:
        print(f"Unexpected error writing log file: {e}")

def main():
    """PL3 Pattern Searcher: 指定されたディレクトリ内の .pl3 ファイルから特定のパターンを検索してログに記録するプログラム"""
    
    # 検索パターンのリスト
    patterns = [r'V=40.*?\.txp', r'V=60.*?\.txp', r'V=80.*?\.txp', r'V=100.*?\.txp']
    
    # ディレクトリを選択
    directory = select_directory()
    if not directory:
        print("No directory selected. Exiting.")
        return

    # 結果を保存する辞書
    results = defaultdict(list)

    # 指定されたディレクトリ内のすべての .pl3 ファイルを検索
    for root_dir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pl3'):
                file_path = os.path.join(root_dir, file)
                matches = search_patterns_in_file(file_path, patterns)
                if matches:
                    results[file_path].extend(matches)

    # ログファイルに結果を記録
    log_file_path = "PL3_pattern_search_results.log"
    write_log_file(results, log_file_path)

if __name__ == "__main__":
    main()
