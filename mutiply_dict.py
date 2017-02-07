#coding:utf-8
#!/usr/bin/env python
# __author__= 'dick'

def dget(dictionary, cmd, default=None):
    cmd_list = cmd.split('.')
    tmp = dict(dictionary)
    for c in cmd_list:
        try:
            val = tmp.get(c, None)
        except AttributeError:
            return default
        if val!= None:
            tmp = val
        else:
            return default
    return tmp

if __name__ == "__main__":
    data = {'a':{'b':{'c':1}}}
    print dget(data, 'a.b.c') # 1
    print dget(data, 'a.d.e') # None
    print dget(data, 'a.b') # {'c': 1}
