from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("BRM")
root.geometry("1100x300")
inp=tk.StringVar()

totaldoc=50

#---------------------Dictionary of postional index, inverted index, and to map doc id------------------------
positionalIndex = {}
invertedindex = {}
docIdMap = {}

 #----------------------------------------- Pre Processing function for text---------------------------
def Pre_Processing(input_string):
    result=''
    punctuations=['.', ',','’','‘','“','(', ')', "'", "!",'©', ':','?','"',';','#','&','*','@','[',']','-','/','{','}','$','“',',','”']
    for character in input_string:
        if character == '.':
           result=result + " "
           continue
        if character in punctuations:
            continue
        else:
            result=result + character
    GottenStopWords=getStopWords()
    result=removeStopWords(result,GottenStopWords)
    result=make_word_list(result)
    return result

 #------------------------------------Removing Punctuations In Input Querry---------------------------
def Remove_Punctuations(input_string):
    result=''
    punctuations=['.', ',','’','‘','“', '(', ')', "'", "!",'©', ':','?','"',';','#','&','*','@','[',']','-','{','}','$','“',',','”']
    for character in input_string:
        if character == '.':
           result=result + " "
           continue
        if character in punctuations:
            continue
        else:
            result=result + character
    return result

 #----------------------------------------Removing Stopwords from Text------------------------------
def removeStopWords(input_string, stopWordss):
    line=input_string.split()
    result=""
    if line[0].isdigit():
        result.join(line)
    for word in line:
        if word not in stopWordss:
            result=result + (word + " ")
    return result

 #-------------------------------------Getting Stopwords from Given File------------------------------
def getStopWords():
    StopWords = open('Stopword-List.txt')
    stopWordssList = []
    for sw in StopWords:
        sw = sw.strip()
        stopWordssList.append(sw)
    return stopWordssList

 #----------------------------------------Tokeninzing the Doccument data------------------------------
def make_word_list(word_list):   
    W=[]
    w=''
    for word in word_list: 
       if((word!=' ')and(word!='.')and(word!=']')and(word!='\n')and(word!='-')and(word!='—')and(word!='?')and(word!='"')and(word!='…')and(word!='/')):
          w=w+word 
       elif((w!='') ):
            W=W+[w]  
            w=''
    if((w!='') ):
        W=W+[w]

    l=len(W)
    #---------Here stemming id done in tokens using nltk library--------
    ps=PorterStemmer() 
    for i in range(l):
        W[i]=ps.stem(W[i])
    return(W)

 #--------------------------------------Storing Postional Index in File------------------------------
def print_positional_index():
        fileobj = open("PositionalIndex.txt", 'w')
        for key, value in sorted(positionalIndex.items()):
            fileobj.write(str(key) + " --> " + str(value))
            fileobj.write("\n")
        fileobj.close()

 #--------------------------------------Storing Postional Index in File------------------------------
def print_Inverted_index(invertedindex):
    fileob = open("InvertedIndex.txt", 'w')
    for key, value in sorted(invertedindex.items()):
        fileob.write(str(key) + " --> " + str(value))
        fileob.write("\n")
    fileob.close()

#---------This function Reads from doccument call Pre_Processing and create Inverted and positional indexes---
def make_Indexes():
    docId = 1
    I_words=[]
    for i in range(totaldoc):
        f = open("ShortStories/"+str(i+1)+'.txt', 'r',encoding="utf8")
        position = 1
        docIdMap[docId] = i
        text=f.read()
        P_words=Pre_Processing(text.lower())
        I_words=P_words
        I_words = list(OrderedDict.fromkeys(I_words))
        
        for j in range(len(I_words)):
            if I_words[j] in invertedindex.keys():
                invertedindex[I_words[j]].append(i+1)
            else:
                invertedindex[I_words[j]] = []
                invertedindex[I_words[j]].append(i+1)
        
        print_Inverted_index(invertedindex)

        for word in P_words:
            if (word in positionalIndex):
                postingList = positionalIndex[word]
                if (docId in postingList):
                    postingList[docId].append(position)
                    position = position + 1
                else:
                    postingList[docId] = [position]
                    position = position + 1
            else:
                positionalIndex[word] = {docId: [position]}
                position = position + 1
        docId = docId + 1
    print_positional_index()


