import gradio as gr
from dispatch import Dispatch


async def setup():
    dispatcher = Dispatch()
    await dispatcher.setup()
    return dispatcher


async def process_message(dispatcher, message, success_criteria, history):
    results = await dispatcher.run_superstep(message, success_criteria, history)
    return results, dispatcher


async def reset():
    new_dispatcher = Dispatch()
    await new_dispatcher.setup()
    return "", "", None, new_dispatcher


def free_resources(dispatcher):
    print("Cleaning up")
    try:
        if dispatcher:
            dispatcher.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Dispatch") as ui:
    gr.Markdown("## Dispatcher Personal Co-Worker")
    dispatcher = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Dispatch", height=300)
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Dispatcher")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    ui.load(setup, [], [dispatcher])
    message.submit(
        process_message, [dispatcher, message, success_criteria, chatbot], [chatbot, dispatcher]
    )
    success_criteria.submit(
        process_message, [dispatcher, message, success_criteria, chatbot], [chatbot, dispatcher]
    )
    go_button.click(
        process_message, [dispatcher, message, success_criteria, chatbot], [chatbot, dispatcher]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, dispatcher])


ui.launch(inbrowser=True, theme=gr.themes.Default(primary_hue="emerald"))
