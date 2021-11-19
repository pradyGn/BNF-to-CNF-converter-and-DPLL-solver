#!/usr/bin/env python
# coding: utf-8

# In[399]:


file_name = input("Input file name: " )
G = open(file_name,'r')
with open(file_name) as G:
    lines = G.readlines()
G.close()


# In[400]:


IN = []
i = 0

for l in lines:
    i = i + 1
    if l[0] != '#' and l[0] != '\n':
        if i < len(lines):
            IN.append(l[:len(l)-1])
        else:
            IN.append(l)


# In[401]:


def getspc(l):
    spc = []
    for j in range(len(l)):
        if l[j] == ' ':
            spc.append(j)
    return spc


# In[402]:


memmory = []

def mem(IN, memmory):
    for l in IN:
        spc = getspc(l)

        if len(spc) == 0:
            if l[0] == '!':
                memmory.append(l[1:])
            else:
                memmory.append(l)

        else:
            if l[0] == '!':
                memmory.append(l[1:spc[0]])
            else:
                memmory.append(l[:spc[0]])

            for k in range(len(spc)-1):
                if l[spc[k]+1] == '!':
                    memmory.append(l[spc[k]+2:spc[k+1]])
                else:
                    memmory.append(l[spc[k]+1:spc[k+1]])

            if l[spc[-1]+1] == '!':
                memmory.append(l[spc[-1]+2:])
            else:
                memmory.append(l[spc[-1]+1:])

    memmory.sort()

mem(IN, memmory)


# In[403]:


var_dict = {}

for var in memmory:
    if var not in var_dict:
        var_dict[var] = None


# In[404]:


orgzd_IN = []

for l in IN:
    spc = getspc(l)
    temp = []
    if len(spc) != 0:
        temp.append(l[:spc[0]])
        for s in range (len(spc)-1):
            temp.append(l[spc[s]+1:spc[s+1]])
        temp.append(l[spc[-1]+1:])
    else:
        temp.append(l)
    
    orgzd_IN.append(temp)


# In[405]:


#print(orgzd_IN)


# In[406]:


#print(var_dict)


# In[407]:


def difference(old_var_dict, new_var_dict, note):
    for var in new_var_dict:
        if new_var_dict[var] != old_var_dict[var] and new_var_dict[var] != None:
            print("easyCase: " + note[var] + " = " + str(new_var_dict[var]))
    
def differencehard(old_var_dict, new_var_dict, note):
    for var in new_var_dict:
        if new_var_dict[var] != old_var_dict[var] and new_var_dict[var] != None:
            print("hardCase: guess " + note[var] + " = " + str(new_var_dict[var]))


# In[408]:


class BFSTree:
    def __init__(self, IN, vd, p):
        self.IN = IN
        self.vd = vd
        self.left = None #for var guessed as True
        self.right = None #for variable guessed as False
        self.p = p


def asiTrue(var_dict, note):
    vd_o = copy.deepcopy(var_dict)
    for var in var_dict:
        if var_dict[var] == None:
            var_dict[var] = True
            differencehard(vd_o, var_dict, note)
            return var_dict.copy()
        
def asiFalse(var_dict, note):
    vd_o = copy.deepcopy(var_dict)
    for var in var_dict:
        if var_dict[var] == None:
            var_dict[var] = False
            differencehard(vd_o, var_dict, note)
            return var_dict.copy()
        
def failcheck(IN):
    for l in IN:
        if len(l) == 0:
            #print("True")
            return True
    #print("False")
    return False

def Print(obj):
    print(obj.IN)
    print(obj.vd)
    print("\n")


# In[409]:


def shortnames(IN):
    note = {}
    i = 65
    for l in IN:
        for ele in l:
            if ele[0] != "!":
                if ele not in note:
                    note[ele] = chr(i)
                    i += 1
            elif ele[0] == '!':
                if ele[1:] not in note:
                    note[ele[1:]] = chr(i)
                    i += 1
    
    newIN = []
    
    for l in IN:
        templ = []
        for ele in l:
            for var in note:
                ele = ele.replace(var, note[var])
            templ.append(ele)    
        newIN.append(templ)
    
    return newIN, note


# In[410]:


import copy

