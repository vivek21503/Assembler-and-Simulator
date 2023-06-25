import sys
l3 =list(sys.stdin.read().split("\n"))
#with open("assembler.txt") as f:
#    l3 = f.read().split("\n")
# wo_variables = []
# with open("assembler.txt") as f:

def decimalToBinary_fraction(n):
    
    a = bin(n).replace("0b", "")
    a = str(a)
    b = '0'*(3-len(a))
    b+=a

    return b

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

    # if(index == 1):
    #     if(res[0] == "0"):
    #         for i in range(index, len(res)):
    #             if(res[i] == "1"):
    #                 exponent = -(i - index)
    #                 if(i+1 == len(res)):
    #                     mantissa = "0"*5
    #                 else:
    #                     mantissa = res[i+1:] + "0"*(5-(len(res) - 1- i))
    #                 break
    # exponent += 3
    # return "0"*8 + decimalToBinary_fraction(exponent) + mantissa
    return decimalToBinary_fraction(exponent) + mantissa

# a = f.read()
# l3 = a.split("\n")
length = len(l3)
while(l3[-1]==''):
    l3.pop(-1)

for i in range(0, len(l3)):
    l3[i]=l3[i].strip()
    

def search_index(list_search):
    # list_search = " ".join(list_search)
    for i in range(0, len(l3)):
        temp = l3[i].split()
        if(list_search == temp):
            return i + 1

dict = {
    "add":["10000", 'A'],
    "addf":["00000", 'A'],

    "sub":["10001", 'A'],
    "subf":["00001", 'A'],

    "mov1":["10010", 'B'],
    "movf":["00010", 'B'],
    "mov":["10011", 'C'],
    "ld":["10100", 'D'],
    "st":["10101", 'D'],
    "mul":["10110", 'A'],
    "div":["10111", 'C'],

    "rs":["11000","B"],
    "ls":["11001", 'B'],
    "xor":["11010", 'A'],

    "or":["11011", 'A'],
    "and":["11100", 'A'],
    "not":["11101", 'C'],
    "cmp":["11110", 'C'],
    "jmp":["11111", 'E'],
    "jlt":["01100", 'E'],
    "jgt":["01101", 'E'],
    "je":["01111", 'E'],
    "hlt":["01010", 'F']
}

dict_reg = {
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111"
}

errors =["No error","Typos in instruction name or register name"
,"Use of undefined variables"
,"Use of undefined labels"
,"Illegal use of FLAGS register"
,"Illegal Immediate values (more than 8 bits)"
,"Misuse of labels as variables or vice-versa"
,"Variables not declared at the beginning"
,"Missing hlt instruction"
,"hlt not being used as the last instruction", 
"General Syntax Error"]

def decimalToBinary(n):
    
    a = bin(n).replace("0b", "")
    a = str(a)
    b = '0'*(8-len(a))
    b+=a

    return b


count = 0       #it is telling that how many instruction are there in instructions
ins = []
var_count = 0
labels = {}
variables = []



def label():
    # a = ""
    # with open("assembler.txt") as f:
    #     a = f.read().split("\n")
    # print(l3)
    a = l3.copy() 
    # str1 = "label: label: add R0 R1 R3 R4"
    # print(str1.split())
    # print(search_index(str1.split()))

    for i in range(0, len(a)):
        # if empty list or for a new line 
        if(a[i] == ''):
            continue

        else:
            global count
            global var_count
            temp = a[i].split()
            # if a label is defined or declared

            if(temp[0][-1] == ':'):
                if(len(temp) == 1):
                    labels[temp[0][:-1]] = count + 1
                else:
                    # when after a label something is written 
                    if(temp[1] == "var"):
                        try:
                            che = int(temp[2])
                            real1 =1
                        except:
                            pass
                        if(real1==1):
                            print("line", search_index(a[i].split()), end =": ")
                            print(errors[10])
                        

                        if(len(temp) == 3):
                            try:
                                real1 =0


                                che = int(temp[2])
                                real1 =1
                            except:
                                pass
                            if(real1==1):
                                
                                print("line", search_index(a[i].split()), end =": ")
                              
                                print(errors[10])
                                exit()
                            variables.append(temp[2])
                            var_count += 1
                        else:
                            
                            print("line", search_index(a[i].split()), end =": ")
                            print(errors[10])
                            exit()
                    else:
                        for j in range(len(temp)):
                            if(temp[j][-1] == ':'):
                                labels[temp[j][:-1]] = count
                        # labels[temp[0][:-1]] = count
                        ins.append(temp[j:])
                        count += 1
                # count += 1

            elif(temp[0] == "var"):
                if(len(temp)==2):
                    real2 =0
                    try:
                        che = int(temp[1])
                        real2 =1
                    except:
                        pass
                    if(real2==1):
                        
                        print("line", search_index(a[i].split()), end =": ")
                        print(errors[10])
                        exit()
                    variables.append(temp[1])
                    var_count += 1
                else:
                  #--------------------------------------
                    # print(a[i])
                    print("line", search_index(a[i].split()), end =": ")
                    print(errors[10])
                    exit()
            else:
                ins.append(temp)
                count += 1        

