#1.List
list = [3,5,8]
print("Before Inserting : ",list)
list.insert(3,4)
print("After Inserting : ",list)
list.remove(5)
print("After Removing : ",list)
list.append(7)
print("Inserting Integer At The End : ",list)
list.sort()
print("After Sorting : ",list)
list.pop(0)
print("Pop The First Element:",list)
list.reverse()
print("Reverse : ",list)

#2.calculator
c=1
while(c==1):
 a = int(input("Enter First Number :"))
 b = int(input("Enter Second Number :"))
 print("1.Add\n2.Sub\n3.Mul\n4.Div\n")
 ch = int(input("Enter Your Choice (1/2/3/4) : "))   
 if (ch==1):
    print("Addtion : ",a+b)
 elif (ch==2):
    print("Subtraction : ",a-b)
 elif (ch==3):
    print("Multiplication : ",a*b)
 elif (ch==4):
    print("Division : ",a/b)
 else:
    print("Invalid Choice")
 c=int(input("do you want to continue: 0 or 1 "))
    
# 3.CONCATENATION
a = "computer"
b = "science"
print("Caoncatenate : ",a+b)
print("Reverse : ",a[::-1])
print("Slice : ",b[2:5:1])
