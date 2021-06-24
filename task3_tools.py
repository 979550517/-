def fanx(x):
    #输入需要反向的字符串
    return x[::-1]

def hub(x):
    #输入需要互补的字符串
    a = ''
    for i in x:
        if i == 'A':
            a=a+'C'
        elif i == 'a':
            a=a+'c'
        elif i == 'C':
            a=a+'A'
        elif i=='c':
            a = a + 'a'
        elif i == 'G':
            a = a + 'T'
        elif i =='g':
            a = a + 't'
        elif i == 'T':
            a = a + 'G'
        elif i == 't':
            a = a + 'g'
    return a

def fanx_hub(x):
    c=x[::-1]
    a = ''
    for i in c:
        if i == 'A':
            a = a + 'C'
        elif i == 'a':
            a = a + 'c'
        elif i == 'C':
            a = a + 'A'
        elif i == 'c':
            a = a + 'a'
        elif i == 'G':
            a = a + 'T'
        elif i == 'g':
            a = a + 't'
        elif i == 'T':
            a = a + 'G'
        elif i == 't':
            a = a + 'g'
    return a

def selected_line(x,y,z):
    t=y-1
    r=z-1
    a=x[t:r]
    return a