def fun_A(l1, ans , error_index):
    if(len(l1)==4):
        try:
            ans+= '0'*2
            ans+= dict_reg[l1[1]]
            ans+= dict_reg[l1[2]]
            ans+= dict_reg[l1[3]]

            
        except:
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[1])
            exit()

        if(l1[1] != "FLAGS" and l1[2] != "FLAGS" and l1[3] != "FLAGS"):
            return ans


        else:
            # print(search_index(l1))
            print("line",error_index, end=": ")
            # print("1")

            print(errors[4])
            exit()
            


    else:
        # print(search_index(l1))
        print("line",error_index, end=": ")

        print(errors[10])
        exit()


def fun_B(l1, ans , error_index):
    if(len(l1)==3):
        try:
            ans += dict_reg[l1[1]]
        except:
            print("line",error_index, end=": ")
            print(errors[1])
            exit()
            
        if(l1[1]=="FLAGS"):
            print("line",error_index, end=": ")
            print(errors[4])
            exit()

        a = l1[2]
        flag1 =0
        # flag2 =0

        try:
            if '.' in a[1:]:
                a = float(a[1:])
                flag1 =0
            else:
                a = int(a[1:])
                flag1 =1
        except:
            print("line",error_index, end=": ")
            

            print(errors[5])
            exit()

        if(flag1 ==1):
            if(a>=0 and a<=255 and l1[0] != "movf"):          
            
                a = decimalToBinary(a)

                ans += str(a) 
                return ans 

            elif(a<0 or a>255 or l1[0] == "movf"):
                print("line",error_index, end=": ")
                print(errors[5])
                exit()
        else:
            if(a>=1 and a<=252 and l1[0] == "movf"): 
                # a = check_a

            
                a = convert_to_fraction(a)

                ans += str(a) 
                return ans 

            elif(a<1 or a>252 or l1[0] != "movf"):
                print("line",error_index, end=": ")
                print(errors[5])
                exit()
    
        # binary conversion

    else:

        print("line",error_index, end=": ")
        print(errors[10])
        exit()


def fun_C(l1, ans , error_index):

    if (len(l1) == 3):
        try:
            ans += "00000"
            ans += dict_reg[l1[1]]
            ans += dict_reg[l1[2]]
        except:

            # print(search_index(l1))
            print("line",error_index, end=": ")

            

            print(errors[1])
            exit()

        if(l1[2]=="FLAGS"):
            
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[4])
            exit()

        if(l1[1]=="FLAGS" and l1[0] != "mov"):
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[4])
            exit()


        return ans
            

    else:
        #  print(search_index(l1))
        print("line",error_index, end=": ")

        print(errors[10])
        exit()

def fun_D(l1, ans , error_index):

    if(len(l1) ==3):
        try:
            ans += dict_reg[l1[1]]
        except:
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[1])
            exit()

        if(l1[1]=="FLAGS"):
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[4])
            exit()

        address = len(ins)

        if(l1[2] not in variables and l1[2] in labels.keys()):
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[6]) 
            exit()


        if(l1[2] not in variables):
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[2]) 
            exit()

        # elif(l1[2] in labels.keys()):
            print(search_index(l1))
            print("line",error_index, end=": ")

        #     print(errors[6])
        #     exit()
        
        else:
            for i in range(0, len(variables)):
                if(variables[i] == l1[2]):
                    address += i
                    break
                
            ans += decimalToBinary(address)

            return ans 
    else:
        # print(search_index(l1))
        print("line",error_index, end=": ")
    
        print(errors[10])
        exit() 

