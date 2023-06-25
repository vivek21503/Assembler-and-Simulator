import sys
from matplotlib import pyplot as plt
sys.setrecursionlimit(3000)
MEM = []

#with open("simulator.txt") as f:
#    MEM = f.read().strip().split("\n")
MEM = list(sys.stdin.read().strip().split("\n"))

# print(MEM)
register_values = ["0000000000000000","0000000000000000","0000000000000000","0000000000000000","0000000000000000","0000000000000000","0000000000000000","0000000000000000"]

dict_variables ={}

# it is taking integer and returning string
def decimalToBinary(n):
    if(n == 0):
        return "0000000000000000"
    
    a = bin(n).replace("0b", "")
    a = str(a)
    if(len(a) > 16):
        b = a[-16:]
    else:
        b = '0'*(16-len(a))
        b+=a    
    
    return b

def decimalToBinary_PC(n):
    
    a = bin(n).replace("0b", "")
    a = str(a)
    b = '0'*(8-len(a))
    b+=a

    return b

def decimalToBinary_fraction(n):
    
    a = bin(n).replace("0b", "")
    a = str(a)
    b = '0'*(3-len(a))
    b+=a

    return b


# taking string returns integer
def binaryToDecimal(n):
    value = 0;
    base = 1;
     
    temp = int(n)
    while(temp):
        last_digit = temp % 10
        temp = int(temp / 10)
        value += last_digit * base
        base = base * 2
    return value

# global definition 
PC = 0

def RF(register_name):
    index = binaryToDecimal(register_name)

    value =   binaryToDecimal(int(register_values[index]))
    return value

# starting of functions
def add(R1, R2,R3):
    index3 = binaryToDecimal(R3)
    val1 = RF(R1)
    val2 = RF(R2)
    
    if(val1+val2 >65535):
        l1 = list(register_values[7])
        l1[-4] = "1"
        register_values[7] = "".join(l1)
    else:
        register_values[index3] = decimalToBinary(val1+val2)

def sub(R1, R2,R3):
    index3 = binaryToDecimal(R3)
    val1 = RF(R1)
    val2 = RF(R2)

    if(val1-val2 <0):

        l1 = list(register_values[7])
        l1[-4] = "1"
        register_values[7] = "".join(l1)
        register_values[index3] = "0000000000000000"
        

    else:
        register_values[index3] = decimalToBinary(val1-val2)

def mov_register(R1, R2):
    index1 = binaryToDecimal(R1)
    index2 = binaryToDecimal(R2)
    register_values[index2] = register_values[index1]

def mov_immediate(R1, value):
    index1 = binaryToDecimal(R1)
    register_values[index1] = "0"*8 + value

def mul(R1, R2,R3):
    index3 = binaryToDecimal(R3)
    val1 = RF(R1)
    val2 = RF(R2)

    if(val1*val2 >65535):
    #    a=register_values[7]
        # val7 = RF("111")
        # register_values[7] = decimalToBinary(val7+8)
    #    register_values[7] = a
        l1 = list(register_values[7])
        l1[-4] = "1"
        register_values[7] = "".join(l1)
    else:
        register_values[index3] = decimalToBinary(val1*val2)
        

def div(R1, R2):
    val1 = RF(R1)
    val2 = RF(R2)
    register_values[0] = decimalToBinary(int(val1/val2))
    register_values[1] = decimalToBinary(val1%val2)


def ls(R1, imm):
    index1 = binaryToDecimal(R1)

    multiplier = pow(2, imm)

    val1 = RF(R1)
    register_values[index1] = decimalToBinary(val1*multiplier)


def rs(R1, imm):
    index1 = binaryToDecimal(R1)

    multiplier = pow(2, imm)

    val1 = RF(R1)
    register_values[index1] = decimalToBinary(int(val1/multiplier))

def xor(R1, R2, R3):
    index3 = binaryToDecimal(R3)
    val1 = RF(R1)
    val2 = RF(R2)

    register_values[index3] = decimalToBinary(val1^val2)

