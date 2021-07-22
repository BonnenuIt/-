import pypinyin
import pdfplumber
import numpy as np
import matplotlib.pyplot as plt

file_path = './共产党宣言.pdf'
words = ''
English_words = ''
with pdfplumber.open(file_path) as pdf:
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        txt = page.extract_text()
        words = words + txt
    pin_list = pypinyin.lazy_pinyin(words, errors='ignore')
    English_words = ''
    for i in pin_list:
        English_words += ''.join(i)
    # print(English_words)

def char_num(string):
    dic_char ={}
    for c in string:
        if not c in dic_char:
            dic_char[c] = 1
        else:
            dic_char[c] += 1
    return sorted(dic_char.items(),key=lambda x:x[0]) # Sorted by value, from low to high

def freq_calc(dic_str):
    word_list = [] 
    word_num = []
    num = 0
    for (key,value) in dic_str:
        word_list.append(key)
        word_num.append(value)
    summation = sum(word_num)
    print('26个字母 = ', word_list)
    print('对应频次 = ', word_num)
    print("编码长度 = ", summation)

    word_freq = [[]]
    for i in range(len(word_num)):
        word_freq[0].append(round(word_num[i]/summation, 3))
    print("频率方差 = ", np.var(word_freq))
    return (word_list, word_freq)

dic_string=char_num(English_words)
(word_list, word_freq) = freq_calc(dic_string)
freq_show = np.array(word_freq)

fig, ax = plt.subplots(figsize = (18, 6))
image1 = ax.imshow(freq_show)

ax.set_xticks(np.arange(26))
ax.set_yticks(np.arange(1))
ax.set_xticklabels(word_list)
ax.set_yticklabels(['Frequency'])

for i in range(1):
    for j in range(26):
        text = ax.text(j, i, freq_show[i, j],
                       ha="center", va="center", color="w")
ax.set_title("Frequency of PINYIN")
fig.tight_layout()
plt.colorbar(image1)
plt.show()

############################ 新方案 ############################

elements_count = {}
for element in pin_list:
    if element in elements_count:
        elements_count[element] += 1
    else:
        elements_count[element] = 1

class treenode:
    def __init__(self,key,freq):
        self.key = key
        self.freq = freq
        self.child01 = None
        self.child02 = None
        self.child03 = None
        self.child04 = None
        self.child05 = None
        self.child06 = None
        self.child07 = None
        self.child08 = None
        self.child09 = None
        self.child10 = None
        self.child11 = None
        self.child12 = None
        self.child13 = None
        self.child14 = None
        self.child15 = None
        self.child16 = None
        self.child17 = None
        self.child18 = None
        self.child19 = None
        self.child20 = None
        self.child21 = None
        self.child22 = None
        self.child23 = None
        self.child24 = None
        self.child25 = None
        self.child26 = None
        self.childnodes = [self.child01, self.child02, self.child03, self.child04, self.child05, self.child06, self.child07,
                           self.child08, self.child09, self.child10, self.child11, self.child12, self.child13, self.child14,
                           self.child15, self.child16, self.child17, self.child18, self.child19, self.child20, self.child21,
                           self.child22, self.child23, self.child24, self.child25, self.child26]
        self.code = ''

def create_noteQ(elements_count):
    Q=[]
    for i in elements_count.keys():
        Q.append(treenode(i,elements_count[i]))        
    Q.sort(key=lambda item:item.freq,reverse = True)# 降序排列
    return Q 
#添加节点
def addQ(Q, nodeNew):
    if len(Q) == 0:
        return [nodeNew]
    else:
        Q=Q+[nodeNew]
        Q.sort(key=lambda item:item.freq,reverse=True)
    return Q
      
class Node_tree:
    def __init__(self,elements_count):
        self.que = create_noteQ(elements_count)
        self.size = len(self.que)
        
    def addnode(self,node):
        self.que = addQ(self.que, node)
        self.size += 1
       
    def popNode(self):
        self.size -= 1
        return self.que.pop()

#创建huffman树
def Huff_Tree(nodeQ,exact_division):
    if exact_division == False:
        r = treenode(None, 0)
        divi = (len(elements_count.keys()) % 25) 
        # print('divi = ', divi)
        for i in range(divi):
            node1 = nodeQ.popNode()
            r.freq = r.freq + node1.freq
            r.childnodes[i] = node1
        nodeQ.addnode(r)

    while nodeQ.size != 1:
        r = treenode(None, 0)
        for i in range(26):
            node1 = nodeQ.popNode()
            r.freq = r.freq + node1.freq 
            r.childnodes[26 - i - 1] = node1
        nodeQ.addnode(r)

    return nodeQ.popNode()
  # 返回根节点

encoding = {}# 编码
decoding = {}# 解码
# 编码
def huffman_encode(roof, x):
    global codeDic, codeList
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if roof:
        huffman_encode(roof.childnodes[0], x + alphabet[0])
        roof.code += x
        if roof.key:
            decoding[roof.code] = roof.key
            encoding[roof.key] = roof.code
        for i in range(25):
            huffman_encode(roof.childnodes[i + 1], x + alphabet[i + 1])

# 编码
def H_encode(en_code):
    global encoding
    transcode = ""
    for i in en_code:
        transcode += encoding[i]
    return transcode
# 解码
def H_decode(code_str):
    global decoding
    code = ""
    res = ""
    for w in code_str:
        code += w
        if code in decoding:
            res += decoding[code]
            code = ""
    return res

if ((len(elements_count.keys())% 25)) == 0:   # (len(elements_count.keys())-26) % 25
    exact_division = True 
else:
    exact_division = False
    # print('len(elements_count.keys()) = ' ,len(elements_count.keys()))
t = Node_tree(elements_count)
tree = Huff_Tree(t,exact_division)
huffman_encode(tree, '')

print('\n\n新编码方案 : \n', encoding)

re_encode = H_encode(pin_list)
dic_new = char_num(re_encode)
(word_list_1, word_freq_1) = freq_calc(dic_new)
freq_show = np.array(word_freq_1)
# 创建画布
fig, ax = plt.subplots(figsize = (18, 6))
image2 = ax.imshow(freq_show)
# 修改标签
ax.set_xticks(np.arange(26))
ax.set_yticks(np.arange(1))
ax.set_xticklabels(word_list_1)
ax.set_yticklabels(['Frequency'])

for i in range(1):
    for j in range(26):
        text = ax.text(j, i, freq_show[i, j],
                       ha="center", va="center", color="w")
ax.set_title("Frequency of PINYIN")
fig.tight_layout()
plt.colorbar(image2)
plt.show()
