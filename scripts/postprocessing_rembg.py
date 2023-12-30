from modules import scripts_postprocessing, ui_components
import gradio as gr

from modules.ui_components import FormRow
from modules.paths_internal import models_path
import rembg
import os

models = [
    "None",
    "isnet-general-use",
    "u2net",
    "u2netp",
    "u2net_human_seg",
    "u2net_cloth_seg",
    "silueta",
    "isnet-general-use",
    "isnet-anime",
]

class ScriptPostprocessingUpscale(scripts_postprocessing.ScriptPostprocessing):
    name = "Rembg"
    order = 20000
    model = None

    def ui(self):
        with ui_components.InputAccordion(False, label="Remove background") as enable:
            with gr.Row():
                model = gr.Dropdown(label="Remove background", choices=models, value="None")
                return_mask = gr.Checkbox(label="Return mask", value=False)
                alpha_matting = gr.Checkbox(label="Alpha matting", value=False)

            with gr.Row(visible=False) as alpha_mask_row:
                alpha_matting_erode_size = gr.Slider(label="Erode size", minimum=0, maximum=40, step=1, value=10)
                alpha_matting_foreground_threshold = gr.Slider(label="Foreground threshold", minimum=0, maximum=255, step=1, value=240)
                alpha_matting_background_threshold = gr.Slider(label="Background threshold", minimum=0, maximum=255, step=1, value=10)

            alpha_matting.change(
                fn=lambda x: gr.update(visible=x),
                inputs=[alpha_matting],
                outputs=[alpha_mask_row],
            )

        return {
            "enable": enable,
            "model": model,
            "return_mask": return_mask,
            "alpha_matting": alpha_matting,
            "alpha_matting_foreground_threshold": alpha_matting_foreground_threshold,
            "alpha_matting_background_threshold": alpha_matting_background_threshold,
            "alpha_matting_erode_size": alpha_matting_erode_size,
        }

    def process(self, pp: scripts_postprocessing.PostprocessedImage, enable, model, return_mask, alpha_matting, alpha_matting_foreground_threshold, alpha_matting_background_threshold, alpha_matting_erode_size):
        if not enable:
            return

        if not model or model == "None":
            return

        if "U2NET_HOME" not in os.environ:
            os.environ["U2NET_HOME"] = os.path.join(models_path, "u2net")

        pp.image = rembg.remove(
            pp.image,
            session=rembg.new_session(model),
            only_mask=return_mask,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
            alpha_matting_background_threshold=alpha_matting_background_threshold,
            alpha_matting_erode_size=alpha_matting_erode_size,
        )

        pp.info["Rembg"] = model
