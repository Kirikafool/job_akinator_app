import streamlit as st
import pandas as pd
import re

# CSV読み込み
df = pd.read_csv("shindan_graph.csv")
url_df = pd.read_csv("url.csv")
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
        label_1 = remove_tilde_text(lines[1])_
