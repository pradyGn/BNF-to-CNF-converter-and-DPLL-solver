#!/usr/bin/env python
# coding: utf-8

# In[259]:


import copy


# In[260]:


file_name = input("Input file name: " )
G = open(file_name,'r')
with open(file_name) as G:
    lines = G.readlines()
G.close()


# In[261]:


IN = []
i = 0

for l in lines:
    i = i + 1
    if l[0] != '#' and l[0] != '\n':
        if i < len(lines):
            IN.append(l[:len(l)-1])
        else:
            IN.append(l)


# In[262]:


def getspc(l):
    spc = []
    for j in range(len(l)):
        if l[j] == ' ':
            spc.append(j)
    return spc


# In[263]:


def priorities(l):
    opn_bracpos = []
    cls_bracpos = []
    pair = []
    p = []
    
    for pos in range(len(l)):
        if l[pos] == "(":
            opn_bracpos.append(pos)
    
    for pos in range(len(l)):
        if l[pos] == ")":
            cls_bracpos.append(pos)
    
    if len(opn_bracpos) != len(cls_bracpos):
        print("Improper Pranthesis")
        return
    
    while len(cls_bracpos) > 0:
        for i in range(len(cls_bracpos)):
            OB = opn_bracpos[-1]
            if cls_bracpos[i] > OB:
                pair.append([OB, cls_bracpos[i]])
                opn_bracpos.remove(OB)
                cls_bracpos.remove(cls_bracpos[i])
                break
    
    para = []
    
    for pr in pair:
        for j in range(pr[0], pr[1]+1):
            para.append(j)
    
    
    return pair, para


# In[264]:


def ifnoif(IN): #remove all if and only if
    for l in IN:
        spc = getspc(l)
        pair, para = priorities(l)
        for pos in range(len(spc)-1):
            if l[spc[pos]+1:spc[pos+1]] == "<=>" and spc[pos]+1 not in para:
                l1 = l[:spc[pos]]
                l2 = l[spc[pos+1]+1:]
                spc1 = getspc(l1)
                spc2 = getspc(l2)
                if len(spc1) > 0:
                    l1 = "(" + l1 + ")"
                if len(spc2) > 0:
                    l2 = "(" + l2 + ")"
                IN.append(l1 + " => " + l2)
                IN.append(l2 + " => " + l1)
                IN.remove(l)
                ifnoif(IN)
                return IN


# In[265]:


def og(IN):
    j = 0
    for l in IN:
        pair, para = priorities(l)
        if len(pair) > 0:
            for pr in pair:
                p = [l[pr[0]+1:pr[1]]]
                ifnoif(p)
                if p != [l[pr[0]+1:pr[1]]]:
                    temp = ''
                    for s in p:
                        if len(s) > 2:
                            s = "(" + s + ")"
                        if len(temp) == 0:
                            temp = temp + s
                        else:
                            temp = temp + ' & ' + s
                    newl = l[:pr[0]+1] + temp + l[pr[1]:]
                    IN.remove(l)
                    IN.append(newl)
                    j = 1
                    return IN, j
    return IN, j


# In[266]:


def tp(IN):
    i = 0
    for l in IN:
        pair, para = priorities(l)
        if len(pair) > 0:
            for pr in pair:
                p = [l[pr[0]+1:pr[1]]]
                implies(p)
                if p[0] != l[pr[0]+1:pr[1]]:
                    newl = l[:pr[0]+1] + p[0] + l[pr[1]:]
                    IN.remove(l)
                    IN.append(newl)
                    i = 1
                    return IN, i
    return IN, i


# In[267]:


def implies(IN):
    for l in IN:
        spc = getspc(l)
        pair, para = priorities(l)
        for pos in range(len(spc)-1):
            if l[spc[pos]+1:spc[pos+1]] == "=>" and spc[pos]+1 not in para:
                spc1 = getspc(l[:spc[pos]])
                spc2 = getspc(l[spc[pos+1]+1:])
                if len(spc1) > 0:
                    l1 = "!(" + l[:spc[pos]] + ")"
                else:
                    l1 = "!" + l[:spc[pos]]
                if len(spc2) > 0:
                    l2 = "(" + l[spc[pos+1]+1:] + ")"
                else:
                    l2 = l[spc[pos+1]+1:]
                IN.append(l1 + " | " + l2)
                IN.remove(l)
                implies(IN)
                return IN


# In[268]:


def endpriority(l, pos):
    pair, para = priorities(l)
    for pr in pair:
        if pr[0] == pos:
            return pr


