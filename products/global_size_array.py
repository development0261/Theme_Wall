

def distinct_size(request,sizes):
    res = []
    for i in sizes:
        if i not in res:
            res.append(i)
    return res