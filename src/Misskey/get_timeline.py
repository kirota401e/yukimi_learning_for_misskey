# 1つ上のディレクトリの絶対パスを取得し、sys.pathに登録する
import sys
import os
from os.path import dirname
parent_dir = dirname(dirname(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir) 

import re
from collections import deque
from ngword_filter import is_ngword
import random
from misskey import Misskey
import json
import requests
import time
misskey = Misskey(os.environ['SERVER'], i=os.environ['TOKEN'])

#Misskey API json request用
get_tl_url = "https://" + os.environ['SERVER'] + "/api/notes/timeline"
limit = 30
get_tl_json_data = {
    "i" : os.environ['TOKEN'],
    "limit": limit,
}


# ToDo:この部分をmfm-jsでデコードするようにする
def get_tl_misskey():
    response = requests.post(
        get_tl_url,
        json.dumps(get_tl_json_data),
        headers={'Content-Type': 'application/json'})
    post_hash_list = response.json()
    #print(post_hash_list)
    import pdb; pdb.set_trace()
    for i in post_hash_list:
        if not 'myReaction' in i:
            print(i)
    time.sleep(100)
    choice_note = random.choice(post_hash_list)
    choice_id = str(choice_note["id"]) 
    choice_text = str(choice_note["text"])
    line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", choice_text)
    line = re.sub(r'@.*', "", line)
    line = re.sub(r'#.*', "", line)
    line = re.sub(r"<[^>]*?>", "", line)
    line = re.sub(r"\(.*", "", line)
    line = line.replace('\\', "")
    line = line.replace('*', "")
    line = line.replace('\n', "")
    line = line.replace('\u3000', "")
    line = line.replace('俺', "私")
    line = line.replace('僕', "私")
    line = line.replace(' ', "")
    mfm_judge = list(line)
    for one_letter in mfm_judge:
        if one_letter == '$':
            get_tl_misskey()
    #自分自身の投稿を除外
    if choice_note["user"]["username"] == "Yukimilearning" or choice_note['cw'] != None:
        get_tl_misskey()
    #フォロワー限定投稿を除外
    if choice_note["visibility"] == "followers":
        get_tl_misskey()
    #センシティブワード検知
    if is_ngword(line) == True or line == "None" or line == "":
        get_tl_misskey()
    try:
        if not 'myReaction' in choice_note:
            misskey.notes_reactions_create(choice_id,"❤️")
            return(line)
        else:
            get_tl_misskey()
    except:
        get_tl_misskey()
    