#----------------------------Functions to get Posting of cetain Term from dictionary-----------------------------
def postinglist(word):
    result=[]
    if (word in positionalIndex):
        postingList = positionalIndex[word]
        result = []
        for keys in postingList:
            result.append(keys)
        result.sort()
        return result
    else:
        return None

#-----------------------------Simple Querry----------------------------------------#
def simple_query(word):
    result=[]
    if (word in invertedindex):
        postingList = invertedindex[word]
        for keys in postingList:
            result.append(keys)
        result.sort()
        return result
    else:
        return None

#-----------------------------Boolean Querry----------------------------------------#
def boolean_query(term1,term2,flag):
    t1=simple_query(term1)
    t2=simple_query(term2)
    if(t1== None):
        t1=[0]
    if(t2== None):
        t2=[0]
    ans = set()
    if (flag=="and"):
        ans = set(t1).intersection(t2)
    else:
        ans=set(t1).union(t2)
    
    return ans

#-----------------------------Complex Querry----------------------------------------#
def complex_query(term1,term2,term3,flag):
    t1=simple_query(term1)
    t2=simple_query(term2)
    t3=simple_query(term3)
    if(t1== None):
        t1=[0]
    if(t2== None):
        t2=[0]
    if(t3== None):
        t3=[0]
    ans=set()
    if(flag=='2and'):
        temp=set()
        temp=set(t1).intersection(t2)
        ans=set(temp).intersection(t3)
    elif(flag=='2or'):
        temp=set()
        temp=set(t1).union(t2)
        ans=set(temp).union(t3)
    elif(flag=='or_and'):
        temp=set()
        temp=set(t2).intersection(t3)
        ans=set(temp).union(t1)
    elif(flag=='and_or'):
        temp=set()
        temp=set(t1).intersection(t2)
        ans=set(temp).union(t3)
    
    return ans

