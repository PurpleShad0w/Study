from turtle import *
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

def read():
    f = open("parameters",mode = "r")
    sys = {}
    for line in f.readlines():
        line = line.replace("\n","").replace('"',"")
        axiom = line.split(" = ")
        if len(axiom) == 1:
            sys["rules"] += axiom[0]
        else:
            sys[axiom[0]] = axiom[1]
    sys["rules"] = sys["rules"].split(" ")[:-1]
    sys["axiom"] = sys["axiom"][:-1] if sys["axiom"][:-1] == " " else sys["axiom"]
    sys["angle"] = int(sys["angle"])
    sys["size"] = int(sys["size"])
    sys["level"] = int(sys["level"])
    temp = sys["rules"]
    sys["rules"] = {}
    for rule in temp:
        sys["rules"][rule.split("=")[0]] = rule.split("=")[1]
    return sys

def generate(sys):
    for lev in range(sys["level"]):
        temp = ""
        for s in sys["axiom"]:
            temp += sys["rules"][s] if s in sys['rules'].keys() else s
        sys["axiom"] = temp
    return sys


def draw(sys):
    s = []
    for axe in sys["axiom"]:
        if axe == "a":
            pd(); fd(sys["size"])
        elif axe == "b":
            pu(); fd(sys["size"])
        elif axe == "-":
            left(sys["angle"])
        elif axe == "+":
            right(sys["angle"])
        elif axe == "*":
            right(180)
        elif axe == "[":
            s.append(pos())
        elif axe == "]":
            goto(s.pop())
    exitonclick()
                      
draw(generate(read()))
