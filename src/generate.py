import gradio as gr
import requests

FASTAPI_URL = "http://127.0.0.1:8000/chat"

def ask_galadirel(message, chat_history):
    if chat_history is None:
        chat_history = []

    try:
        response = requests.post(FASTAPI_URL, json={"query": message})
        data = response.json()
        answer = data.get("answer", "Error: No answer from backend")
    except Exception as e:
        answer = f"Error: {e}"

    # User bubble (right aligned, blue)
    user_msg = f"""
    <div style='background-color:#007bff;
                color:white;
                padding:10px 14px;
                border-radius:12px;
                max-width:70%;
                text-align:left;
                float:right;
                clear:both;
                margin:4px 0'>
        {message}
    </div>
    """

    # Galadirel bubble (left aligned, dark gray for readability)
    bot_msg = f"""
    <div style='background-color:#2f2f2f;
                color:#f5f5f5;
                padding:10px 14px;
                border-radius:12px;
                max-width:70%;
                text-align:left;
                float:left;
                clear:both;
                margin:4px 0'>
        {answer}
    </div>
    """

    chat_history.append((user_msg, bot_msg))
    return chat_history, ""  # clear input

with gr.Blocks(css="footer {visibility: hidden}") as demo:  # hides gradio footer
    gr.Markdown("<h1 style='text-align:center'>💬 Ask Galadirel</h1>")

    chatbot = gr.Chatbot(height=500, show_label=False)
    msg = gr.Textbox(
        placeholder="Ask me anything...",
        lines=1
    )
    submit_btn = gr.Button("Send")

    submit_btn.click(
        ask_galadirel,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

    msg.submit(
        ask_galadirel,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

demo.launch()
