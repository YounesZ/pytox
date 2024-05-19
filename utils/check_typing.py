
def is_list_of_dictionaries(elem):
    conds = False
    if isinstance(elem, list):
        cond1 = len(elem)>0
        cond2 = all( isinstance(i_, dict) for i_ in elem)
        conds = cond1 & cond2
    return conds


def is_list_of_strings(elem):
    conds = False
    if isinstance(elem, list):
        cond1 = len(elem) > 0
        cond2 = all(isinstance(i_, str) for i_ in elem)
        conds = cond1 & cond2
    return conds