# In[269]:


def addnt(ntskips_pos, l):
    for i in range(1, len(ntskips_pos)):
        ntskips_pos[i] = ntskips_pos[i] - 1
    
    adds = []
    for j in range(1, len(ntskips_pos)-1):
        adds.append(j)
        
    for k in range(2, len(ntskips_pos)):
        ntskips_pos[k] = ntskips_pos[k] + adds[k-2]
        
    l = l[:ntskips_pos[0]] + l[ntskips_pos[0]+1:]
    ntskips_pos.remove(ntskips_pos[0])
    
    for m in range(len(ntskips_pos)):
        l = l[:ntskips_pos[m]] + "!" + l[ntskips_pos[m]:]
    
    return l


# In[270]:


def andor(brac):
    for i in range(len(brac)):
        if brac[i] == '&':
            brac = brac[:i] + "|" + brac[i+1:]
        elif brac[i] == "|":
            brac = brac[:i] + "&" + brac[i+1:]
            
    return brac


# In[271]:


def nots(IN, skips):
    k = 0
    for l in IN:
        for pos in range(len(l)-1):
            if l[pos] == '!' and l[pos+1] == "(":
                ntskips_pos = [pos]
                cur_pair = endpriority(l, pos+1)
                for i in range(cur_pair[0]+1, cur_pair[1]):
                    if l[i] not in skips:
                        ntskips_pos.append(i)
                temp = addnt(ntskips_pos, l)
                cur_pair = endpriority(temp, pos)
                temp1 = andor(temp[pos:cur_pair[1]+1])
                temp = temp[:cur_pair[0]] + temp1 + temp[cur_pair[1]+1:]
                IN.remove(l)
                IN.append(temp)
                k = 1
                return IN, k
    return IN, k


# In[272]:


def doublenots(IN, zz):
    zz = 0
    for l in IN:
        for pos in range(len(l)):
            check = 1
            num = 0
            i = 0
            while check != 0 and (pos+i) < len(l):
                check = 0
                if l[pos + i] == "!":
                    num = num + 1
                    check = 1
                    i = i + 1
            if num > 1:
                zz = 1
                num1 = num%2
                if num1 == 0:
                    newl = l[:pos] + l[pos+num:]
                elif num1 == 1:
                    newl = l[:pos] + "!" + l[pos+num:]
                IN.remove(l)
                IN.append(newl)
                return IN, zz
                
    return IN, zz


# In[273]:


def unibrac (l):
    level1brac = []
    final = []
    i = 0
    for pos in range(len(l)):
        if l[pos] == "(":
            i = i + 1
            if i == 1:
                level1brac.append(pos)
        elif l[pos] == ")":
            i = i - 1
            if i == 0:
                level1brac.append(pos)
    if len(level1brac)%2 != 0:
        return "Improper paranthesis"
    
    for pos in range(int(len(level1brac)/2)):
        temp = [level1brac[2*pos], level1brac[(2*pos)+1]]
        final.append(temp)
    return final


# In[274]:


def l2anddeep(l):
    pair, para = priorities(l)
    uni = unibrac(l)
    for u in uni:
        pair.remove(u)
    skip = []
    for pr in pair:
        for pos in range(pr[0], pr[1]+1):
            skip.append(pos)
    return skip, pair


# In[275]:


def check(l):
    ands = []
    for pos in range(len(l)):
        if l[pos] == "&":
            ands.append(pos)
        elif l[pos] == "|" and len(ands) > 0:
            break
    if len(ands) > 0:
        spc0 = getspc(l[:ands[0]])
        spc1 = getspc(l[ands[-1]+1:])
        if len(spc0) > 1:
            pos0 = spc0[-2] + 1
        else:
            pos0 = 0
        if len(spc1) > 1:
            pos1 = ands[-1] + spc1[1]
        else:
            pos1 = len(l)-1
        return [pos0, pos1]
    else:
        return None


# In[276]:


def brl2(IN, memmory, i):
    for l in IN:
        allpos, l2 = l2anddeep(l)
        if len(l2) > 0:
            for br in l2:
                memmory.append(l[br[0]:br[1]+1])
                newl = l[:br[0]] + str(i) + l[br[1]+1:]
                IN.append(newl)
                IN.remove(l)
                i += 1
                brl2(IN, memmory, i)
                return IN, memmory
                
    return IN, memmory


# In[277]:


