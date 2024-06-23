import os
import sys
import gradio as gr

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import LOG
from model import GLMModel
from translator import PDFTranslator

def translate(input_file_path, source_language, target_language):
    LOG.info(f"Translating PDF {input_file_path} from {source_language} to {target_language}...")

    model = GLMModel(model="glm-4")

    if input_file_path is None:
        raise ValueError('PDF file is not specified.')
    
    file_format = "PDF"
    
    translator = PDFTranslator(model)
    return translator.translate_pdf(input_file_path, file_format)
    
demo = gr.Interface(
    fn=translate,
    inputs= [
        gr.File(label="上传 PDF 文件"),
        gr.Textbox(label="Source Language",placeholder="English",value="English"),
        gr.Textbox(label="Target Language",placeholder="Chinese",value="Chinese"),
    ],
    outputs=[
        gr.File(label="翻译后的 PDF 文件"),
    ],
)

demo.launch(share=False)
