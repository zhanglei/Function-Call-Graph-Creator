import os
import pygraphviz as pgv

class Function:
    def __init__(self, _fn, _fp, _fa):
        self.functionName, self.functionPosition, self.functionAddr = _fn, _fp, _fa
        self.childs = []
        self.parent = None
        self.prefixLength = 0
        self.isFirstChild = False
    
    def meCallYou(self, function):
        function.parent = self
        if not self.childs:
            function.isFirstChild = True
        self.childs.append(function)

    def setPrefixLength(self, prefixlen):
        self.prefixLength = prefixlen

    def __eq__(self, other):
        return self.functionAddr == other.functionAddr \
        and self.functionName == other.functionName \
        and self.functionPosition == other.functionPosition

    def __str__(self):
        return '%s@%s' % (self.functionName, self.functionPosition) 

def getLabel(array):
    i = 0
    label = ''
    while i < len(array):
        j = i + 1
        while j < len(array) and array[j] == array[j - 1] + 1:
            j += 1
        if array[i] == array[j - 1]:
            label += str(array[i]) + ','
        else:
            label += str(array[i]) + '-' + str(array[j - 1]) + ','
        i = j
    return label[:-1]

def getEdgeLabel(edgeHASH, startnode, endnode, step):
    key = str(startnode) + '=>' + str(endnode)
    if key in edgeHASH:
        edgeHASH[key].append(step)
        #get label like "1-5,8,10-12"
        return getLabel(edgeHASH[key])
    else:
        edgeHASH[key] = [step]
        return str(step)    

def printCallGraphAsPicture(graph):
    G = pgv.AGraph(directed = True,strict = True)
    G.add_node(str(graph))
    step = 1
    stack = [graph]
    edgeHASH = {}
    while stack:
        current = stack.pop()
        parent = current.parent
        G.add_node(str(current))
        if parent:
            label = getEdgeLabel(edgeHASH, parent, current, step)
            G.add_edge(str(parent), str(current), label = label)
            step += 1
        for node in current.childs[::-1]:
            stack.append(node)
    G.layout('dot')
    G.draw('CallGraph.png')

def printCallGraphAsSimpleFigure(graph):
    with open('CallGraphAsSimpleFigure.txt', 'w') as fp:
        fp.write('***')
        step = 1
        stack = [graph]
        while stack:
            current = stack.pop()
            parent = current.parent
            if parent:
                edge = '--(%d)-->' % step
                current.setPrefixLength(parent.prefixLength + len(str(parent)) + len(edge))
                if current.isFirstChild:
                    fp.write(edge + str(current))
                else:
                    writeout = ' ' * (parent.prefixLength + len(str(parent)))
                    fp.write(writeout + edge + str(current))
                step += 1
            else:#head
                fp.write(str(current))
                current.setPrefixLength(0)
            if not current.childs:
                fp.write('\n***')
            for node in current.childs[::-1]:
                stack.append(node)

def getFunctionInformation(functionAddr):
    outputs = os.popen('addr2line -e test %s -f -s -p' % functionAddr).readline().strip().split(' ')
    return outputs[0], outputs[2]

def readCallRecord():
    stack = []
    graphHead = None
    with open('CallRecord.txt', 'r') as inputFile:
        for line in inputFile:
            line = line.strip()
            functionAddr = line[7:].split(',')[0]
            functionName, functionPosition = getFunctionInformation(functionAddr)
            function = Function(functionName, functionPosition, functionAddr)
            if line.startswith('Enter:'):
                stack.append(function)
            else:
                if not stack:
                    print 'Error Call Record File.'
                    exit(1)
                top = stack[-1]
                if top == function:
                    stack.pop()
                    if not stack:
                        graphHead = top
                    else:
                        parent = stack[-1]
                        parent.meCallYou(top)
                else:
                    print 'Error Call Record File.'
                    exit(1)
    return graphHead

graph = readCallRecord()
printCallGraphAsSimpleFigure(graph)
