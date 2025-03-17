import google.generativeai as genai
from dotenv import load_dotenv
import os

# .envファイルからAPIキーを読み込む
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("APIキーが設定されていません。")

genai.configure(api_key=API_KEY)

# モデルの選択（Gemini Proを使用）
model = genai.GenerativeModel("gemini-1.5-flash")

def check_black_history(text):
    """入力テキストが黒歴史に該当するか判定する"""
    prompt = f"""
    次の文章が「黒歴史」にあたるかどうか判定してください。
    黒歴史とは、過去に自分が書いたり発言したりしたことで、後から恥ずかしく思うような内容です。
    ただし、一般的な創作活動やジョークは含みません。
    
    【判定対象の文章】
    {text}
    
    「黒歴史です」または「黒歴史ではありません」とだけ回答してください。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"エラーが発生しました: {e}"

# テスト
test_text = "中二病時代に書いたポエム：『俺の闇の力が目覚めた…』"
result = check_black_history(test_text)

print("判定結果:", result)