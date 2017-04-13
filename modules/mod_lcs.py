# -*- coding: utf-8 -*-
def lcs(a, b):
    lena = len(a)
    lenb = len(b)
    c = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
    flag = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
    for i in range(lena):
        for j in range(lenb):
            if a[i] == b[j]:
                c[i + 1][j + 1] = c[i][j] + 1
                flag[i + 1][j + 1] = 'ok'
            elif c[i + 1][j] > c[i][j + 1]:
                c[i + 1][j + 1] = c[i + 1][j]
                flag[i + 1][j + 1] = 'left'
            else:
                c[i + 1][j + 1] = c[i][j + 1]
                flag[i + 1][j + 1] = 'up'
    return c, flag


def printLcs(flag, a, i, j,lcs_title):

    if i == 0 or j == 0:
        return
    if flag[i][j] == 'ok':
        printLcs(flag, a, i - 1, j - 1,lcs_title)
        #print(a[i - 1])
        lcs_title.append(a[i - 1])
    elif flag[i][j] == 'left':
        printLcs(flag, a, i, j - 1,lcs_title)
    else:
        printLcs(flag, a, i - 1, j,lcs_title)
    return lcs_title
