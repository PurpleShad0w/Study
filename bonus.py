def create_stack():
  return []

def is_empty(s):
  return s == []

def peek(s):
  if is_empty(s):
    print("Error, this is empty")
  else:
    return s[0]

def push(s,x):
  if is_empty(s):
    s.append(x)
  else:
    s = [x] + s
  return s

def stack(s):
  s.pop(0)
  return s

def bonus_1(a):
    s,b,c = create_stack(),0,0
    while is_empty(a) == False:
        if peek(a) != "+" and peek(a) != "-" and peek(a) != "/" and peek(a) != "*" and peek(a) != "**":
            push(s,peek(a))
            stack(a)
        elif peek(a) == "+":
            b = int(peek(s))
            stack(s)
            c = int(peek(s))
            stack(s)
            push(s,b+c)
        elif peek(a) == "-":
            b = int(peek(s))
            stack(s)
            c = int(peek(s))
            stack(s)
            push(s,c-b)
        elif peek(a) == "*":
            b = int(peek(s))
            stack(s)
            c = int(peek(s))
            stack(s)
            push(s,b*c)
        elif peek(a) == "/":
            b = int(peek(s))
            stack(s)
            c = int(peek(s))
            stack(s)
            push(s,c//b)
        elif peek(a) == "**":
            b = int(peek(s))
            stack(s)
            c = int(peek(s))
            stack(s)
            push(s,c**b)
    return(int(peek(s)))

start_list = ["[","{","("] 
end_list = ["]","}",")"] 

def bonus_2(a):
  s = create_stack()
  for i in range(len(a)):
    if i in start_list:
      s.append(i)
    elif i in end_list:
      p = end_list.index(i)
      if (is_empty(s) == False) and (start_list[p] == s[-1]):
        stack(s)
      else:
        return "Unbalanced parentheses"
  if is_empty(s):
    return "Balanced parentheses"
