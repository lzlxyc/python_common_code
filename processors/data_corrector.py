#
# # 中文文本纠错
from pycorrector.macbert.macbert_corrector import MacBertCorrector
use_model = "macbert4csc-base-chinese"
use_model = f"/data1/linzelun/workspace/pretrained_model_torch/{use_model}"
corrector = MacBertCorrector(use_model).correct
def zh_text_corrector(text:str) -> str:
    '''用于中文文本纠错'''
    return corrector(text).get('target',text)