def Or(R1, R2, R3):
    index3 = binaryToDecimal(R3)
    val1 = RF(R1)
    val2 = RF(R2)

    register_values[index3] = decimalToBinary(val1|val2)

def And(R1, R2, R3):
    index3 = binaryToDecimal(R3)
    val1 = RF(R1)
    val2 = RF(R2)

    register_values[index3] = decimalToBinary(val1&val2)

def invert(R1, R2):
    index2 = binaryToDecimal(R2)
    val1 = RF(R1)

    register_values[index2] = decimalToBinary(~val1)

def compare(R1, R2):
    val1 = RF(R1)
    val2 = RF(R2)

    l1 = list(register_values[7])
    if(val1 == val2):
        l1[-1] = "1"
    elif(val1 > val2):
        l1[-2] = "1"
    else:
        l1[-3] = "1"
    register_values[7] = "".join(l1)


# here will be floating functions

def floatToDec(b, point_loc):
    sum =0
    loc = point_loc
    
    for i in b:
        if i != '.':
            sum+= pow(2, loc-1)*int(i)
            loc-=1            

    return sum

def ieeeTofloat(a):
    #changes 
    n = binaryToDecimal(a)
    a = register_values[n]
    a=a[8:]

# 00010000
    main_exponent = int(binaryToDecimal(a[:3]))
    if main_exponent <0 :
        # new_str = "0"
        new_str = "."
        new_str += "0"*(abs(main_exponent) - 1)
    
        new_str += "1"
        new_str += a[3:]

        ret = floatToDec(new_str, 0)

    else:
        new_str = "1"
        new_str += a[3:(3+main_exponent)]
        new_str += "."
        new_str += a[(3+main_exponent):]

        # print(new_str)


        ret = floatToDec(new_str, main_exponent+1)

    return ret


def convert_to_fraction(n):
    string = str(n)
    decimal = ""
    for i in range(len(string)):
        if(string[i] != '.'):
            decimal = decimal + string[i]
        else:
            break

    fraction = string[i+1:]
    res = ""
    if(decimal == "0"):
        res += "0."
    else:
        res = bin(int(decimal)).lstrip("0b") + "."
        
    for i in range(5):
        if(int(fraction) == 0):
            res += "0"*(5-i)
            break
        
        fraction = float("0."+ fraction)*2
        if(fraction >=1):
            res += "1"
            fraction -= 1
            fraction = str(fraction)[2:]
        else:
            res += "0"
            fraction = str(fraction)[2:]

    # print(res)
    # converting to IEEE 754 format 
    index  = 1 
    for i in range(len(res)):
        if(res[i] == "."):
            index = i 
            break
    
    # if first index is 0
    exponent = index-1
    mantissa = res[1:i] + res[i+1:(5-exponent + i + 1)]

    return "0"*8 + decimalToBinary_fraction(exponent) + mantissa

def mov_float(R1, value):
    index1 = binaryToDecimal(R1)
    register_values[index1] = "0"*8 + value 

def add_float(R1, R2, R3):
    index3 = binaryToDecimal(R3)
    R1 = ieeeTofloat(R1)
    R2 = ieeeTofloat(R2)

    if(R1 + R2 > 252):
        l1 = list(register_values[7])
        l1[-4] = "1"
        register_values[7] = "".join(l1)
    else:
        register_values[index3] = convert_to_fraction(R1 + R2)

def sub_float(R1, R2, R3):
    index3 = binaryToDecimal(R3)
    R1 = ieeeTofloat(R1)
    R2 = ieeeTofloat(R2)

    # print(type(R1))

    if(R1-R2 < 0):
        l1 = list(register_values[7])
        l1[-4] = "1"
        register_values[7] = "".join(l1)
        register_values[index3] = "0000000000000000"
        

    else:
        register_values[index3] = convert_to_fraction(R1-R2)

