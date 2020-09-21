import json
import pickle

def load_object(fn):
    with open(fn, 'rb') as fp:
        return pickle.load(fp)

def save_object(obj, fn, protocol=pickle.HIGHEST_PROTOCOL):
    with open(fn, 'wb') as fp:
        pickle.dump(obj, fp)

def load_object_json(fn):
    with open(fn, 'r') as fp:
        return json.load(fp)

def save_object_json(obj, fn):
    with open(fn, 'w') as fp:
        json.dump(obj, fp, indent=2)

def prettify(obj):
    return json.dumps(obj, indent=2)

def pf(obj): return prettify(obj)

def ppf(obj): print(pf(obj))

def capitalize_text(txt, default=None):
    if txt:
        txt = str(txt)
        txt = txt[:1].upper() + txt[1:].strip('\r')
        return txt
    return default

def enum_dic(dic):
    for id in dic:
        yield id
        for child in enum_dic(dic[id]):
            yield child

def dic_contains(dic, id):
    if id in dic: return id
    for key in dic:
        x = dic_contains(dic[key], id)
        if x: return x
    return None

def ensure_upper_list(ids):
    if not type(ids) is list: ids = [ids]
    ids = [id.upper() for id in ids if id]
    ids = list(dict.fromkeys(ids))
    return ids