def fun_E(l1, ans, error_index):
    if(len(l1) == 2):
        
        ans += "000"
       

        address = 0
        new_label = l1[1]
        if(l1[1] not in labels.keys() and l1[1] in variables):
            # print(search_index(l1))
            print("line",error_index, end=": ")
            print(errors[6]) 
            exit()

        # if(l1[1] in variables):
            print(search_index(l1))
            print("line",error_index, end=": ")
        #     print(errors[6]) # here error correction
        #     exit()

        elif(l1[1] not in labels.keys()):
            # print(search_index(l1))
            print("line",error_index, end=": ")

            print(errors[3])    # here error correction
            exit()
        else:
            for i in labels.keys():
                if(new_label == i):
                    address = labels[i]
        
            ans += decimalToBinary(address)
            return ans 

    else:
        # print(search_index(l1))
        print("line",error_index, end=": ")
    
        print(errors[10])   # hee also error correction
        exit() 

    # ans += "000"

    # new_label = l1[1]
    # address = 0
    # for i in labels.keys():
    #     if(new_label == i):
    #         address = labels[i]
    
    # ans += decimalToBinary(address)
    # return ans 

def check_variables(file):
    
    count = len(variables)

    check_count = 0
    for i in range(0, len(file)):

        if(file[i] == ''):
            continue    
        if(file[i].split()[0] == "var"):
            check_count += 1
        else:
            break
    
    if(check_count == count):
        # No error 
        pass
        
    else:
        print(i +1)
        print(errors[7])
        exit()
        # code nahi chalega
printlist =[]

def func_check(temp_list1, error_index, i):


    if(temp_list1[0] == "mov1"):
        # print(search_index(temp_list1))
        print("line",error_index, end=": ")
        print(errors[1])
        exit()
    if(temp_list1[0]== "mov"):
        try:
            dollar = temp_list1[2]
            if ('$' == dollar[0]):
                temp_list1[0] = "mov1"

        except:
            # print(search_index(temp_list1))
            print("line",error_index, end=": ")
            print(errors[10])
            exit()
    try:
        opcode = dict[temp_list1[0]][0]
        types = dict[temp_list1[0]][1]

    except:
        # print(1)
        # print(search_index(temp_list1))
        print("line",error_index, end=": ")
        # print(1)

        print(errors[1])
        exit()
    ans = opcode
    if(types == 'A'):
        ans = fun_A(temp_list1, ans, error_index)

    elif(types == 'B'):
        ans = fun_B(temp_list1, ans, error_index)
    elif(types == 'C'):
        ans = fun_C(temp_list1, ans, error_index)
    elif(types == 'D'):
        ans = fun_D(temp_list1, ans, error_index)
    elif(types == 'E'):
        ans = fun_E(temp_list1, ans, error_index)
    elif(types == 'F'):

        if(len(temp_list1) == 1):
            ans += "0"*11
            if ("hlt" == temp_list1[0] and i!=len(l3) -1):
            # lab: my lab: add R1 R2 R3


                print("line",error_index, end=": ")
                print(errors[9])
                exit()

            # print(ans)
            printlist.append(ans)
            # if ("hlt" != l3[len(l3)-1] ):
            #     print("line",error_index, end=": ")
            #     print(errors[9])
            #     exit()
            for data in printlist:
                print(data)

            
            exit()
        else:
            print("line",error_index, end=": ")
            print(errors[1])
            exit()
    # print(ans)
    printlist.append(ans)


# here would be function which will remove spaces from end




#  Here main function is starting

#************* 
def main():
    a = ""
    
    count = 0
    l1 = l3.copy()
    check_variables(l1)
    

    # l1 = ins.copy()    --------------------------------------------------marked
    # print(l3)
    # print(l1)

    for i in range(0, len(l1)):
        # changes -------------
        # temp = l1[i].split()

        # if(temp[0] == "var" or temp[0] == ''):
        #     continue
        # elif(temp[0][-1] == ':'):
        #     temp_label = temp[0]
        #     temp_ins = temp[1:]
            # check for instruction inside temp 



        
        if(l1[i] ==  ''):
            continue


        temp_list1 = l1[i].split()

        # print(temp_list1)

        
        if ("hlt" == temp_list1[0] and i!=len(l1) -1):
        # lab: my lab: add R1 R2 R3
        

            print("line", search_index(["hlt"]), end =": ")
            print(errors[9])
            exit()
        # ["mov", "R1", "$10", "654"]

        if(temp_list1[0] == "var"):
            continue
            
        if(temp_list1[0][-1] == ':'):
            for k in range(len(temp_list1)):
                if(temp_list1[k][-1] != ':'):
                    break
            vibes = temp_list1[k:]
            func_check(vibes, i + 1, i)

        else:
            func_check(temp_list1, i+1, i)
        
        
    if ("hlt" != l1[len(l1)-1] ):
        print(errors[8])
        exit()

    for data in printlist:
        print(data)

    

if (__name__ == "__main__"):
    label()
    main()
