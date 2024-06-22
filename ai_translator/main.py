from asyncio import timeout
from datetime import time
import sys
import os
from typing import Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config = ConfigLoader(args.config).load_config() if args.config else None

    def arg_or_config(arg, config_key: str) -> Optional[str]: 
        if arg is not None:
            return arg

        if config is not None:
            config_node = config
            for key in config_key.split('.'):
                config_node = config_node.get(key)
                if config_node is None:
                    break
            return config_node
        
    model_type = arg_or_config(args.model_type, 'common.model_type')
    if model_type == 'GLMModel':
        model = arg_or_config(args.glm_model, 'GLMModel.model')
        if model is None:
            raise ValueError('GLMModel.model is not specified.')
        api_key = arg_or_config(args.glm_api_key, 'GLMModel.api_key')
        model = GLMModel(model=model, api_key=api_key)
    elif model_type == 'OpenAIModel':
        model_name = arg_or_config(args.openai_model, 'OpenAIModel.model')
        if model_name is None:
            raise ValueError('OpenAIModel.model is not specified.')
        api_key = arg_or_config(args.openai_api_key, 'OpenAIModel.api_key')
        model = OpenAIModel(model=model_name, api_key=api_key)
    else:
        raise ValueError(f'Unsupported model type: {model_type}')

    pdf_file_path = arg_or_config(args.book, 'common.book')
    if pdf_file_path is None:
        raise ValueError('PDF file is not specified.')

    file_format = file_format if (file_format := arg_or_config(args.file_format, 'common.file_format')) else 'PDF'

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(pdf_file_path, file_format)
