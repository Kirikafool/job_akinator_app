import streamlit as st
import pandas as pd

# CSV読み込み
df = pd.read_csv("shindan_graph.csv")
questions = df.iloc[:, 0].tolist()
job_columns = df.columns[1:]

st.set_page_config(page_title="職業診断アプリ", page_icon="🧠")
st.title("🧠 職業アキネーター - スライダー診断版")
st.write("以下の10問にスライダーで回答すると、あなたに向いている本部がわかります！")

user_scores = []

# 質問フォーム（修正版）
with st.form("questionnaire_form"):
    for i, q in enumerate(questions):
        clean_q = q.split("\n")[0]  # 質問の冒頭1行だけ表示
        score = st.slider(label=clean_q, min_value=1, max_value=10, value=5, key=f"q{i}")
        user_scores.append(score)

    submitted = st.form_submit_button("診断する")

# 結果表示
if submitted:
    total_scores = dict.fromkeys(job_columns, 0.0)
    for i, user_score in enumerate(user_scores):
        for job in job_columns:
            weight = df.loc[i, job]
            total_scores[job] += user_score * float(weight)

    sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_scores[:3]

    st.subheader("🎯 あなたに合っている本部 TOP3")
    for idx, (job, score) in enumerate(top3, 1):
        st.markdown(f"**{idx}. {job}**：{score:.1f} 点")

    st.write("### スコア内訳")
    st.bar_chart(pd.Series(total_scores))
