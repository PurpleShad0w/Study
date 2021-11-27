a = [2,4,5,6,7]

def is_sorted(a):
    check = 0
    for i in range(len(a)):
        if check > a[i]:
            return False
        check = a[i]
    return True

print(is_sorted(a))

def add(a,x):
    for i in range(len(a)):
        if a[i] < x < a[i+1]:
            a.insert(i+1,x)
            break
    return a

print(add(a,3))
tab = [18,0,2,4,9,3,7,1]

def cocktail(tab):
    swap = True
    n = len(tab)
    check = 0
    while swap:
        swap = False
        if check == 0:
            for i in range(n-1):
                if tab[i] > tab[i+1]:
                    tab[i],tab[i+1] = tab[i+1],tab[i]
                    swap = True
            check = 1
            n = n - 1
        if check == 1:
            for j in range(n,1,-1):
                if tab[j] < tab[j-1]:
                    tab[j],tab[j-1] = tab[j-1],tab[j]
                    swap = True
            check = 0
    return tab

print(cocktail(tab))
boo = [True,False,True,False,False,True,True]

def sort_bool(boo):
    for i in range(len(boo)):
        if boo[i] == True:
            boo.append(boo.pop(boo.index(i)))