# for plotting a graph
list1 = []
cycle = 0
list2 = []
def ex_engine():
    global PC
    global cycle

    list1.append(PC)
    list2.append(cycle)

    instruction = MEM[PC]
    new_PC = PC + 1
    op = instruction[:5]

    # function calling 
    if(op == "10000"):
        add(instruction[7:10], instruction[10:13], instruction[13:16])
    elif(op == "10001"):
        sub(instruction[7:10], instruction[10:13], instruction[13:16])

    elif(op == "10010"):
        mov_immediate(instruction[5:8],instruction[8:])
    elif(op == "10011"):
        mov_register(instruction[10:13],instruction[13:])

    elif(op == "10110"):
        mul(instruction[7:10], instruction[10:13], instruction[13:16])
    elif(op == "10111"):
        div(instruction[10:13], instruction[13:])
    elif(op == "11001"):
        ls(instruction[5:8],instruction[8:])
    elif(op == "11000"):
        rs(instruction[5:8],instruction[8:])

    elif(op == "11010"):
        xor(instruction[7:10], instruction[10:13], instruction[13:16])
    elif(op == "11011"):
        Or(instruction[7:10], instruction[10:13], instruction[13:16])
    elif(op == "11100"):
        And(instruction[7:10], instruction[10:13], instruction[13:16])
    elif(op == "11101"):
        invert(instruction[10:13], instruction[13:])
    elif(op == "11110"):
        compare(instruction[10:13], instruction[13:])
    
    # load and store instructions 
    if(op == "10101"):      #for store instruction
        mem_add = instruction[8:]
        dict_variables[mem_add] = RF(instruction[5:8])
    
    elif(op == "10100"):        #for load function
        index = binaryToDecimal(instruction[5:8])
        mem_add = instruction[8:]
        if(mem_add not in dict_variables.keys()):
            dict_variables[mem_add] = "0000000000000000"
        register_values[index] = decimalToBinary(int(dict_variables[mem_add]))
    
    # for floating point numbers
    elif(op == "00010"):
        mov_float(instruction[5:8],instruction[8:])
    elif(op == "00000"):
        add_float(instruction[7:10], instruction[10:13], instruction[13:16])
    elif(op == "00001"):
        sub_float(instruction[7:10], instruction[10:13], instruction[13:16])

    # for jumping instructions
    elif(op == "11111"):
        new_PC = binaryToDecimal(instruction[8:])
    elif(op == "01100"):
        if(register_values[7][-3] == "1"):
            new_PC = binaryToDecimal(instruction[8:])

        if(register_values[7][-4] == "1"):
            register_values[7] = "0000000000001000"
        else:
            register_values[7] = "0000000000000000"
    elif(op == "01101"):
        if(register_values[7][-2] == "1"):
            new_PC = binaryToDecimal(instruction[8:])

        if(register_values[7][-4] == "1"):
            register_values[7] = "0000000000001000"
        else:
            register_values[7] = "0000000000000000"
    elif(op == "01111"):
        if(register_values[7][-1] == "1"):
            new_PC = binaryToDecimal(instruction[8:])

        if(register_values[7][-4] == "1"):
            register_values[7] = "0000000000001000"
        else:
            register_values[7] = "0000000000000000"
        

    # printing the pc and register values 
    # print(decimalToBinary_PC(PC), end = " ")
    # for i in range(len(register_values)):
    #     if(i == 7):
    #         print(register_values[i])
    #     else:
    #         print(register_values[i], end = " ")


    PC = new_PC     #updation of PC
    # function calling 
    if(PC != len(MEM)):
        cycle += 1
        ex_engine()
    else:
        return

ex_engine()

plt.plot(list2, list1)
plt.xlabel("Cycle")
plt.ylabel("PC")
plt.show()


# # here will be dump function 
# dict_variables = {key: val for key, val in sorted(dict_variables.items(), key = lambda ele: ele[0])}
# count = 0
# for i in MEM:
#     count += 1
#     print(i)
# for i in dict_variables.values():
#     count += 1
#     print(decimalToBinary(int(i)))
# for i in range(256 - count):
#     print("0000000000000000")
