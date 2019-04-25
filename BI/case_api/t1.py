

alist = [6, 3, 8, 2, 9, 1]


# 冒泡排序
def bubble_sort(alist):
    """
    :param alist: list
    :return: list
    """
    for i in range(len(alist)):
        for j in range(len(alist) - 1):
            if alist[j] > alist[j + 1]:
                temp = alist[j]
                alist[j] = alist[j + 1]
                alist[j + 1] = temp
    return alist


def selection_sort(alist):
    b = []
    while alist:
        b.append(alist.pop(alist.index(min(alist))))
    alist = b
    return alist

print(selection_sort(alist))