#-----------------------------Complex Negation Querry----------------------------------------#
def negation_query(term1,term2,term3,flag):
    t1=simple_query(term1)
    t2=simple_query(term2)
    t3=simple_query(term3)
    if(t1== None):
        t1=[0]
    if(t2== None):
        t2=[0]
    if(t3== None):
        t3=[0]
    uni=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
    ans=set()
    if(flag=='Nand'): # not A and B
        temp=set()
        temp = set(uni).difference(t1)
        ans=set(temp).intersection(t2)
    elif(flag=='andN'): # A and not B
        temp=set()
        temp = set(uni).difference(t2)
        ans=set(temp).intersection(t1)
    elif(flag=='NandN'): # not A and not B
        print("mushi1")
        temp1=set()
        temp2=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        ans=set(temp1).intersection(temp2)
    elif(flag=='Nor'): # not A or B
        temp1=set()
        temp1 = set(uni).difference(t1)
        ans=set(temp1).union(t2)
    elif(flag=='orN'): # A or not B
        temp1=set()
        temp1 = set(uni).difference(t2)
        ans=set(temp1).union(t1)
    elif(flag=='and_and_N'): # A and B and NOT C 3333333333333333333333
        temp1=set()
        temp2=set()
        interset=set()
        interset = set(t1).intersection(t2)
        temp2 = set(uni).difference(t3)
        ans=set(interset).intersection(temp2)
    elif(flag=='and_N_and'): # A and Not B and C
        temp2=set()
        interset=set()
        interset = set(t1).intersection(t3)
        temp2 = set(uni).difference(t2)
        ans=set(interset).intersection(temp2)
    elif(flag=='N_and_and'): # Not A and B and C
        temp1=set()
        interset=set()
        interset = set(t2).intersection(t3)
        temp1 = set(uni).difference(t1)
        ans=set(interset).intersection(temp1)
    elif(flag=='and_or_N'): # A and B or Not C  
        temp1=set()
        temp2=set()
        interset=set()
        interset = set(t1).intersection(t2)
        temp2 = set(uni).difference(t3)
        ans=set(interset).union(temp2)
    elif(flag=='N_and_or'):
        temp1=set()
        temp2=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        interset = set(temp1).intersection(t2)
        ans=set(interset).union(t3)
    elif(flag=='N_and_N_and'): # Not A and Not B and C
        temp1=set()
        temp2=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        interset = set(temp1).intersection(temp2)
        ans=set(interset).intersection(t3)
    elif(flag=='and_N_and_N'): # A and Not B and Not C
        temp2=set()
        temp3=set()
        interset=set()
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset = set(temp2).intersection(temp3)
        ans=set(interset).intersection(t1)
    elif(flag=='N_and_and_N'): # Not A and B and Not C
        temp1=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp3 = set(uni).difference(t3)
        interset = set(temp1).intersection(temp3)
        ans=set(interset).intersection(t2)
    elif(flag=='or_and_N'): # A or B and Not C
        temp1=set()
        temp3=set()
        interset=set()
        temp3 = set(uni).difference(t3)
        interset = set(temp3).intersection(t2)
        ans=set(interset).union(t1)
    elif(flag=='and_N_or'): # A and Not B or C
        temp1=set()
        temp2=set()
        interset=set()
        temp2 = set(uni).difference(t2)
        interset = set(temp2).intersection(t1)
        ans=set(interset).union(t3)
    elif(flag=='or_N_and'): # A or Not B and C
        temp1=set()
        temp2=set()
        interset=set()
        temp2 = set(uni).difference(t2)
        interset = set(t3).intersection(temp2)
        ans=set(interset).union(t1)
    elif(flag=='N_or_and'): # Not A or B and C
        temp1=set()
        temp2=set()
        interset=set()
        interset = set(t2).intersection(t3)
        temp1 = set(uni).difference(t1)
        ans=set(interset).union(temp1)
    elif(flag=='NorN'): # not A or Not B
        temp1=set()
        temp2=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        ans=set(temp1).union(temp2)
    elif(flag=='NandNandN'): # Not A and Not B and Not C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset=set(temp1).intersection(temp2)
        ans=set(interset).intersection(temp3)
    elif(flag=='or_or_N'): # A or B or Not C
        temp3=set()
        unionset=set()
        temp3 = set(uni).difference(t3)
        unionset=set(t2).union(t1)
        ans=set(unionset).union(temp3)
    elif(flag=='or_N_or'): # A or Not B or C
        temp2=set()
        unionset=set()
        temp2 = set(uni).difference(t2)
        unionset=set(t1).union(t3)
        ans=set(unionset).union(temp2)
    elif(flag=='N_or_or'): # Not A or B or C
        temp1=set()
        unionset=set()
        temp1 = set(uni).difference(t1)
        unionset=set(t2).union(t3)
        ans=set(unionset).union(temp1)
    elif(flag=='N_and_N_or'): # Not A and Not B or C
        temp1=set()
        temp2=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        interset=set(temp1).intersection(temp2)
        ans=set(interset).union(t3)
    elif(flag=='N_or_N_and'): # Not A or Not B and C
        temp1=set()
        temp2=set()
        unionset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        unionset=set(temp1).union(temp2)
        ans=set(unionset).intersection(t3)
    elif(flag=='and_N_or_N'): # A and Not B or Not C
        temp3=set()
        temp2=set()
        interset=set()
        temp3 = set(uni).difference(t3)
        temp2 = set(uni).difference(t2)
        interset=set(t1).intersection(temp2)
        ans=set(interset).union(temp3)
    elif(flag=='or_N_and_N'): # A or Not B and Not C
        temp3=set()
        temp2=set()
        interset=set()
        temp3 = set(uni).difference(t3)
        temp2 = set(uni).difference(t2)
        interset=set(temp3).intersection(temp2)
        ans=set(interset).union(t1) 
    elif(flag=='N_and_or_N'): # Not A or Not B and C
        temp1=set()
        temp2=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        interset=set(temp2).intersection(t3)
        ans=set(interset).union(temp1)
    elif(flag=='N_or_and_N'): # Not A or Not B and Not C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset=set(temp2).intersection(temp3)
        ans=set(interset).union(temp1)
    elif(flag=='NorNandN'): # Not A or Not B and Not C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset=set(temp2).intersection(temp3)
        ans=set(interset).union(temp1)
    elif(flag=='NandNorN'): # Not A and Not B or Not C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset=set(temp1).intersection(temp2)
        ans=set(interset).union(temp3)
    elif(flag=='N_or_N_or'): # Not A or Not B or C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        interset=set(temp1).union(temp2)
        ans=set(interset).union(t3)
    elif(flag=='N_or_N_or'): # Not A or B or Not C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp3 = set(uni).difference(t3)
        interset=set(temp1).union(temp3)
        ans=set(interset).union(t2)
    elif(flag=='N_or_N_or'): # A or Not B or Not C
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset=set(temp2).union(temp3)
        ans=set(interset).union(t1)
    elif(flag=='NorNorN'):
        temp1=set()
        temp2=set()
        temp3=set()
        interset=set()
        temp1 = set(uni).difference(t1)
        temp2 = set(uni).difference(t2)
        temp3 = set(uni).difference(t3)
        interset=set(temp1).union(temp2)
        ans=set(interset).union(temp3)
    else:
        ans=set() # not A
        ans=set(uni).difference(t1)
    
    return ans

