import streamlit as st
import pandas as pd
import re

# ✅ ページ設定（最初に書く！）
st.set_page_config(page_title="職業診断アプリ", page_icon="🧠")

# ✅ パスワード認証（最初に必ず通す）
PASSWORD = "secret123"  # ← お好きなパスワードに変更OK
password_input = st.text_input("🔒 パスワードを入力してください", type="password")
if password_input != PASSWORD:
    st.warning("パスワードが必要です")
    st.stop()

# ✅ CSV読み込み
df = pd.read_csv("shindan_graph.csv")
url_df = pd.read_csv("url.csv")
questions = df.iloc[:, 0].dropna().tolist()
job_columns = df.columns[1:]

# ✅ タイトル表示
st.title("🧠 あなたに合う本部はどれ？")
st.write("以下の10問にスライダーで回答すると、あなたに向いている本部の部署がわかります！")

user_scores = []

# ✅ ()の補足テキストを消す関数
def remove_tilde_text(text):
    return re.sub(r"\(.*?\)", "", text).strip()

# ✅ 質問フォーム
with st.form("questionnaire_form"):
    for i, q in enumerate(questions):
        full_q = str(q).strip()
        lines = full_q.split("\n")

        title = lines[0] if len(lines) > 0 else ""
        label_1 = remove_tilde_text(lines[1]) if len(lines) > 1 else "1"
        label_10 = remove_tilde_text(lines[2]) if len(lines) > 2 else "10"

        st.markdown(f"**Q{i+1}.** {title}")
        score = st.slider(label="", min_value=1, max_value=10, value=5, key=f"q{i}")
        user_scores.append(score)

        col1, col2 = st.columns(2)
        with col1:
            col1.markdown(f"<div style='font-weight:bold;'>⬅️ {label_1}</div>", unsafe_allow_html=True)
        with col2:
            col2.markdown(f"<div style='text-align:right; font-weight:bold;'>{label_10} ➡️</div>", unsafe_allow_html=True)

        st.markdown("---")

    submitted = st.form_submit_button("診断する")

# ✅ 診断ロジック & 出力
if submitted:
    total_scores = dict.fromkeys(job_columns, 0.0)
    for i, raw_score in enumerate(user_scores):
        normalized_score = (raw_score - 5.5) / 4.5  # 1〜10を-1〜+1に正規化
        for job in job_columns:
            weight = df.loc[i, job]
            total_scores[job] += normalized_score * float(weight)

    sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = [job for job, score in sorted_scores[:3]]

    st.subheader("🎯 あなたに合っている本部はこちら")

    # TOP3 横並びで表示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{top3[0]}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{top3[1]}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{top3[2]}</div>", unsafe_allow_html=True)

    # 対応するURLをリンク表示
    st.write("### 🔗 各本部の詳細はこちら：")
    for dept in top3:
        match = url_df[url_df.iloc[:, 0] == dept]
        if not match.empty:
            url = match.iloc[0, 1]
            st.markdown(f"- [{dept} の詳細を見る]({url})", unsafe_allow_html=True)
