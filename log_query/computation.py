class fwrapper:
    def __init__(self, function, childcount, name):
        self.function = function
        self.childcount = childcount
        self.name = name

class node:
    def __init__(self, fw, children):
        self.function = fw.function
        self.children = children
        self.name = fw.name

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

class paramnode:
    def __init__(self, idx, name='param'):
        self.idx = idx
        self.name = name
        self.children = []

    def evaluate(self, inp):
        return inp[self.idx]

class listnode:
    def __init__(self, name='list'):
        self.name = name

    def evaluate(self, inp):
        return inp

class constnode:
    def __init__(self, v, name='const'):
        self.value = v
        self.name = name
        self.children = []

    def evaluate(self, inp):
        return self.value

    def set_value(self, v):
        if type(v) == list:
            self.value = len(v)
        else:
            self.value = v

class maxnode:
    def __init__(self, children, name='max'):
        self.children = children
        self.name = name
    def evaluate(self, inp):
        results = [self.children[i].evaluate(inp[0]) for i in xrange(len(self.children)-1)]
        results.append(self.children[-1].evaluate(inp[1]))
        return max(results)

class minnode:
    def __init__(self, children, name='min'):
        self.children = children
        self.name = name
    def evaluate(self, inp):
        results = [self.children[i].evaluate(inp[0]) for i in xrange(len(self.children)-1)]
        results.append(self.children[-1].evaluate(inp[1]))
        return min(results)

class sumnode:
    def __init__(self, children, name='sum'):
        self.children = children
        self.name = name
    def evaluate(self, inp):
        results = [self.children[i].evaluate(inp[0]) for i in xrange(len(self.children)-1)]
        results.append(self.children[-1].evaluate(inp[1]))
        return sum(results)

class countnode:
    def __init__(self, children, name='count'):
        self.children = children
        self.name = name
    def evaluate(self, inp):
        results = []
        for i in xrange(len(self.children)-1):
            temp = self.children[i].evaluate(inp[0])
            if type(temp) == list: results += temp
            else: results.append(temp)
        temp = self.children[-1].evaluate(inp[1])
        if type(temp) == list: results += temp
        else: results.append(temp)
        return list(set(results))

addfunc = fwrapper(lambda item: item[0] + item[1], 2, '+')
subfunc = fwrapper(lambda item: item[0] - item[1], 2, '-')
mulfunc = fwrapper(lambda item: item[0] * item[1], 2, '*')
divfunc = fwrapper(lambda item: item[0] / item[1], 2, '/')
gtfunc = fwrapper(lambda item: item[0] > item[1], 2, '>')
ltfunc = fwrapper(lambda item: item[0] < item[1], 2, '<')
eqfunc = fwrapper(lambda item: item[0] == item[1], 2, '==')
gtefunc = fwrapper(lambda item: item[0] >= item[1], 2, '>=')
ltefunc = fwrapper(lambda item: item[0] <= item[1], 2, '<=')
iffunc = fwrapper(lambda item: item[1] if item[0] else item[2], 3, 'if')

funcdict = {'+': addfunc, '-': subfunc, '*': mulfunc, '/': divfunc,
            '>': gtfunc, '<': ltfunc, '==': eqfunc, '>=': gtefunc,
            '<=': ltefunc, 'if': iffunc}
nodelist = {'max': maxnode, 'min': minnode, 'sum': sumnode, 'count': countnode}

