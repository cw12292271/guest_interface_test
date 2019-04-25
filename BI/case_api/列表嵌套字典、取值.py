rt1 = ['a', 'b']
rt2 = [{'a': 1, 'b': 2, 'c': 3, 'd': 4},
       {'d': 3, 'a': 3, 'b': 3, 'c': 4},
       {'d': 1, 'b': 1, 'c': 3, 'a': 2},
       {'a': 5, 'c': 6, 'd': 3, 'b': 0}]

result = [dict([(k, item[k]) for k in rt1]) for item in rt2]
print(result)
'''[{'a': 1, 'b': 2}, {'a': 3, 'b': 3}, {'a': 2, 'b': 1}, {'a': 5, 'b': 0}]'''

result = [(k, [x[k] for x in rt2]) for k in rt1]
print(result)
'''[('a', [1, 3, 2, 5]), ('b', [2, 3, 1, 0])]'''

result = [(k, sum([x[k] for x in rt2])) for k in rt1]
print(result)
'''[('a', 11), ('b', 6)]'''
