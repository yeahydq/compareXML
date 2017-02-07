#coding:utf-8
#!/usr/bin/env python
# __author__= 'dick'

tulp1 = {'test_two': '124', 'test_four': '185', 'test_one': '196', 'test_three': '26', 'test_five': '489'}
tulp2 = {'test_two': '124', 'test_one': '196', 'test_three': '26'}

dif = set(tulp1.items())^set(tulp2.items())
print dif

# print [k for k in set(tulp1)&set(tulp2) if tulp1.get(k) != tulp2.get(k)]
def cmpdicts(dct0, dct1):
    diffs = set()
    keys = set(dct0.keys() + dct1.keys())
    for k in keys:
            if cmp(dct0.get(k), dct1.get(k)):
                    diffs.add(k)
    return diffs

print cmpdicts(tulp1,tulp2)