def removebrac(l):
    rm = ["(", ")"]
    for pos in range(len(l)):
        if l[pos] in rm:
            l = l[:pos] + l[pos+1:]
            l = removebrac(l)
            return l
    return l


# In[278]:


def removebracpos(l, pos):
    if l[pos[0]] == "(":
        l = l[:pos[0]] + l[pos[0]+1:]
        pos[1] = pos[1] - 1
    if l[pos[1]] == ")":
        l = l[:pos[1]] + l[pos[1]+1:]
        pos[1] = pos[1] - 1
    return l, pos


# In[279]:


def rpfrmmem(l, memmory):
    for pos in range(len(l)):
        if l[pos].isdigit():
            temp = memmory[int(l[pos])]
            l = l[:pos] + temp + l[pos+1:]
            l = rpfrmmem(l, memmory)
            return l
    return l


# In[280]:


def setLRObj(l, cor, obj, memmory):
    spc0 = getspc(l[cor[0]:])
    spc1 = getspc(l[:cor[1]])
    if cor[1] == len(l)-1:
        temp_left = l[:cor[0]+spc0[0]]
        temp_right = l[:cor[0]] + l[spc1[-1]+1:]
    elif cor[0] == 0:
        temp_left = l[:spc0[0]] + l[cor[1]+1:]
        temp_right = l[spc1[-1]+1:]
    elif cor[1] == len(l)-1 and cor[0] == 0:
        temp_left = l[:spc0[0]]
        temp_right = l[spc1[-1]+1:]
    else:
        temp_left = l[:cor[0]+spc0[0]] + l[cor[1]+1:]
        temp_right = l[:cor[0]] + l[spc1[-1]+1:]
    
    temp_left = rpfrmmem(temp_left, memmory)
    temp_right = rpfrmmem(temp_right, memmory)
    
    return temp_left, temp_right


# In[281]:


def build(l, memmory, obj):
    cor = check(l) #seems fine for all milti-alpha variables
    if cor == None:
        l = removebrac(l)
        newl = rpfrmmem(l, memmory)
        if newl != l:
            l = newl
            build(l, memmory, obj)
        else:
            obj.l = l #changed from l to None
            obj.right = None
            obj.operator = None
    else:
        l, cor = removebracpos(l, cor)
        temp_left, temp_right = setLRObj(l, cor, obj, memmory)
        obj.left = logicalstatement(temp_left)
        obj.right = logicalstatement(temp_right)


# In[282]:


def inorder(node, sol):
    if node:
        inorder(node.left, sol)
        if (not node.left):
            sol.append(node.l)
            #print(node.l)
        inorder(node.right, sol)


# In[283]:


def recall(l, memmory, obj):
    build(l, memmory, obj)
    if obj.left == None or obj.right == None:
        return
    recall(obj.left.l, memmory, obj.left)
    recall(obj.right.l, memmory, obj.right)


# In[284]:


def nottog(IN, z):
    z = 0
    for l in IN:
        for pos in range(len(l)-1):
            if l[pos] == "!" and l[pos+1] == " ":
                newl = l[:pos+1] + l[pos+2:]
                IN.remove(l)
                IN.append(newl)
                z = 1
                return IN, z
    return IN, z


# In[285]:


def shortnames(IN, note):
    skips = ["<=>", "=>", "&", "|", "(", ")", "!"]
    i = 65
    for l in IN:
        spc = getspc(l)
        if l[0] != "!":
            if l[:spc[0]] not in skips and l[:spc[0]] not in note:
                note[l[:spc[0]]] = chr(i)
                i += 1
        elif l[0] == "!":
            if l[:spc[0]] not in skips and l[:spc[0]] not in note:
                note[l[1:spc[0]]] = chr(i)
                i += 1
        for s in range(len(spc)-1):
            if l[spc[s]+1] != "!":
                if l[spc[s]+1:spc[s+1]] not in skips and l[spc[s]+1:spc[s+1]] not in note:
                    note[l[spc[s]+1:spc[s+1]]] = chr(i)
                    i += 1
            elif l[spc[s]+1] == "!":
                if l[spc[s]+2:spc[s+1]] not in skips and l[spc[s]+2:spc[s+1]] not in note:
                    note[l[spc[s]+2:spc[s+1]]] = chr(i)
                    i += 1
        if l[spc[-1]+1] != "!":
            if l[spc[-1]+1:] not in skips and l[spc[-1]+1:] not in note:
                note[l[spc[-1]+1:]] = chr(i)
                i += 1
        elif l[spc[-1]+1] == "!":
            if l[spc[-1]+2:] not in skips and l[spc[-1]+2:] not in note:
                note[l[spc[-1]+2:]] = chr(i)
                i += 1

    newIN = []
    for l in IN:
        for var in note:
            if var in l:
                l = l.replace(var, note[var])
        newIN.append(l)

    IN = copy.deepcopy(newIN)
    
    return IN, note


