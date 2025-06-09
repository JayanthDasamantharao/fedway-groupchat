# import streamlit as st
# from rag_chain import ask_question, get_top_doc_score

# # === Initialize session state ===
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "mode" not in st.session_state:
#     st.session_state.mode = "AI"
# if "ai_suggestion" not in st.session_state:
#     st.session_state.ai_suggestion = ""
# if "ai_score" not in st.session_state:
#     st.session_state.ai_score = 0.0

# st.set_page_config(page_title="POET Assistant", layout="wide")
# st.title("AI Assistant with Human Escalation")

# # === Chat Panel ===
# st.markdown("### 💬 Chat")
# for msg in st.session_state.messages:
#     if msg["role"] == "assistant":
#         icon = msg.get("sender", "AI")
#         avatar = "🧑‍💼" if icon == "HUMAN" else "🤖"
#     else:
#         avatar = "👤"

#     with st.chat_message(msg["role"], avatar=avatar):
#         st.markdown(msg["content"])

# # === Chat input ===
# user_input = st.chat_input("Ask about POET system...")
# if user_input:
#     with st.chat_message("user"):
#         st.markdown(user_input)
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     if st.session_state.mode == "AI":
#         with st.chat_message("assistant", avatar="🤖"):
#             response = ask_question(user_input)
#             score = get_top_doc_score(user_input)
#             st.session_state.ai_score = score

#             if "let me connect you to a human" in response.lower() or score < 0.3:
#                 st.session_state.mode = "HUMAN"
#                 response += "\n\n🔁 Switching to a human representative..."

#             st.markdown(response)
#             st.session_state.messages.append({"role": "assistant", "content": response, "sender": "AI"})

#     elif st.session_state.mode == "HUMAN":
#         # AI prepares a suggestion for human rep
#         response = ask_question(user_input)
#         score = get_top_doc_score(user_input)
#         st.session_state.ai_suggestion = response
#         st.session_state.ai_score = score

#         with st.chat_message("assistant", avatar="🤖"):
#             st.info("🤖 AI has made a suggestion. Review it on the right-hand panel.")

# # === Human Panel Sidebar ===
# with st.sidebar:
#     st.markdown("### 🧑‍💼 Human Panel")

#     if st.session_state.mode == "HUMAN":
#         st.success("Chat is now routed to a human rep.")

#         # === Optional: Hand back to AI ===
#         if st.button("🤖 Pass control back to AI"):
#             st.session_state.mode = "AI"
#             st.success("AI will now take over the conversation.")
#             st.rerun()

#         # === AI Suggestion Preview ===
#         if st.session_state.ai_suggestion:
#             st.markdown("### 🤖 AI Suggestion")
#             st.info(st.session_state.ai_suggestion)
#             st.text(f"Confidence Score: {st.session_state.ai_score:.3f}")

#             if st.button("✅ Send AI Response"):
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": st.session_state.ai_suggestion,
#                     "sender": "AI"
#                 })
#                 st.session_state.ai_suggestion = ""
#                 st.rerun()

#         # === Human Reply ===
#         if st.session_state.get("reset_rep_reply"):
#             st.session_state["rep_reply"] = ""
#             st.session_state["reset_rep_reply"] = False

#         human_reply = st.text_area("🧑‍💼 Your message to user:", key="rep_reply")

#         if st.button("Send Response", key="send_rep_response"):
#             if human_reply.strip():
#                 st.session_state.messages.append({"role": "assistant", "content": human_reply, "sender": "HUMAN"})
#                 st.session_state["reset_rep_reply"] = True
#                 st.session_state.ai_suggestion = ""  # Clear AI suggestion
#                 st.rerun()

#         # === Ask AI Privately ===
#         st.markdown("---")
#         st.markdown("### 🤖 Ask AI Privately")

#         private_query = st.text_area("Ask AI (user won't see this):", key="private_ai_input")
#         if st.button("Ask AI Privately"):
#             if private_query.strip():
#                 ai_response = ask_question(private_query, suppress_escalation=True)
#                 st.success("AI Response (Private):")
#                 st.info(ai_response)

#         # === Summarize Chat ===
#         st.markdown("---")
#         st.markdown("### 📜 Summarize User's Query")

#         if st.button("Summarize Chat"):
#             user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
#             user_history = "\n".join(user_msgs)

#             summary_prompt = (
#                 "Please summarize the following conversation history from the user. "
#                 "Just give me the key questions or topics they asked:\n\n" + user_history
#             )

