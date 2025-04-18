
import streamlit as st
import pandas as pd
import re


# データ読み込み
df = pd.read_csv("shindan_graph.csv")
url_df = pd.read_csv("url.csv")  # 本部名とURLの対応表

questions = df.iloc[:, 0].dropna().tolist()
job_columns = df.columns[1:]

st.set_page_config(page_title="職業診断アプリ", page_icon="🧠")
st.title("🧠 職業アキネーター - 正規化スライダー診断版")
st.write("以下の10問にスライダーで回答すると、あなたに向いている本部がわかります！")

# 🔐 パスワード制御
PASSWORD = "secret123"  # ←ここを好きなパスワードに変更
password_input = st.text_input("🔒 パスワードを入力してください", type="password")
if password_input != PASSWORD:
    st.warning("パスワードが必要です")
    st.stop()

user_scores = []

# （〜）内の補足を削除
def remove_tilde_text(text):
    return re.sub(r"\(.*?\)", "", text).strip()

# 質問フォーム
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

# 診断ロジック
if submitted:
    total_scores = dict.fromkeys(job_columns, 0.0)
    for i, raw_score in enumerate(user_scores):
        normalized_score = (raw_score - 5.5) / 4.5  # 正規化: -1 〜 +1
        for job in job_columns:
            weight = df.loc[i, job]
            total_scores[job] += normalized_score * float(weight)

    sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = [job for job, score in sorted_scores[:3]]

    # 横並びで本部名表示
    st.subheader("🎯 あなたに合っている本部はこちら")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{top3[0]}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{top3[1]}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold;'>{top3[2]}</div>", unsafe_allow_html=True)

    # 各本部のリンクを表示
    st.write("### 🔗 各本部の詳細はこちら：")
    for dept in top3:
        match = url_df[url_df.iloc[:, 0] == dept]
        if not match.empty:
            url = match.iloc[0, 1]
            st.markdown(f"- [{dept} の詳細を見る]({url})", unsafe_allow_html=True)