def parse(fstr):
    parts = []
    flag = 0
    for i in range(len(fstr)):
        if fstr[i] >= '0' and fstr[i] <= '9':
            if flag == 1: parts[-1] = parts[-1]*10+int(fstr[i])
            else:
                parts.append(int(fstr[i]))
                flag = 1
        elif (fstr[i] >= 'a' and fstr[i] <= 'z') or (fstr[i] >= 'A' and fstr[i] <= 'Z'):
            if flag == 2: parts[-1] += fstr[i]
            else:
                parts.append(fstr[i])
                flag = 2
        else:
            if fstr[i] == '(':
                if len(parts) > 0 and parts[-1] in nodelist: parts[-1] += '('
                else: parts.append('(')
            elif fstr[i] == ')': parts.append(')')
            elif fstr[i] == ',': parts.append(',')
            elif fstr[i] == '=':
                if len(parts) > 0 and parts[-1] in ['=', '>', '<']: parts[-1] += '='
                else: parts.append('=')
            elif fstr[i] in funcdict: parts.append(fstr[i])
            flag = 0

    return parts

def compute(stack, s, operations):
    idx = s
    while idx < len(stack):
        if stack[idx] in operations:
            stack[idx-1] = node(funcdict[stack[idx]], [stack[idx-1], stack[idx+1]])
            del stack[idx:idx+2]
        else:
            idx += 1

def move_back(stack, specialnodes, rflag=''):
    idx = len(stack) - 1
    s = 0
    rstr = None
    while idx>0:
        if rflag != '' and type(stack[idx-1]) == str and stack[idx-1].endswith(rflag):
            rstr = stack[idx-1]
            del stack[idx-1]
            s = idx -1
            break
        elif stack[idx-1] != ',' and stack[idx-1] not in funcdict:
            return False
        idx -= 2
    compute(stack, s, ['+', '-'])
    compute(stack, s, ['<', '<=', '>=', '==', '>'])
    idx = s
    while idx < len(stack):
        if stack[idx] == 'if':
            stack[idx-1] = node(funcdict['if'], [stack[idx+1], stack[idx-1], constnode(0)])
            del stack[idx:idx+2]
        else:
            idx += 1
    if rstr == '(' or rstr == None:
        if s == len(stack)-1: return True
    else:
        temp = generate_special_node(stack, s, rstr[:-1])
        if temp != None:
            specialnodes.append((temp, constnode(0, 'NA')))
            stack[s] = specialnodes[-1][1]
        del stack[s+1:]
    return False

def generate_special_node(stack, s, rstr):
    if rstr not in nodelist: return None
    children = []
    for i in xrange(s, len(stack), 2):
        children.append(stack[i])
    if len(children) == 0: return None
    if rstr in ['max', 'min', 'sum']:
        children.append(paramnode(0))
    elif rstr == 'count':
        children.append(listnode())
    else:
        return None
    return nodelist[rstr](children)


def generate_function_tree(fstr, cdict):
    parts = parse(fstr)
    stack = []
    specialnodes = []
    for i in xrange(len(parts)):
        if type(parts[i]) == str and parts[i].endswith('('): stack.append(parts[i])
        elif parts[i] == ')':
            move_back(stack, specialnodes, '(')
            if len(stack) > 2 and (stack[-2] == '*' or stack[-2] == '/'):
                tempnode = node(funcdict[stack[-2]], [stack[-3], stack[-1]])
                del stack[-2:]
                stack[-1] = tempnode
        elif parts[i] not in funcdict:
            if type(parts[i]) == int: node1 = constnode(parts[i])
            elif parts[i] == ',': node1 = ','
            elif type(parts[i]) == str:
                try: node1 = paramnode(cdict[parts[i]])
                except: return None, None
            else: break
            if len(stack)>0 and (stack[-1] == '*' or stack[-1] == '/'):
                tempnode = node(funcdict[stack[-1]], [stack[-2], node1])
                del stack[-1]
                stack[-1] = tempnode
            else:
                stack.append(node1)
        elif parts[i] in funcdict:
            if parts[i] == 'if': move_back(stack, specialnodes)
            stack.append(parts[i])
    move_back(stack, specialnodes)
    return specialnodes, stack[0]

def has_paramnode(tree):
    if tree == None: return False
    for child in tree.children:
        if child.name == 'param': return True
        if has_paramnode(child) == True: return True
    return False
