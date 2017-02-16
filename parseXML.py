#coding:utf-8
#!/usr/bin/env python
# __author__= 'dick'

from xml.dom import minidom
import sys
import re
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


def replaceList(jobList=[], mapps={}):
    for i in range(len(jobList)):
        if type(jobList[i]) == dict:
            replaceDict(jobList[i],mapps)
        elif type(jobList[i]) == list:
            replaceList(jobList[i], mapps)
            pass


def replaceDict(jobList={}, mapps={}):
    for key in jobList:
        if type(jobList[key]) == dict:
            replaceDict(jobList[key],mapps)
        elif type(jobList[key]) == list:
            replaceList(jobList[key], mapps)

    for key,v in mapps.items():
        if jobList.get(key) == mapps[key][1]:
            jobList[key] = mapps[key][0]
    pass


def cmpdicts(dct0, dct1):
    diffs = {}
    keys = set(dct0.keys() + dct1.keys())
    for k in keys:
            if cmp(dct0.get(k), dct1.get(k)):
                diffs[k]=(dct0.get(k),dct1.get(k))
    return diffs


def _sortListMethod(l):
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,dict):
        try:
            return l.get('JOB').get('JOBNAME')
        except Exception,e:
            return l.get('JOB')


def getFromDict(d={},key="JOBNAME"):
    for k,v in d.items():
        if k==key:
            return v
        elif isinstance(v,dict):
            return getFromDict(v,key)


def cmpDeepLists(listA, listB):
    diffs = []
    #
    sortA=sorted(listA,key=_sortListMethod)
    sortB=sorted(listB,key=_sortListMethod)
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
                if curTypA==dict:
                    diffs.append({"Left Insert": curA.values()[0].get('JOBNAME',curA)})
                else:
                    diffs.append({"Left Insert": curA})
                iA += 1
        elif curA == nxtB:
            if curTypB == dict:
                diffs.append({"Right Insert": curB.values()[0].get('JOBNAME',curB)})
            else:
                diffs.append({"Right Insert": curB})
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
                diffs.append({"Left Insert": curA})
                iA += 1
            if curTypB != dict and nxtTypB==dict:
                diffs.append({"Right Insert", curB})
                iB += 1
        # if nxtA==None and nxtB==None:
        #     break
    # print list(set(listA).difference(set(listB)))
    return diffs

def cmpDeepDict(dct0, dct1,keyFld="JOBNAME"):
    diffs = {}
    keys = set(dct0.keys() + dct1.keys())
    for k in keys:
        if dct0.get(k)!=dct1.get(k):
            if dct1.get(k) == None:
                diffs[k] = {"Left Insert": 'where %s="%s", string %s="%s" is added' % (keyFld,dct0.get(keyFld),k, dct0.get(k))}
            elif dct0.get(k) == None:
                diffs[k] = {"Right Insert":'where %s="%s", string %s="%s" is added' % (keyFld,dct1.get(keyFld),k, dct1.get(k))}
            elif k==keyFld:
                diffs[k] = [
                            {"Left Insert": 'where %s="%s", string %s="%s" is added' % (keyFld,dct0.get(keyFld),k, dct0.get(k))},
                            {"Right Insert": 'where %s="%s", string %s="%s" is added' % (keyFld,dct1.get(keyFld),k, dct1.get(k))}
                            ]
                # diffs[k] = ("DICT RIGHT Insert:", dct1.get(keyFld), k, dct1.get(k))
            elif isinstance(dct0.get(k),list):
                diffs[k] = cmpDeepLists(dct0.get(k),dct1.get(k))
            elif type(dct0.get(k)) == dict and type(dct1.get(k)) == dict:
                diffs[k] = cmpDeepDict(dct0.get(k), dct1.get(k),keyFld)
            else:
                diffs[k]={"Change": 'where %s="%s", variable:%s changes from left="%s" to right="%s"' % (keyFld,dct1.get(keyFld),k,dct0.get(k),dct1.get(k))}
    return diffs


def getFrmList(l=[],i=0):
    if i >= len(l):
        return None
    else:
        # return l[min(i,len(l)-1)]
        return l[i]


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
    # currLvl=[[{tree.nodeName:dict(tree.attributes.items())}]]
    currLvl={tree.nodeName:dict(tree.attributes.items())}
    # print '---'*cnt, "NodeName:",tree.nodeName,"Value:",dict(tree.attributes.items())
    addnAttr=[]
    for childTree in iterate_children(tree):
        childLvl=loopXML(childTree,cnt+1)
        if childLvl <> None:
            addnAttr.append(childLvl)
    if len(addnAttr)>0:
        try:
            # addnAttrSorted=sorted(addnAttr,key=lambda x: x[0][0].items()[0][1].get("NAME"))
            addnAttrSorted=sorted(addnAttr,key=lambda x: x.items()[0][1].get("NAME"))
        except Exception,e:
            print('Cannot sort  : %s' %addnAttr)
            print('Error : %s' %e)
            pass
        else:
            addnAttr=addnAttrSorted
        # currLvl.extend(addnAttr)
        currLvl[tree.nodeName]["JOB_Attributes"]=addnAttr
    return currLvl

def _sortAtts(x):
    a = x[0][0].get("NAME")
    b=x[0][0]
    c=b.items()[0][1].get("NAME")
    return a


mapping={
    "NODE_ID":('PRD.SERVER','UAT.SERVER'),
    "USER_ID": ('PRD.ID', 'UAT.ID'),
}

# a=[0,1,{"NAME":4,'VAR1':1},{"NAME":4,'VAR2':1},4]
# b=[3,{"NAME":4,'VAR1':2},4,1,5]
# print cmpDeepLists(a,b)
# sys.exit(0)

def showResult(rslt):
    if isinstance(rslt,list):
        for i in range(len(rslt)):
            showResult(rslt[i])
    elif isinstance(rslt,dict):
        for key,v in rslt.items():
            if re.search(r'(.*Insert.*|.*Change.*|.*Delete.*)',key,re.IGNORECASE):
                print ("%s:%s") % (key,rslt.get(key))
            elif isinstance(rslt.get(key), list):
                showResult(rslt.get(key))
            elif isinstance(rslt.get(key), dict):
                showResult(rslt.get(key))
    pass

UAT=parseXML_New('./IN_UAT.xml')
replaceDict(UAT,mapping)
PRD=parseXML_New('./IN_PRD.xml')
a= cmpDeepDict(UAT,PRD)
# print a
showResult(a)
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
