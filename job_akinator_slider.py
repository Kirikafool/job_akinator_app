import streamlit as st
import pandas as pd

# CSV読み込み
df = pd.read_csv("shindan_graph.csv")
questions = df.iloc[:, 0].dropna().tolist()
job_columns = df.columns[1:]

st.set_page_config(page_title="職業診断アプリ", page_icon="🧠")
st.title("🧠 職業アキネーター - スライダー診断版")
st.write("以下の10問にスライダーで回答すると、あなたに向いている本部がわかります！")

user_scores = []

with st.form("questionnaire_form"):
    for i, q in enumerate(questions):
        full_q = str(q).strip()
        lines = full_q.split("\n")

        title = lines[0] if len(lines) > 0 else ""
        label_1 = lines[1] if len(lines) > 1 else "1"
        label_10 = lines[2] if len(lines) > 2 else "10"
