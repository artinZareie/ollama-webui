import gradio as gr
from ai_interface import get_model_names, list_models
import ollama
from utils import ChatHistory

def launch():
    """
    Launch Gradio server.
    """

    models_list = list_models()

    def create_interface():
        """Creates and returns the chat interface components"""
        with gr.Row():
            with gr.Column(scale=1):
                model_selector = gr.Dropdown(
                    choices=get_model_names(models_list),
                    label="Select Model",
                    value=get_model_names(models_list)[0]
                )

                chats = gr.Dataframe(
                    headers=["Chats"],
                    value=[["Chat 1"], ["Chat 2"], ["Chat 3"]],
                    show_label=False
                )
            with gr.Column(scale=4, elem_classes="chat-container"):
                chat_history = gr.Chatbot(bubble_full_width=False, elem_classes="chatbot")
                with gr.Row():
                    with gr.Column(scale=12):
                        msg_input = gr.Textbox(
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
                        send_button = gr.Button("🚀")
                        # New trash button for deleting current chat.
                        delete_chat_button = gr.Button("🗑️")

        def update_gallery(files):
            return [file.name for file in files] if files else None

        image_upload.change(fn=update_gallery, inputs=[image_upload], outputs=[gallery])
        return msg_input, chat_history, send_button, delete_chat_button, model_selector

    def generate_response(message, history, model):
        """Generate a streamed response from the selected model"""
        if not message:
            yield "", history
            return

        chat_history_obj.append_user_message(message)
        response = ""
        stream = ollama.chat(
            model=model,
            messages=chat_history_obj.get_dict(),
            stream=True,
        )
        for chunk in stream:
            new_text = chunk['message']['content']
            response += new_text
            # Update the last user message with the current assistant response
            chat_history_obj.history_list[-1] = (chat_history_obj.history_list[-1][0], response)
            yield "", chat_history_obj.get_list()

    # New function to clear the chat history.
    def clear_chat():
        chat_history_obj.clear()
        return []  # update the chat UI with an empty history

    chat_history_obj = ChatHistory()

    with gr.Blocks(theme=gr.themes.Soft(), css="""
.chat-container { display: flex; flex-direction: column; height: 100vh; }
.chat-container > .chatbot { flex: 1; overflow: auto; }
""") as chat_interface:
        msg_input, chat_history, send_button, delete_chat_button, model_selector = create_interface()
        
        msg_input.submit(generate_response, [msg_input, chat_history, model_selector], [msg_input, chat_history])
        send_button.click(generate_response, [msg_input, chat_history, model_selector], [msg_input, chat_history])
        # Wire the trash button to clear the chat.
        delete_chat_button.click(clear_chat, inputs=[], outputs=chat_history)

    chat_interface.launch(share=False)
