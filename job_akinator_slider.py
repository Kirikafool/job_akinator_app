import streamlit as st
import pandas as pd
import re

# CSV読み込み
df = pd.read_csv("shindan_graph.csv")
questions = df.iloc[:, 0].dropna().tolist()
job_columns = df.columns[1:]

st.set_page_config(page_title="職業診断アプリ", page_icon="🧠")
st.title("🧠 職業アキネーター - 正規化スライダー診断版")
st.write("以下の10問にスライダーで回答すると、あなたに向いている本部がわかります！")

user_scores = []

# （〜）内のテキストを削除する関数
def remove_tilde_text(text):
    return re.sub(r"\(.*?\)", "", text).strip()

with st.form("questionnaire_form"):
    for i, q in enumerate(questions):
        full_q = str(q).strip()
        lines = full_q.split("\n")

        title = lines[0] if len(lines) > 0 else ""
        label_1 = remove_tilde_text(lines[1]) if len(lines) > 1 else "1"
        label_10 = remove_tilde_text(lines[2]) if len(lines) > 2 else "10"

        # 質問表示
        st.markdown(f"**Q{i+1}.** {title}")
        score = st.slider(label="", min_value=1, max_value=10, value=5, key=f"q{i}")
        user_scores.append(score)

        # ラベル表示
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
        normalized_score = (raw_score - 5.5) / 4.5  # 1〜10を-1〜+1に正規化
        for job in job_columns:
            weight = df.loc[i, job]
            total_scores[job] += normalized_score * float(weight)

    sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_scores[:3]

    st.subheader("🎯 あなたに合っている本部 TOP3")
    for idx, (job, score) in enumerate(top3, 1):
        st.markdown(f"**{idx}. {job}**：{score:.2f} 点")

    st.write("### スコア内訳")
    st.bar_chart(pd.Series(total_scores))
