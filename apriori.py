'''
Created on 2017年11月10日

@author: Administrator
'''

data = [] 
freq_map = {}  #频数统计
SUPPORT_MIN = 0.05
ITEM_MAX = 0   #总条目数


#读取data.txt并转化成数字 并找到最大的数值
def read_datafile():
    global ITEM_MAX
    
    with open('data.txt', 'r') as file: 
        raw_data = file.readlines()  #raw_data为list类型,每个元素是字符串类型
        for raw_line in raw_data:
            line = []
            for nstr in raw_line.split(): #split默认以空格划分
                try:
                    int(nstr)  #数据过滤
                    line.append(nstr)
                    if (nstr in freq_map): #统计出现次数
                        freq_map[nstr] = freq_map[nstr]+1
                    else:
                        freq_map[nstr]=1
                except (ValueError, TypeError):
                    pass
            if (len(line) > 0):
                data.append(line)
        ITEM_MAX = len(data)
        #print(data) 
        #print(freq_map)
        print(ITEM_MAX)
        
#找出频繁一项集
def findObjList1():
    obj1 = []
    
    for item in freq_map:
        if (freq_map[item]/ITEM_MAX >= SUPPORT_MIN):
            obj1.append([item])
    return obj1

#连接两个k项
#['1', '2', '3'] ['1', '2', '4']->['1', '2', '3', '4']
def Connect(lineX, lineY):
    length = len(lineX)
    new_list = list()
    not_equal = 0
    for i in range(length):
        if (lineX[i] != lineY[i]):
            if (lineX[i] > lineY[i]):
                new_list += [lineY[i], lineX[i]]
            else:
                new_list += [lineX[i], lineY[i]]
                
            not_equal += 1
            if (not_equal > 1):
                return []
        else:
            new_list.append(lineX[i])
    
    new_list.sort()
    return new_list

#所有子集是否都满足频繁的
def isAllSubObjSupported(items, objk):
    for i in range(0,len(items)):
        if ((items[0:i]+items[i+1:]) not in objk):
            return False
    return True


#是否满足支持度
def isSupported(items, database, gate=0):
    support = 0
    for line in database:
        included = True
        for each_item in items:
            if ((each_item in line) == False):
                included = False
                break
        if (included):
            support += 1
    
    return (support/len(database) >= gate)

#由频繁k项集得出频繁k+1项集
# 参数:k项集
def findByObjk(objk):
    length = len(objk)
    obj_new = list()
    for i in range(length):
        for j in range(i+1, length):
            tmp = Connect(objk[i], objk[j])
            if (tmp and tmp not in obj_new):
                if ((isAllSubObjSupported(tmp, objk)) and (isSupported(tmp, data, SUPPORT_MIN))):
                    obj_new.append(tmp)
    return obj_new
        
#找出频繁集
def findAll():
    obj = []
    i = 0
    obj.append(findObjList1())
    while True:
        tmp = findByObjk(obj[i])
        if (tmp):
            obj.append(tmp)
            i += 1
        else:
            break
    return obj
            
#保存至文件
def SaveObj(obj):
    i = 1
    for eachline in obj:
        with open('obj'+str(i)+'.txt', 'w+') as file: 
            for eachitem in eachline:
                file.write(str(eachitem)+'\n')
        i += 1
   
read_datafile()   
ObjList = findAll()
SaveObj(ObjList)

  


