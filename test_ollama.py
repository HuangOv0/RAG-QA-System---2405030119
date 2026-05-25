import ollama

def test_ollama():
    try:
        response = ollama.chat(model='deepseek-r1:7b', messages=[
            {
                'role': 'user',
                'content': '你好，请问你是谁？',
            },
        ])
        print("Ollama API测试成功！")
        print("响应内容:", response['message']['content'])
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        return False

if __name__ == "__main__":
    test_ollama()