#-----------------------------Proximity Querry----------------------------------------#
def proximity_query(term1,term2,difference):
    result=[]
    t1=positionalIndex.get(term1)
    t2=positionalIndex.get(term2)
    resultant=set(t1).intersection(t2)
    skip=int(difference)+0
    for i in resultant:
        t1=positionalIndex.get(term1)[i]
        t2=positionalIndex.get(term2)[i]
        ii=jj=0 
        for ii in range(len(t1)):
            for jj in range(len(t2)):
                if((abs((t1[ii]) - (t2[jj]))) == skip ):
                    result.append(i)
                elif(t2[jj] > t1[ii]):
                    break 
    # result=list(dict.fromkeys(result))
    return result

#-----------------------------Querry Handling Function----------------------------------------#
def QueryHandler(query):
    query=query+" "
    result=[]
    restrict=query
    restrict=make_word_list(query)
    if(len(restrict)>=9):
        return("Invalid or Restricted to term count 3!")
    else:

#-----------------------------Negation Querry Handler----------------------------------------#
        if("not"in query):
            GottenStopWords = getStopWords()
            word=removeStopWords(query,GottenStopWords)
            quer=make_word_list(word)
            if(len(quer)==2):
                result=negation_query(quer[1],0,0,0)
            elif(len(quer)==3):
                if(quer[0]=='not'):
                    flag='Nand' # NOT + AND
                    result=negation_query(quer[1],quer[2],0,flag)
                else:
                    flag='andN' # AND + NOT
                    result=negation_query(quer[0],quer[2],0,flag)
            elif(len(quer)==4):
                if("or" in quer):
                        if(quer[2]=='or'): # NOT
                            flag='Nor'
                            result=negation_query(quer[1],quer[3],0,flag)
                        elif(quer[1]=='or'):
                            flag='orN'
                            result=negation_query(quer[0],quer[3],0,flag)
                elif(quer[0]=='not' and quer[2]=='not'):
                        flag='NandN'
                        result=negation_query(quer[1],quer[3],0,flag)
                elif(quer[2]=='not'):
                        flag='and_and_N'
                        result=negation_query(quer[0],quer[1],quer[3],flag)
                elif(quer[1]=='not'):
                        flag='and_N_and'
                        result=negation_query(quer[0],quer[2],quer[3],flag)
                elif(quer[0]=='not'):
                        flag='N_and_and'
                        result=negation_query(quer[1],quer[2],quer[3],flag)
            elif(len(quer)==5):
                if(quer[2]=='or'):
                    flag='and_or_N'
                    result=negation_query(quer[0],quer[1],quer[4],flag)
                elif(quer[3]=='or'):
                    flag='N_and_or'
                    result=negation_query(quer[1],quer[2],quer[4],flag)
                elif(quer[0]=='not' and quer[2]=='not'):
                    flag='N_and_N_and'
                    result=negation_query(quer[1],quer[3],quer[4],flag)
                elif(quer[1]=='not' and quer[3]=='not'):
                    flag='and_N_and_N'
                    result=negation_query(quer[0],quer[1],quer[4],flag)
                elif(quer[0]=='not' and quer[3]=='not'):
                    flag='N_and_and_N'
                    result=negation_query(quer[1],quer[2],quer[4],flag)
                elif(quer[1]=='or' and quer[3]=='not'):
                    flag='or_and_N'
                    result=negation_query(quer[0],quer[2],quer[4],flag)
                elif(quer[1]=='not' and quer[3]=='or'):
                    flag='and_N_or'
                    result=negation_query(quer[0],quer[2],quer[4],flag)
                elif(quer[1]=='or' and quer[2]=='not'):
                    flag='or_N_and'
                    result=negation_query(quer[0],quer[3],quer[4],flag)
                elif(quer[0]=='not' and quer[2]=='or'):
                    flag='N_or_and'
                    result=negation_query(quer[1],quer[3],quer[4],flag)
                else:
                    flag='NorN' # not A or not B
                    result=negation_query(quer[1],quer[4],0,flag)
            elif(len(quer)==6):
                if(quer[0]=='not' and quer[2]=='not' and quer[4]=='not'):
                    flag='NandNandN'
                    result=negation_query(quer[1],quer[3],quer[5],flag)
                elif(quer[1]=='or' and quer[3]=='or' and quer[4]=='not'): 
                    flag='or_or_N'
                    result=negation_query(quer[0],quer[2],quer[5],flag)
                elif(quer[1]=='or' and quer[2]=='not' and quer[4]=='or'): 
                    flag='or_N_or'
                    result=negation_query(quer[0],quer[3],quer[5],flag)
                elif(quer[0]=='not' and quer[2]=='or' and quer[4]=='or'): 
                    flag='N_or_or'
                    result=negation_query(quer[1],quer[3],quer[5],flag)
                elif(quer[0]=='not' and quer[2]=='not' and quer[4]=='or'):  
                    flag='N_and_N_or'
                    result=negation_query(quer[1],quer[3],quer[5],flag)
                elif(quer[0]=='not' and quer[2]=='or' and quer[3]=='not'):  
                    flag='N_or_N_and'
                    result=negation_query(quer[1],quer[4],quer[5],flag)
                elif(quer[1]=='not' and quer[3]=='or' and quer[4]=='not'): 
                    flag='and_N_or_N'
                    result=negation_query(quer[0],quer[2],quer[5],flag)
                elif(quer[1]=='or' and quer[2]=='not' and quer[4]=='not'):  
                    flag='or_N_and_N' 
                    result=negation_query(quer[0],quer[2],quer[5],flag)
                elif(quer[0]=='not' and quer[3]=='or' and quer[4]=='not'):  
                    flag='N_and_or_N' 
                    result=negation_query(quer[1],quer[2],quer[5],flag)
                elif(quer[0]=='not' and quer[2]=='or' and quer[4]=='not'):  ##
                    flag='N_or_and_N'
                    result=negation_query(quer[1],quer[3],quer[5],flag)
            elif(len(quer)==7):
                if(quer[2]=='or' and quer[3]=='not' and quer[5]=='not'):
                    flag='NorNandN'
                    result=negation_query(quer[1],quer[4],quer[6],flag)
                elif(quer[0]=='not' and quer[4]=='or' and quer[5]=='not'):
                    flag='NandNorN'
                    result=negation_query(quer[1],quer[3],quer[6],flag)
                elif(quer[2]=='or' and quer[5]=='or'):
                    flag='N_or_N_or'
                    result=negation_query(quer[1],quer[4],quer[6],flag)
                elif(quer[2]=='or' and quer[4]=='or'):
                    flag='N_or_or_N'
                    result=negation_query(quer[1],quer[3],quer[6],flag)
                elif(quer[1]=='or' and quer[4]=='or'):
                    flag='or_N_or_N'
                    result=negation_query(quer[0],quer[3],quer[6],flag)                   
            elif(len(quer)==8):
                flag='NorNorN'
                result=negation_query(quer[1],quer[4],quer[7],flag)

    #-----------------------------Complex Querry Handler----------------------------------------#
        elif( ("and") or ("or") in query):
            GottenStopWords = getStopWords()
            word=removeStopWords(query,GottenStopWords)
            quer=make_word_list(word)
            if(len(quer)==3):
                if(quer[1]=='or'):
                    flag='or'
                    #--------------Boolean Querry Handler--------------------#
                    result=boolean_query(quer[0],quer[2],flag)
                else:
                    flag='2and'
                    result=complex_query(quer[0],quer[1],quer[2],flag)
            elif(len(quer)==2):
                flag='and'
                #--------------Boolean Querry Handler--------------------#
                result=boolean_query(quer[0],quer[1],flag)
            elif(len(quer)==5): # 2s or's
                flag='2or'
                #--------------Complex Querry Handler--------------------#
                result=complex_query(quer[0],quer[2],quer[4],flag)
            elif(len(quer)==4):
                if(quer[1]=='or'):
                    flag='or_and'  # or + and
                    #--------------Complex Querry Handler--------------------#
                    result=complex_query(quer[0],quer[2],quer[3],flag)
                else: 
                    flag='and_or' # and + or
                    #--------------Complex Querry Handler--------------------#
                    result=complex_query(quer[0],quer[1],quer[3],flag)
        else:
            None
        GottenStopWords = getStopWords()
        word=removeStopWords(query,GottenStopWords)
    #-----------------------------Proximity Querry Handler----------------------------------------#
        if("/" in word ):
            quer=make_word_list(word)
            result=proximity_query(quer[0],quer[1],quer[2])
        else:
            None
    #-----------------------------Simple Querry Handler----------------------------------------#  
        quer=make_word_list(word)
        if len(quer)==1:
            result=simple_query(quer[0])
        else:
            None
    
    return result

