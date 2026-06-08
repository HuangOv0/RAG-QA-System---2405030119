"""Ollama API 测试脚本"""
import ollama

def test_ollama_connection():
    """测试Ollama连接"""
    try:
        # 列出可用模型
        models = ollama.list()
        print("可用的模型:")
        for model in models.get("models", []):
            print(f" - {model['name']}")
        
        # 测试生成功能
        response = ollama.generate(
            model="deepseek-r1:7b",
            prompt="你好，请介绍一下自己。"
        )
        print("\n生成结果:")
        print(response.get("response", ""))
        
        return True
    except Exception as e:
        print(f"连接失败: {str(e)}")
        print("请确保Ollama服务正在运行，并且已下载deepseek-r1:7b模型")
        return False

if __name__ == "__main__":
    print("=== Ollama API 测试 ===")
    success = test_ollama_connection()
    if success:
        print("\n✅ Ollama API 连接成功")
    else:
        print("\n❌ Ollama API 连接失败")