# In[286]:


def groupands(l):
    spc = getspc(l)
    ls = []
    if len(spc) > 2:
        for s in range(len(spc)):
            if l[spc[s]+1] == "&":
                i = 2
                num = 1
                if s+i < len(spc):
                    if (spc[s+i]+1) < len(l):
                        while l[spc[s+i]+1] == "&":
                            if s+i+2 < len(spc):
                                if spc[s+i+2]+1 < len(l):
                                    i = i + 2
                                else:
                                    i = i + 1
                            else:
                                i = i + 1
                            num = num + 1
                        if i%2 != 0:
                            i = i + 1
                if num > 0:
                    if s == 0:
                        ls.append("(" + l[:spc[s+i]] + ")")
                    elif s+i-1 == len(spc)-1:
                        ls.append("(" + l[spc[s-1]+1:] + ")")
                    else:
                        ls.append("(" + l[spc[s-1]+1:spc[s+i]] + ")")
        for ele in ls:
            pos = l.find(ele[1:-1])
            l = l[:pos] + ele + l[pos+len(ele)-2:]

        return l
    return l


# In[287]:


def rmdirt(IN):
    y = 0
    for l in IN:
        pair, para = priorities(l)
        for pr in pair:
            for pr1 in pair:
                if pr[0] == (pr1[0]+1) and pr[1] == (pr1[1]-1):
                    newl = l[:pr[0]] + l[pr[0]+1:pr[1]] + l[pr[1]+1:]
                    IN.remove(l)
                    IN.append(newl)
                    y = 1
                    return IN, y
    return IN, y


# In[288]:


class logicalstatement:
    def __init__(self, l):
        self.l = l
        self.left = None
        self.right = None
    
    def retvalues(self):
        return self.left, self.right, self.l


# In[289]:


#print(IN)


# In[ ]:





# In[290]:


#removes space between ! and a variable if any
z = 1
while z != 0:
    z = 0
    nottog(IN, z)

#print(IN)


# In[291]:


#assigns temp sortnames to long char variables
note = {}
IN, note = shortnames(IN, note)
#print(IN)
#print(note)


# In[292]:


#groups all ands togerther
import copy
newIN = []
for l in IN:
    newl = groupands(l)
    newIN.append(newl)

IN = copy.deepcopy(newIN)


# In[293]:


#print(IN)


# In[294]:


#simplifies if and only if operator from lvl 1 brackets
ifnoif(IN)


# In[250]:


#simplifies if and only if operator from higher lvl brackets
j = 1
while j != 0:
    j = 0
    IN, j = og(IN)
            
#print(IN)


# In[251]:


#simplifies implies operator from lvl 1 brackets
implies(IN)


# In[252]:


#simplifies implies operator from higher lvl brackets
i = 1
while i != 0:
    i = 0
    IN, i = tp(IN)

#print(IN)


# In[253]:


#gets all the ! inside the brackets
skips = ["|", "&", " ", "(", ")", "!"]
#print(IN)

k = 1
while k != 0:
    k = 0
    IN, k = nots(IN, skips)


# In[254]:


#simplifyes double, triple, ... nots
zz = 1
while zz != 0:
    zz = 0
    IN, zz = doublenots(IN, zz)


# In[255]:


#removes unnecessary brackets
y = 1
while y != 0:
    y = 0
    IN, y = rmdirt(IN)


# In[256]:


#shorterns all deep brackets and keeps it in memmory
memmory = []
i = 0
IN, memmory = brl2(IN, memmory, i)
#print(IN)
#print(memmory)


# In[257]:


#returns the CNF form of the given DNF equation
ls = []
sol = []

for l in range(len(IN)):
    ls.append(str(l))
    ls[l] = logicalstatement(IN[l])
    recall(ls[l].l, memmory, ls[l])
    inorder(ls[l], sol)


# In[258]:


#reassigns the original names of the variables
note = {value:key for key, value in note.items()}
fsol = []
for l in sol:
    for var in note:
        if var in l:
            l = l.replace(var, note[var])
    fsol.append(l)

for ele in fsol:
    print(ele)


# In[ ]:





# In[ ]:




