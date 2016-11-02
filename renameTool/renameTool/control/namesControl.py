# coding:utf-8

import pymel.all as pm

def getAlpha(value, capital=False):
    '''
     입력 받은 정수를 알파벳으로 바꿔준다.
    0 => a  1 => b ...... 25 => z
    26 => aa 27 => ab ......
    '''
    # calculate number of characters required
    base_power = 0 # 근이 저장된다.
    base_start = 0
    base_end   = 0    
    while value >= base_end:
        base_power +=1
        base_start = base_end
        base_end += pow(26, base_power)
    base_index = value - base_start # 나머지가 저장된다.
    
    # create alpha representation
    alphas = ['a'] * base_power
    for i in range(base_power-1, -1, -1):
        alphas[i] = chr(97+ (base_index % 26))
        base_index /= 26
    
    if capital:
        return ''.join(alphas).upper()
    
    return ''.join(alphas)
        
def rename(text, prefix = None, suffix = None, padding = 0, letters = False, capital = False):
    nodes = pm.ls(sl=True)
    newNames = []
    for i, _ in enumerate(nodes):
        tempName = ''
        if prefix: tempName += prefix + text + str(i)
        if suffix: tempName += suffix

        tempName = tempName.partition(prefix+text)[2]
        if suffix:
            tempName = tempName.rpartition(suffix)[0]
        if letters: # 페딩을 문자로 사용한다
            alpha   = getAlpha(int(i), capital)
            newName = prefix+text+alpha+suffix
            newNames.append(newName)
        else:
            num = str(i+1).zfill(padding+1)
            newName = prefix+text+num+suffix
            newNames.append(newName)
        
    error_msg = 'Fail to rename one of more nodes.\n'
    failedNodes = []
    for i, node in enumerate(nodes):
        if not pm.objExists(newNames[i]):
            node.rename(newNames[i])
        else:
            error_msg += '\t {} ==> {} \n'.format(node.name(), newNames[i]) 
            failedNodes.append(node)
            
    if failedNodes:
        pm.error(error_msg)
        print failedNodes    
             
    
def findReplace(findStr, replaceStr, flag):
    '''
    nodes = None
    if flag == 'all':
        nodes = pm.ls()
    else:
        nodes = pm.ls(sl=True)
    '''
    print flag
    pm.mel.searchReplaceNames(findStr, replaceStr, flag)
            
                

