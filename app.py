import os
import streamlit as st
import warnings

# 警告を抑制
warnings.filterwarnings("ignore")

# 環境変数を読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenvがインストールされていない場合はスキップ
    pass

# ページ設定
st.set_page_config(
    page_title="AI専門家チャット",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI専門家チャット")
st.markdown("専門分野を選択して、AIエキスパートと対話できます。")

user_input = st.text_input(label="質問を入力してください。", placeholder="ここに質問を入力...")

# LLM応答関数の定義
def get_llm_response(input_text, expert_type):
    try:
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    except ImportError as e:
        return f"必要なライブラリがインストールされていません: {str(e)}"
    
    # OpenAI APIキーの確認
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "エラー: OPENAI_API_KEYが設定されていません。.envファイルにAPIキーを設定してください。"
    
    if expert_type == "法律":
        system_message = "あなたは法律の専門家です。法律に関する質問に対して、正確かつ簡潔に答えてください。"
    elif expert_type == "AI":
        system_message = "あなたはAIの専門家です。AIに関する質問に対して、正確かつ簡潔に答えてください。"
    else:
        system_message = "あなたは健康の専門家です。健康に関する質問に対して、正確かつ簡潔に答えてください。"

    try:
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_message),
            HumanMessagePromptTemplate.from_template("{input_text}")
        ])

        messages = chat_prompt.format_messages(input_text=input_text)

        chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
        response = chat.invoke(messages)

        return response.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"
    

expert_type = st.radio(
    "専門家の種類を選択してください。",
    ["法律", "AI", "健康"]
)

if st.button("実行"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            response = get_llm_response(user_input, expert_type)
            st.success("回答が生成されました！")
            st.write(response)
    else:
        st.warning("テキストを入力してください。")


