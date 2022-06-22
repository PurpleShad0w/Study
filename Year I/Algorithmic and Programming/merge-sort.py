def merge(l,r):
    if len(l) == 0 or len(r) == 0:
        return l or r
    tab = []
    i, j = 0, 0
    while (len(tab) < len(l) + len(r)):
        if l[i] < r[j]:
            tab.append(l[i])
            i+= 1
        else:
            tab.append(r[j])
            j+= 1
        if i == len(l) or j == len(r):
            tab.extend(l[i:] or r[j:])
            break
    return tab
 
def sort(tab):
    if len(tab) <= 1:
        return tab
    m = len(tab)/2
    l = sort(tab[:m])
    r = sort(tab[m:])
    return merge(l, r)

T = [1,5,3,9,6,4]
print(sort(T))
