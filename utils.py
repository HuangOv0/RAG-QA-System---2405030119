"""工具函数模块"""
import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any

def calculate_file_hash(file_path: str) -> str:
    """计算文件的哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def get_file_info(file_path: str) -> Dict[str, Any]:
    """获取文件信息"""
    if not os.path.exists(file_path):
        return {}
    
    stat = os.stat(file_path)
    return {
        "name": os.path.basename(file_path),
        "path": file_path,
        "size": stat.st_size,
        "formatted_size": format_file_size(stat.st_size),
        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "hash": calculate_file_hash(file_path)
    }

def save_json(data: Any, file_path: str) -> bool:
    """保存数据为JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存JSON文件失败: {e}")
        return False

def load_json(file_path: str) -> Any:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败: {e}")
        return None

def format_timestamp(timestamp: float = None) -> str:
    """格式化时间戳"""
    if timestamp is None:
        timestamp = datetime.now().timestamp()
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def validate_file_format(file_path: str, supported_formats: List[str]) -> bool:
    """验证文件格式"""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in supported_formats

def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    # 移除多余的空白字符
    text = ' '.join(text.split())
    return text.strip()

def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def export_chat_history(chat_history: List[Dict], format: str = "json") -> str:
    """导出聊天记录"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format == "json":
        data = {
            "export_time": datetime.now().isoformat(),
            "total_messages": len(chat_history),
            "chat_history": chat_history
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    elif format == "txt":
        lines = [f"聊天记录导出时间: {datetime.now().isoformat()}", f"总消息数: {len(chat_history)}", ""]
        for msg in chat_history:
            role = "用户" if msg["role"] == "user" else "助手"
            lines.append(f"[{role}] {msg['content']}")
        return "\n".join(lines)
    
    elif format == "csv":
        lines = ["角色,内容,时间"]
        for msg in chat_history:
            role = "用户" if msg["role"] == "user" else "助手"
            # 转义CSV中的特殊字符
            content = msg["content"].replace('"', '""')
            lines.append(f'"{role}","{content}","{datetime.now().isoformat()}"')
        return "\n".join(lines)
    
    return ""

def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    import platform
    import sys
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": sys.version,
        "working_directory": os.getcwd()
    }