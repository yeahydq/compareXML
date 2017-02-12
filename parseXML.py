#coding:utf-8
#!/usr/bin/env python
# __author__= 'dick'

from xml.dom import minidom
import sys
import copy
def iterate_children(parent):
    child = parent.firstChild
    while child != None:
        if child.localName <> None:
            yield child
        child = child.nextSibling

def parseXML(xmlName='/dev/null'):
    xmlFile=minidom.parse(xmlName)
    xmlTree=xmlFile.documentElement

    jobList={}

    for job in xmlTree.getElementsByTagName('JOB'):
        # if job.hasAttribute('JOBNAME'):
        jobName=job.getAttribute('JOBNAME')
        jobList[jobName]=dict(job.attributes.items())
        childDict={}
        for child in iterate_children(job):
            childDict.setdefault(child.localName,[])
            childDict[child.localName].append(dict(child.attributes.items()))
        childDict[child.localName] = sorted(childDict[child.localName], key=lambda k: k['NAME'])

        jobList[jobName].update(dict(childDict))
    return jobList

def replaceVer(jobList={},mapps={}):
    newList=copy.deepcopy(jobList)
    for job in newList:
        for key in mapps:
            if newList[job][key]==mapps[key][1]:
                newList[job][key]=mapps[key][0]
    return newList

def replaceDict(newList={},mapps={}):
    # newList=copy.deepcopy(jobList)
    for job in newList:
        for key in mapps:
            if newList[job][key]==mapps[key][1]:
                newList[job][key]=mapps[key][0]
    return newList

def replaceVerAll(jobList=[],mapps={}):
    newList=copy.deepcopy(jobList)
    for i in range(len(newList)):
        if isinstance(newList[i],list):
            newList=replaceVer(newList,mapps)
        elif isinstance(newList[i])==dict:
            for job in newList:
                for key in mapps:
                    if isinstance(newList[job][key][1])==dict:
                        replaceVer(newList[job][key][1],mapps)
                        pass
                    if newList[job][key]==mapps[key][1]:
                        newList[job][key]=mapps[key][0]
    return newList

def cmpdicts(dct0, dct1):
    diffs = {}
    keys = set(dct0.keys() + dct1.keys())
    for k in keys:
            if cmp(dct0.get(k), dct1.get(k)):
                diffs[k]=(dct0.get(k),dct1.get(k))
    return diffs

def cmpDeepDict(dct0, dct1):
    diffs = {}
    keys = set(dct0.keys() + dct1.keys())
    for k in keys:
            if dct0.get(k)!=dct1.get(k):
                if dct1.get(k) == None:
                    diffs[k] = ("DICT Left Insert:",dct0.get('JOBNAME'),k, dct0.get(k))
                elif dct0.get(k) == None:
                    diffs[k] = ("DICT Right Insert:",dct1.get('JOBNAME'),k, dct1.get(k))
                elif isinstance(dct0.get(k),list):
                    diffs[k] = cmpDeepLists(dct0.get(k),dct1.get(k))
                elif type(dct0.get(k)) == dict and type(dct1.get(k)) == dict:
                    diffs[k] = cmpDeepDict(dct0.get(k), dct1.get(k))
                else:
                    diffs[k]=("DICT Update:",dct1.get('JOBNAME'),k,dct0.get(k),dct1.get(k))

            # if cmp(dct0.get(k), dct1.get(k)):
            #     diffs[k]=(dct0.get(k),dct1.get(k))
    return diffs

def getFrmList(l=[],i=0):
    if i >= len(l):
        return None
    else:
        return l[min(i,len(l)-1)]

def cmpLists(listA, listB):
    diffs = []
    #
    sortA=sorted(listA)
    sortB=sorted(listB)
    print sortA,sortB
    iA=0
    iB=0
    for i in range(max(len(sortA),len(sortB)))*2:
        if getFrmList(sortA,iA) == getFrmList(sortB,iB):
            iA+=1
            iB+=1
        elif getFrmList(sortA,iA) != getFrmList(sortB,iB):
            if getFrmList(sortA,iA + 1) == getFrmList(sortB,iB):
                diffs.append(("Left Insert", sortA[iA]))
                iA += 1
            elif getFrmList(sortA,iA) == getFrmList(sortB,iB+1):
                diffs.append(("Right Insert", getFrmList(sortB,iB)))
                iB += 1
            else :
                # diffs.append(("Update", (getFrmList(sortA, iA),getFrmList(sortB, iB))))
                diffs.append(("Left Insert", sortA[iA]))
                diffs.append(("Right Insert", sortB[iB]))
                iA += 1
                iB += 1
    # print list(set(listA).difference(set(listB)))
    return diffs


