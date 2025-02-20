import gradio as gr
from ai_interface import get_model_names, list_models
import ollama

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
            
            with gr.Column(scale=4):
                chat_history = gr.Chatbot(height=500, bubble_full_width=False)
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

        def update_gallery(files):
            return [file.name for file in files] if files else None

        image_upload.change(fn=update_gallery, inputs=[image_upload], outputs=[gallery])
        return msg_input, chat_history, send_button, model_selector

    def generate_response(message, history, model):
        """Generate a response from the selected model"""
        if not message:
            return "", history

        # Simulate a response from the model
        response = ollama.generate(model=model, prompt=message)['response']
        
        history.append((message, response))
        return "", history

    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        msg_input, chat_history, send_button, model_selector = create_interface()
        
        # Message handlers
        msg_input.submit(generate_response, [msg_input, chat_history, model_selector], [msg_input, chat_history])
        send_button.click(generate_response, [msg_input, chat_history, model_selector], [msg_input, chat_history])

    demo.launch(share=False)