#             summary = ask_question(summary_prompt, suppress_escalation=True)
#             st.success("User Query Summary:")
#             st.info(summary)

#     else:
#         st.info("You're in AI mode. Rep tools will appear here after escalation.")

# ====================================================================================


import streamlit as st
from rag_chain import ask_question, get_top_doc_score

# === Initialize session state ===
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "AI"
if "ai_suggestion" not in st.session_state:
    st.session_state.ai_suggestion = ""
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0.0

st.set_page_config(page_title="POET Assistant", layout="wide")
st.title("AI Assistant with Human Escalation")

# === Chat Panel ===
st.markdown("### 💬 Chat")
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        icon = msg.get("sender", "AI")
        avatar = "🧑‍💼" if icon == "HUMAN" else "🤖"
    else:
        avatar = "👤"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# === Chat input ===
user_input = st.chat_input("Ask about POET system...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if st.session_state.mode == "AI":
        with st.chat_message("assistant", avatar="🤖"):
            response = ask_question(user_input)
            score = get_top_doc_score(user_input)
            st.session_state.ai_score = score

            if "let me connect you to a human" in response.lower() or score < 0.3:
                st.session_state.mode = "HUMAN"
                response += "\n\n🔁 Switching to a human representative..."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response, "sender": "AI"})

    elif st.session_state.mode == "HUMAN":
        # AI prepares a suggestion for human rep
        response = ask_question(user_input)
        score = get_top_doc_score(user_input)
        st.session_state.ai_suggestion = response
        st.session_state.ai_score = score

        with st.chat_message("assistant", avatar="🤖"):
            st.info("🤖 AI has made a suggestion. Review it on the right-hand panel.")

# === Human Panel Sidebar ===
with st.sidebar:
    st.markdown("### 🧑‍💼 Human Panel")

    if st.session_state.mode == "HUMAN":
        st.success("Chat is now routed to a human rep.")

        # === AI Suggestion Preview ===
        if st.session_state.ai_suggestion:
            st.markdown("### 🤖 AI Suggestion")
            st.info(st.session_state.ai_suggestion)
            st.text(f"Confidence Score: {st.session_state.ai_score:.3f}")

            if st.button("✅ Send AI Response"):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": st.session_state.ai_suggestion,
                    "sender": "AI"
                })
                st.session_state.ai_suggestion = ""
                st.rerun()

        # === Pass control back to AI ===
        if st.button("🤖 Pass control back to AI"):
            st.session_state.mode = "AI"
            # Notify in chat
            takeover_notice = "AI is now taking over the conversation..."
            st.session_state.messages.append({"role": "assistant", "content": takeover_notice, "sender": "AI"})

            # Inject suggestion as official message
            if st.session_state.ai_suggestion:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": st.session_state.ai_suggestion,
                    "sender": "AI"
                })
                st.session_state.ai_suggestion = ""

            st.success("AI has taken over. User will see the AI's suggestion now.")
            st.rerun()

        # === Human reply form ===
        if st.session_state.get("reset_rep_reply"):
            st.session_state["rep_reply"] = ""
            st.session_state["reset_rep_reply"] = False

        human_reply = st.text_area("🧑‍💼 Your message to user:", key="rep_reply")

        if st.button("Send Response", key="send_rep_response"):
            if human_reply.strip():
                st.session_state.messages.append({"role": "assistant", "content": human_reply, "sender": "HUMAN"})
                st.session_state["reset_rep_reply"] = True
                st.session_state.ai_suggestion = ""
                st.rerun()

        # === Ask AI Privately ===
        st.markdown("---")
        st.markdown("### 🤖 Ask AI Privately")

        private_query = st.text_area("Ask AI (user won't see this):", key="private_ai_input")
        if st.button("Ask AI Privately"):
            if private_query.strip():
                ai_response = ask_question(private_query, suppress_escalation=True)
                st.success("AI Response (Private):")
                st.info(ai_response)

        # === Summarize Chat ===
        st.markdown("---")
        st.markdown("### 📜 Summarize User's Query")

        if st.button("Summarize Chat"):
            user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
            user_history = "\n".join(user_msgs)

            summary_prompt = (
                "Please summarize the following conversation history from the user. "
                "Just give me the key questions or topics they asked:\n\n" + user_history
            )

            summary = ask_question(summary_prompt, suppress_escalation=True)
            st.success("User Query Summary:")
            st.info(summary)

    else:
        st.info("You're in AI mode. Rep tools will appear here after escalation.")