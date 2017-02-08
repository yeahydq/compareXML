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
        if job.hasAttribute('INCOND'):
            print "name element:%s"%job.getAttribute('INCOND')
        childDict={}
        for child in iterate_children(job):
            # print child.localName
            # print dict(child.attributes.items())
            childDict[child.localName]=dict(child.attributes.items())
        jobList[jobName].update(childDict)

    return jobList
def replaceVer(jobList={},mapps={}):
    newList=copy.deepcopy(jobList)
    for job in newList:
        for key in mapps:
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
