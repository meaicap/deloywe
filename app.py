import streamlit as st
import requests

# ===================== CONFIG =====================
st.set_page_config(page_title="AI Study Agent", layout="wide")
API_BASE = "http://127.0.0.1:8000"

# ===================== SESSION INIT =====================
defaults = {
    "user": None,
    "selected_document_id": None,
    "last_uploaded_name": None,
    "flashcards": None,
    "fc_index": 0,
    "fc_flipped": False,
    "quiz": None,
    "answers": {},
    "submitted": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ===================== LOGIN / REGISTER =====================
if st.session_state.user is None:
    st.title("🔐 AI Study Agent")

    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Đăng nhập"):
            res = requests.post(f"{API_BASE}/auth/login", json={"username": u, "password": p})
            if res.status_code == 200:
                st.session_state.user = res.json()
                st.rerun()
            else:
                st.error(res.text)

    with tab2:
        u = st.text_input("Username", key="ru")
        p = st.text_input("Password", type="password", key="rp")
        if st.button("Đăng ký"):
            res = requests.post(f"{API_BASE}/auth/register", json={"username": u, "password": p})
            if res.status_code == 200:
                st.success("✅ Đăng ký thành công")
            else:
                st.error(res.text)

    st.stop()

# ===================== USER INFO =====================
user_id = st.session_state.user["id"]
st.title("📘 AI Study Agent")

# ===================== LOGOUT =====================
st.sidebar.divider()
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.clear()
    st.rerun()

# ===================== LOAD DOCUMENTS =====================
st.sidebar.header("📚 Tài liệu")
documents = requests.get(f"{API_BASE}/documents/user/{user_id}").json()

for doc in documents:
    c1, c2 = st.sidebar.columns([4, 1])
    if c1.button(f"📄 {doc['filename']}", key=f"d{doc['id']}"):
        st.session_state.selected_document_id = doc["id"]
        st.rerun()
    if c2.button("❌", key=f"dd{doc['id']}"):
        r = requests.delete(f"{API_BASE}/documents/{doc['id']}", params={"user_id": user_id})
        if r.status_code == 200:
            st.session_state.selected_document_id = None
            st.rerun()

# ===================== CURRENT DOC =====================
st.divider()
doc = next((d for d in documents if d["id"] == st.session_state.selected_document_id), None)
if doc:
    st.success(f"📄 Đang học: **{doc['filename']}**")
else:
    st.info("📌 Upload hoặc chọn tài liệu")

# ===================== UPLOAD =====================
st.header("📄 Upload PDF")
uploaded = st.file_uploader("Chọn PDF", type=["pdf"])
if uploaded and uploaded.name != st.session_state.last_uploaded_name:
    with st.spinner("Đang upload & index..."):
        res = requests.post(
            f"{API_BASE}/upload/pdf",
            files={"file": uploaded},
            data={"user_id": user_id},
            timeout=120
        )
        if res.status_code == 200:
            st.session_state.last_uploaded_name = uploaded.name
            st.session_state.selected_document_id = res.json()["document_id"]
            st.rerun()
        else:
            st.error(res.text)

# ===================== CREATE =====================
if doc:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✨ Tạo Flashcard"):
            requests.post(
                f"{API_BASE}/flashcard/create",
                json={"user_id": user_id, "document_id": doc["id"], "num_cards": 10}
            )
            st.rerun()

    with c2:
        if st.button("🧪 Tạo Quiz"):
            requests.post(
                f"{API_BASE}/quiz/create",
                json={"user_id": user_id, "document_id": doc["id"], "num_questions": 10}
            )
            st.rerun()

# ===================== FLASHCARD BOX =====================
st.divider()
st.subheader("🧠 Flashcards")

sets = requests.get(
    f"{API_BASE}/flashcard/list/{user_id}",
    params={"document_id": st.session_state.selected_document_id}
).json() if doc else []

for s in sets:
    with st.container(border=True):
        st.markdown(f"**🃏 {s['title']}**")
        c1, c2 = st.columns(2)
        if c1.button("▶️ Học", key=f"fs{s['id']}"):
            st.session_state.flashcards = requests.get(
                f"{API_BASE}/flashcard/{s['id']}",
                params={"user_id": user_id}
            ).json()["cards"]
            st.session_state.fc_index = 0
            st.session_state.fc_flipped = False
        if c2.button("❌ Xóa", key=f"fds{s['id']}"):
            requests.delete(f"{API_BASE}/flashcard/{s['id']}", params={"user_id": user_id})
            st.rerun()

# ===================== FLASHCARD VIEW =====================
if st.session_state.flashcards:
    cards = st.session_state.flashcards
    i = st.session_state.fc_index
    card = cards[i]

    st.info(card["answer"] if st.session_state.fc_flipped else card["question"])
    c1, c2, c3 = st.columns(3)
    if c1.button("⬅️") and i > 0:
        st.session_state.fc_index -= 1
    if c2.button("👀"):
        st.session_state.fc_flipped = not st.session_state.fc_flipped
    if c3.button("➡️") and i < len(cards) - 1:
        st.session_state.fc_index += 1

# ===================== QUIZ BOX =====================
st.divider()
st.subheader("📝 Quiz")

quizzes = requests.get(
    f"{API_BASE}/quiz/list/{user_id}",
    params={"document_id": st.session_state.selected_document_id}
).json() if doc else []

for q in quizzes:
    quiz_id, title, created_at = q
    with st.container(border=True):
        st.markdown(f"**📝 {title}**")
        c1, c2 = st.columns(2)
        if c1.button("▶️ Làm", key=f"qq{quiz_id}"):
            st.session_state.quiz = requests.get(
                f"{API_BASE}/quiz/{quiz_id}",
                params={"user_id": user_id}
            ).json()
            st.session_state.answers = {}
            st.session_state.submitted = False
        if c2.button("❌ Xóa", key=f"dq{quiz_id}"):
            requests.delete(f"{API_BASE}/quiz/{quiz_id}", params={"user_id": user_id})
            st.rerun()

# ===================== DO QUIZ =====================
if st.session_state.quiz and not st.session_state.submitted:
    for i, q in enumerate(st.session_state.quiz):
        st.write(q["question"])
        st.session_state.answers[i] = st.radio(
            "",
            list(q["options"].keys()),
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"a{i}"
        )
    if st.button("📨 Nộp bài"):
        st.session_state.submitted = True

if st.session_state.submitted:
    score = sum(
        1 for i, q in enumerate(st.session_state.quiz)
        if st.session_state.answers.get(i) == q["correct_answer"]
    )
    st.success(f"🎉 Điểm: {score}/{len(st.session_state.quiz)}")
