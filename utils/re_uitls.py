# -*- coding: utf-8 -*-
'''
方法工具库
'''
import re
import torch
GPU = 3
# torch.cuda.set_device(GPU)
'''
#################################################
数据正则化处理方法
################################################
'''

def remove_punctuation(text)->str:
    # 定义正则表达式模式，去掉标点符号和数字
    pattern = r'[^\w\s]|[\d]|_|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩'
    result = re.sub(pattern, '', text)
    return result

    '''
        TODO:
            1. 命名符合开源规范: no_chinese_character -> check_chinese_character 或 has_chinese_character
    '''
def without_chinese_character(text)->str:
    # 定义正则表达式模式，匹配中文字符,判断字符串中是不是没有中文，没中文字符返回True
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    # 使用 search() 方法查找第一个匹配的中文字符
    result = pattern.search(text)
    return result is None

def is_all_chinese(text)->str:
    '''判断字符串是否全部都是中文,全是中文返回True'''
    text = text.replace(' ','')
    for _char in text:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    match = re.search(pattern, text)
    if match:
        return True
    return False

def remove_chinese_punctuation_numbers(text)->str:
    # 去掉中文字符、标点符号和数字
    text = remove_punctuation(text)
    filtered_text = re.sub(r'[\u4e00-\u9fa5]+', '', text)
    return filtered_text.strip()

def retain_number(text) ->str:
    '''只保留数字'''
    return re.sub(r'[^\d+]','', text)

def retain_chinese(text) ->str:
    # 只保留中文数据
    return re.sub(r'[^\u4e00-\u9fa5]', '', text)


def retain_zh_en(text):
    # 只保留中英文数据
    return re.sub(r'[^\u4e00-\u9fa5a-zA-Z]', '', text)

def filter_pinyin_with_tone(text):
    # 过滤出带音调的拼音
    pattern = r'[āáǎàēéěèīíǐìōóǒǒòūúǔùüǖǘǚǜ]'
    result = re.findall(pattern, text)
    return result

def remove_html_tags(text):
    '''去掉搜题结果中包含<xxx>的内容'''
    return re.sub(r"<.*?>", " ", text).replace('/',' ').replace('&nbsp;',' ')


def split_sentence_with_start_number_point(text:str) -> list:
    '''对包含数字和点开头的句子进行分割'''
    text = text.replace(')','）').replace('(','（').replace('?','？').replace('!','！')
    pattern_point = r'\b\d+\.[^\d]+\b'
    sentences_point = re.findall(pattern_point, text)

    pattern_bracket = r'\b\d+\）[^\d]+\b'
    sentences_bracket = re.findall(pattern_bracket, text)
    if len(sentences_point) >= len(sentences_bracket): return [sentences.strip() for sentences in sentences_point]
    return [sentences.strip() for sentences in sentences_bracket]

import unicodedata
def remove_pinyin_tone(pinyin_with_tone):
    '''去掉拼音的音调'''
    pinyin_without_tone = unicodedata.normalize('NFKD', pinyin_with_tone).encode('ascii','ignore')
    return pinyin_without_tone.decode()



def get_time():
    from datetime import datetime,timedelta
    # 获取当前日期和时间
    now = datetime.now() + timedelta(hours=8)
    # 提取年、月、日、时、分、秒
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    # 输出结果
    return f"\n进行作业批改，当前系统时间：{year}年{month}月{day}日 {hour}时{minute}分{second}秒" + '-'*50 + '\n'
