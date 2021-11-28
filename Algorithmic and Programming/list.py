print("Please insert a series of integers and type 'STOP' to stop")
integers = []
n = "zero"
while n != "STOP":
    n = input()
    if n != "STOP":
        n = int(n)
        integers.append(n)
print(integers)

max, min, i = 0,integers[0],0
while i < len(integers):
    if integers[i] < min:
        min = integers[i]
    if integers[i] > max:
        max = integers[i]
    i+=1
print("The maximum of this list is", max, "and its minimum is", min)

print("Enter one of the list's integers")
a = int(input())
b = 0
for i in integers:
    if i == a:
        b+=1
print("The integer", a, "occurs", b, "times")

c = integers[0]
check = True
for i in integers:
    if i >= c:
        c = i
    else:
        check = False
if check == True:
    print("This list is already sorted")
else:
    print("This list is yet to be sorted")
