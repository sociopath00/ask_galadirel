import gradio as gr
import requests

# FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/chat"

# Function to call FastAPI and update chat
def ask_galadirel(message, chat_history):
    if chat_history is None:
        chat_history = []

    try:
        response = requests.post(FASTAPI_URL, json={"query": message})
        data = response.json()
        answer = data.get("answer", "Error: No answer from backend")
    except Exception as e:
        answer = f"Error: {e}"

    # Add user message and Galadirel response as styled HTML
    chat_history.append((
        f"<div style='background-color:#007bff;color:white;padding:8px;border-radius:10px;max-width:70%;margin-left:auto'>{message}</div>",
        f"<div style='background-color:#e5e5e5;color:black;padding:8px;border-radius:10px;max-width:70%;margin-right:auto'>{answer}</div>"
    ))

    return chat_history, ""  # clear input

# Gradio Chat Interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align:center'>💬 Ask Galadirel</h1>")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(
        label="Type your question here...",
        placeholder="Ask me anything...",
        lines=1
    )
    submit_btn = gr.Button("Send")

    submit_btn.click(
        ask_galadirel,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    # Enter key to submit
    msg.submit(
        ask_galadirel,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

# Launch app
demo.launch()
