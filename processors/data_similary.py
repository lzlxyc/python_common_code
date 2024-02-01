
'''
###########################################
文本相似度分析
###########################################

'''


def text_process(text:str):
    '''对文本进行预处理'''
    return ''.join(re.sub(r"[_,.;/'!@#$%^&*(){}《》：“？，。；‘、【】{}！@#￥%……&*（）<>?: ]",'',text))

def split_text(text:str, n=3):
    '''对字符串进行按照字符数n切分'''
    return list(set([text[idx:idx + n] for idx in range(len(text) + 1 - n)]))


def get_n_gram_score(user_question:str, search_question:str, n=3) -> float:
    '''doc_text为输入的题干，query_list为搜题题干,返回两个字符串的n-gram分数'''
    #print("user_question:",user_question,'\nsearch_question:',search_question)
    user_question_list = split_text(text_process(user_question), n)
    search_question_list = split_text(text_process(search_question), n)
    if not user_question_list or not search_question_list: return 0.0
    score = sum([1 for user_question in user_question_list if user_question in search_question_list])
    return score / len(user_question_list)


def get_n_gram_score_special_symbols(user_question:str, search_question:str):
    '''如果题干和搜题信息都共同包含一些特殊符号，就返回True'''
    special_symbols = '①②③④⑤⑥⑦⑧⑨⑩ABCDEFGHIZKL'
    return any(special_symbol in user_question for special_symbol in special_symbols) and \
           any(special_symbol in search_question for special_symbol in special_symbols)


def text_similary(user_question:str, search_question:str) -> float:
    '''计算两个文本相似度'''
    score = get_n_gram_score(user_question, search_question,3)
    if get_n_gram_score_special_symbols(user_question, search_question):
        score *= 1.2
    """
    Todo:后续加上答案的相似度
    """
    return score

def get_similary_text(user_question:str, question_info_list:list, n=3, max_score = 0.3):
    '''从搜题文本列表中，获取跟题干最相似的文本'''
    max_score = max_score
    similary_question_info = ''
    for idx,question_info in enumerate(question_info_list):
        score = get_n_gram_score(user_question, question_info,n=n)
        if score > max_score:
            similary_question_info = question_info
            max_score = score

    return similary_question_info


def get_similary_text_position(user_question:str, question_info_list:list, n=3, max_score = 0.3):
    '''从搜题文本列表中，获取跟题干最相似的文本的索引'''
    max_score = max_score
    position = -1
    for idx,question_info in enumerate(question_info_list):
        score = get_n_gram_score(user_question, question_info,n=n)
        # print("score:",score,user_question,'-->',question_info)
        if score > max_score:
            position = idx
            max_score = score

    return position,max_score


def get_similary_text_score(answer_list:list, question_answer:str, n=3):
    # return max([get_n_gram_score(answer,question_answer,n=n) for answer in answer_list])
    res = []
    for answer in answer_list:
        score = get_n_gram_score(answer,question_answer,n=n)
        print("score:",score,'answer:',answer)
        res.append(score)
    return max(res)


def get_similary_search_info(user_question:str, search_question_info_list:list, n=3, max_score = 0.3):
    '''获取最相似题目的搜题信息'''
    max_score = max_score
    similary_search_info = {}
    for search_info in search_question_info_list:
        score = get_n_gram_score(user_question, search_info.get('question_text',''),n=n)
        #print(f"score:{score},search_info:{search_info.get('question_text','')}")
        if score > max_score:
            similary_search_info = search_info
            max_score = score
    # print("max_score:",max_score)
    return similary_search_info, max_score


def get_similary_question_answer(user_question:str, search_question_info_list:list, n=3, max_score = 0.3):
    '''获取最相似题目的答案'''
    similary_search_info, _ = get_similary_search_info(user_question, search_question_info_list,n,max_score)
    return similary_search_info.get('question_answer', ''), similary_search_info.get('question_text', '')


from similarities import BertSimilarity
use_model = "sbert-base-chinese-nli"  # 这里可以进行模型的替换
use_model = f"/data1/linzelun/workspace/pretrained_model_torch/{use_model}"
similary_model = BertSimilarity(model_name_or_path=use_model)
def get_sentence_meaning_similary_score(text1,text2):
    """计算两个句子的语义相似度"""
    score = similary_model.similarity(text1,text2)
    # print('*'*50,'\n',score,text1,'-->',text2)
    return score


def get_meaning_similary_answer(questions,all_search_answer_list):
    if not all_search_answer_list: return ''
    search_info_list = [remove_html_tags(search_info['question_text']) for search_info in all_search_answer_list]
    score_list = get_sentence_meaning_similary_score(questions,search_info_list)
    return remove_html_tags(all_search_answer_list[torch.argmax(score_list).item()]['question_answer'])



def is_original_question(parent_title:str, parent_search_info:list):
    '''针对阅读理解、填空题，未召回的数据，进行原题判断，
    这里的条件需要设置相对严格，如果通过原题判断，不在答案里面的就直接批改为“错”
    1)利用n-gram进行相似度计算
    2）利用语义相似度
    3）优先大框数据进行判断，然后是小框
    '''
    if not parent_title or not parent_search_info: return False
    if len(parent_title) > 15: n = 3
    else: n = 1
    _,score = get_similary_search_info(parent_title,parent_search_info,n=n)

    search_info_list = [remove_html_tags(search_info['question_text']) for search_info in parent_search_info]
    score_list = get_sentence_meaning_similary_score(parent_title, search_info_list)
    score_mearing = torch.argmax(score_list).item()
    return score >= 0.9 or score_mearing >= 0.9