# -------------------------Initiallization Process----------------------------#
def Initiallization():
    make_Indexes()
    query=inp.get()
    query=Remove_Punctuations(query)
    Retrieved_Doccuments=QueryHandler(query.lower())
    if((Retrieved_Doccuments)==None or (Retrieved_Doccuments)=={0} or (Retrieved_Doccuments)==set()):
        labelthree=tk.Label(root,text='No Result Found!')
    else:
        length=len(Retrieved_Doccuments)
        labelfour=tk.Label(root,text=length)
        labelthree=tk.Label(root,text=Retrieved_Doccuments)
        labelfour.grid(row = 3, column = 1)
        labelfour.after(10000,lambda: labelfour.destroy())
    labelthree.grid(row = 4, column = 0)
    labelthree.after(10000,lambda: labelthree.destroy())

#----------------------------GUI INTERFACE--------------------------
def GUI():
    ttk.Label(root, text = "Boolean Retrieval Model", background = 'skyblue', foreground ="white",font = ("Times New Roman", 15)).grid(row = 0, column = 1)
    tk.Label(root, text="Please Search A Querry: ").grid(row=1,column=0)
    tk.Label(root, text="Total Retrieved Doccuments : \n DocID's").grid(row=3,column=0)

    user_input = tk.Entry(root,width=40,textvariable=inp)
    user_input.grid(row=1, column=1)

    ttk.Label(root, text = "Select the Querry :",font = ("Times New Roman", 10)).grid(column = 0,row = 2, padx = 10, pady = 25)
    
    monthchoosen = ttk.Combobox(root, width = 40, textvariable = inp)
    monthchoosen['values'] = (' beard',' passenger',' permission and possible',' power and play',' ladies and gentleman',' strange and land and play',' god and man and love',' smiling face /3',' filling room /1',' not pleaser and not fever')

    monthchoosen.grid(column = 1, row = 2)
    monthchoosen.current()

    btn = tk.Button(root, text='Execute',command=Initiallization)
    btn.grid(row=2, column=2, sticky=tk.W, pady=10)
    btn = tk.Button(root, text='Execute',command=Initiallization)
    btn.grid(row=1, column=2, sticky=tk.W, pady=10)

    root.mainloop()

if __name__ == "__main__":
    GUI()