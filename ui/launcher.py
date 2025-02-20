import gradio as gr
from ai_interface import get_model_names, list_models
from utils import ChatHistory

def launch():
    """
    Launch Gradio server.
    """
    chat_history_obj = ChatHistory()

    def chat_interface():
        """Creates and returns the chat interface components"""
        with gr.Row():
            with gr.Column(scale=1):
                model_selector = gr.Dropdown(
                    choices=get_model_names(list_models()),
                    label="Select Model",
                    value=get_model_names(list_models())[0] if get_model_names(list_models()) else None
                )
                chats = gr.Dataframe(
                    headers=["Chats"],
                    value=[["Chat 1"], ["Chat 2"], ["Chat 3"]],
                    show_label=False
                )
            
            with gr.Column(scale=4):
                chat_history = gr.Chatbot(height=500, bubble_full_width=False)
                with gr.Row():
                    with gr.Column(scale=12):
                        msg = gr.Textbox(
                            placeholder="Type your message here...",
                            show_label=False,
                            container=False
                        )
                        with gr.Row():
                            image_upload = gr.File(
                                label="Upload Images",
                                file_count="multiple",
                                file_types=["image"],
                                elem_id="image_upload",
                                height=120,
                                visible=True
                            )
                            gallery = gr.Gallery(
                                label="Preview",
                                show_label=False,
                                height=120,
                                visible=True,
                                columns=4
                            )
                    with gr.Column(scale=1):
                        send_btn = gr.Button("🚀")

        def update_gallery(files):
            return [file.name for file in files] if files else None

        image_upload.change(fn=update_gallery, inputs=[image_upload], outputs=[gallery])
        return msg, chat_history, send_btn, model_selector

    def chat_response(message, history, model):
        """Handle chat response using ChatClient"""
        if not message:
            return "", history

        chat_client = ChatClient(model=model)
        for h in history:
            chat_client.add_message(message=h[0], role=h[1])

        chat_client.add_message(message=message, role="user")
        
        # Get streaming response
        response = ""
        for chunk in chat_client.generate_response(message):
            if chunk.get('message', {}).get('content'):
                response += chunk['message']['content']
                yield "", history + [(message, response)]

        chat_client.add_message("assistant", response)
        return "", history + [(message, response)]

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        msg, chat_history, send_btn, model_selector = chat_interface()
        
        # Message handlers
        msg.submit(chat_response, [msg, chat_history, model_selector], [msg, chat_history])
        send_btn.click(chat_response, [msg, chat_history, model_selector], [msg, chat_history])

        # Add copy/edit buttons for each message
        chat_history.like_btn = "📋"  # Copy button
        chat_history.edit_btn = "✏️"  # Edit button

    demo.launch(share=False)