def Singleton(orgzd_IN, var_dict, note):
    vd_o = copy.deepcopy(var_dict)
    for l in orgzd_IN:
        if len(l) == 1 and l[0][0] == '!':
            var_dict[l[0][1:]] = False
            orgzd_IN.remove(l)
            difference(vd_o, var_dict, note)
            return orgzd_IN, var_dict
        elif len(l) == 1 and l[0][0] != '!':
            var_dict[l[0]] = True
            V = l[0]
            orgzd_IN.remove(l)
            difference(vd_o, var_dict, note)
            return orgzd_IN, var_dict
    return orgzd_IN, var_dict
        
def Singletion_sol(orgzd_IN, var_dict, obj, note):
    i = 1
    while i == 1:
        temp_list = []
        
        orgzd_IN, var_dict = Singleton(orgzd_IN, var_dict, note)

        for var in var_dict:
            if var_dict[var] == True:
                for l in orgzd_IN:
                    if var in l:
                        temp_list.append(l)
                    if '!' + var in l:
                        l.remove('!' + var)
        
        for l in temp_list:
            orgzd_IN.remove(l)
        temp_list.clear()
        
        
        for var in var_dict:
            if var_dict[var] == False:
                for l in orgzd_IN:
                    if var in l:
                        l.remove(var)
                    if '!' + var in l:
                        temp_list.append(l)

        for l in temp_list:
            orgzd_IN.remove(l)
        
        i = 0

        for l in orgzd_IN:
            if len(l) == 1:
                i = 1
    return orgzd_IN, var_dict #removed copy here


# In[ ]:





# In[ ]:





# In[411]:


def CNFtoSol(obj, note):
    if len(obj.IN) == 0:
        print("Solution Found")
        return obj
    else:
        if None in list(obj.vd.values()) and obj.left == None:
            
            var_dict = asiTrue(copy.deepcopy(obj.vd), note)
            
            orgzd_IN, var_dict = Singletion_sol(copy.deepcopy(obj.IN), copy.deepcopy(var_dict), obj, note)
            
            obj.left = BFSTree(copy.deepcopy(orgzd_IN), copy.deepcopy(var_dict), obj)
            
            del orgzd_IN
            
            del var_dict
            
            if failcheck(copy.deepcopy(obj.left.IN)):
                return CNFtoSol(obj, note)
            else:
                return CNFtoSol(obj.left, note)
        elif obj.right == None:
            
            var_dict = asiFalse(copy.deepcopy(obj.vd), note)
            
            orgzd_IN, var_dict = Singletion_sol(copy.deepcopy(obj.IN), copy.deepcopy(var_dict), obj, note)
            
            obj.right = BFSTree(copy.deepcopy(orgzd_IN), copy.deepcopy(var_dict), obj)
            
            del orgzd_IN
            
            del var_dict
            
            if failcheck(copy.deepcopy(obj.right.IN)):
                return CNFtoSol(obj, note)
            else:
                return CNFtoSol(obj.right, note)
        elif obj.p != None:
            return CNFtoSol(obj.p, note)
        elif obj.p == None:
            print("NO VALID ASSIGNMENT")


# In[412]:


orgzd_IN, note = shortnames(orgzd_IN)
#print(note)
#print(orgzd_IN)


# In[413]:


note = {value:key for key, value in note.items()}

new_var_dict = {}

for var in note:
    new_var_dict[var] = None
    
#print(new_var_dict)

var_dict = copy.deepcopy(new_var_dict)


# In[414]:


dummyobj = BFSTree(None, None, None)

print(orgzd_IN)

orgzd_IN, var_dict = Singletion_sol(orgzd_IN.copy(), var_dict.copy(), dummyobj, note)

if not failcheck(orgzd_IN):
    root = BFSTree(orgzd_IN.copy(), var_dict.copy(), None)
    result = CNFtoSol(root, note)
    #print(result.vd)
else:
    print("NO VALID ASSIGNMENT")


# In[415]:


note = {value:key for key, value in note.items()}
b00l = list(result.vd.values())
keys = list(note.keys())
OP = {}
for i in range(len(keys)):
    OP[keys[i]] = b00l[i]
    
for var in OP:
    if OP[var] == None:
        print("Assigning default value (True) to variable: " + var)
        OP[var] = True

print(OP)


# In[ ]:





# In[ ]:





# In[344]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[339]:


"""
newIN = []
for l in orgzd_IN:
    templ = []
    for ele in l:
        for var in note:
            ele = ele.replace(var, note[var])
        templ.append(ele)    
    newIN.append(templ)
    
orgzd_IN = copy.deepcopy(newIN)
"""


# In[ ]:





# In[ ]:




