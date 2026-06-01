"""Ollama API测试脚本"""
import ollama

def test_ollama_connection():
    """测试Ollama连接"""
    try:
        # 获取模型列表
        models = ollama.list()
        print("已安装的模型:")
        for model in models.get("models", []):
            print(f"  - {model['name']}")
        
        # 测试生成响应
        response = ollama.generate(
            model="deepseek-r1:7b",
            prompt="你好，介绍一下你自己。"
        )
        print("\n模型响应:")
        print(response.get("response", ""))
        
        return True
    except Exception as e:
        print(f"测试失败: {str(e)}")
        print("请确保Ollama服务已启动，并且deepseek-r1:7b模型已下载。")
        return False

if __name__ == "__main__":
    print("=== Ollama API测试 ===")
    success = test_ollama_connection()
    if success:
        print("\n✓ Ollama连接测试成功！")
    else:
        print("\n✗ Ollama连接测试失败")