def cmpDeepLists(listA, listB):
    diffs = []
    #
    sortA=sorted(listA)
    sortB=sorted(listB)
    # print sortA,sortB
    iA=0
    iB=0
    cnt=len(sortA)+len(sortB)
    for i in range(cnt):
        curA=getFrmList(sortA, iA)
        curB=getFrmList(sortB, iB)
        nxtA=getFrmList(sortA, iA+1)
        nxtB=getFrmList(sortB, iB+1)

        if curA==None and curB==None:
            break

        curTypA=type(curA)
        curTypB=type(curB)
        nxtTypA=type(nxtA)
        nxtTypB=type(nxtB)

        if curA == curB:
            iA+=1
            iB+=1
        elif nxtA == curB:
                diffs.append(("Left Insert", curA))
                iA += 1
        elif curA == nxtB:
            diffs.append(("Right Insert", curB))
            iB += 1
        elif curTypA==dict and curTypB==dict and curA.get('NAME') == curB.get('NAME'):
            diffDict=cmpDeepDict(curA,curB)
            diffs.append(diffDict)
            iA+=1
            iB+=1
            # diffs.append(("Update", (getFrmList(sortA, iA),getFrmList(sortB, iB))))
        elif curTypA == list and curTypB == list:
            diffs.append(cmpDeepLists(curA,curB))
            iA+=1
            iB+=1
        else:
            if curTypA != dict and nxtTypA==dict:
                diffs.append(("Left Insert", curA))
                iA += 1
            if curTypB != dict and nxtTypB==dict:
                diffs.append(("Right Insert", curB))
                iB += 1
        # if nxtA==None and nxtB==None:
        #     break
    # print list(set(listA).difference(set(listB)))
    return diffs


a=[0,1,{"NAME":4,'VAR1':1},{"NAME":4,'VAR2':1},4]
b=[3,{"NAME":4,'VAR1':2},4,1,5]
# print cmpDeepLists(a,b)
# sys.exit(0)

mapping={
    "NODE_ID":('PRD.SERVER','UAT.SERVER'),
    "USER_ID": ('PRD.ID', 'UAT.ID'),
}

def compareXML(jobList_A,jobList_B):
    diff_Jobs= cmpdicts(jobList_A,jobList_B)
    # print diff_Jobs
    for job in diff_Jobs:
        if job not in jobList_A:
            print ('%s not in LEFT XML')%job
            continue
        if job not in jobList_B:
            print ('%s not in RIGHT XML')%job
            continue
        print ('%s%s')%(job,str(cmpdicts(jobList_A[job],jobList_B[job])))


def parseXML_New(xmlName='/dev/null'):
    xmlFile=minidom.parse(xmlName)
    xmlTree=xmlFile.documentElement
    return loopXML(xmlTree)

def loopXML(tree=None,cnt=0):
    currLvl=[[{tree.nodeName:dict(tree.attributes.items())}]]
    print '---'*cnt, "NodeName:",tree.nodeName,"Value:",dict(tree.attributes.items())
    addnAttr=[]
    for childTree in iterate_children(tree):
        childLvl=loopXML(childTree,cnt+1)
        if childLvl <> None:
            addnAttr.append(childLvl)
    if len(addnAttr)>0:
        try:
            addnAttrSorted=sorted(addnAttr,key=lambda x: x[0][0].items()[0][1].get("NAME"))
        except Exception,e:
            print('Eannot sort  : %s' %addnAttr)
            print('Error : %s' %e)
            pass
        else:
            addnAttr=addnAttrSorted
        currLvl.extend(addnAttr)
    return currLvl

def _sortAtts(x):
    a = x[0][0].get("NAME")
    b=x[0][0]
    c=b.items()[0][1].get("NAME")
    return a



UAT=parseXML_New('./IN_UAT.xml')
UAT_replace=replaceVerAll(UAT,mapping)
PRD=parseXML_New('./IN_PRD.xml')
a= cmpDeepLists(UAT,PRD)
print a
sys.exit(0)
jobList_A=parseXML('./IN_PRD.xml')
jobList_B=parseXML('./IN_UAT.xml')
jobList_C=replaceVer(jobList_B,mapping)

compareXML(jobList_A,jobList_C)
# atts = dict(job.attributes.items())

sys.exit(0)
attributes={}
for i in jobList_A:
    for key in jobList_A[i]:
        attributes[key]='1'

diff = set(jobList_A.items().items())^set(jobList_B.items().items())

print diff
sys.exit(0)
for job in jobList.keys():
    if job=="":continue
    for key in attributes:
        print ("%s:%s:%s" % (i, key, jobList[job].get(key,"")))

tulp1 = {'test_two': '124', 'test_four': '185', 'test_one': '196', 'test_three': '26', 'test_five': '489'}
tulp2 = {'test_two': '124', 'test_one': '196', 'test_three': '26'}

dif = set(tulp1.items())^set(tulp2.items())
print dif
