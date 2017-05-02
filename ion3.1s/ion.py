import sys
fileOpen = open('test.i',"r")
fileLines = fileOpen.readlines()
code = []
for i in fileLines:
    while i[0] == " ":
        i = i[1:]
    if i[-1:] == "\n":
        i = i[:-1]
    code.append(i)
curlPairs, curlPairsBack, funs, halfp = {},{},{},{}
place, depth = 0, 0
for i in code:
    if "{" in i:
        depth += 1
        halfp[depth] = place
    elif "}" in i:
        curlPairs[place] = halfp[depth]
        curlPairsBack[halfp[depth]] = place
        depth -= 1
    place += 1
varriables = {}
def varNorm(string):
    if str(string) in varriables:
        return(int(varriables[str(string)]))
    return(int(str(string)))
def mathLine(listComms):
    coms = listComms
    coms[0], coms[2] = varNorm(coms[0]), varNorm(coms[2])
    if coms[1] == "+":
        return(coms[0]+coms[2])
    if coms[1] == "-":
        return(coms[0]-coms[2])
    if coms[1] == "*":
        return(coms[0]*coms[2])
    if coms[1] == "/":
        return(coms[0]/coms[2])
    if coms[1] == "^":
        return(coms[0]**coms[2])
    if coms[1] == "%":
        return(coms[0]%coms[2])
def ifLine(listComms):
    coms = listComms
    coms[0], coms[2] = varNorm(coms[0]), varNorm(coms[2])
    if coms[1] == "!=":
        return(coms[0]!=coms[2])
    if coms[1] == "=":
        return(coms[0]==coms[2])
    if coms[1] == ">":
        return(coms[0]>coms[2])
    if coms[1] == "<":
        return(coms[0]<coms[2])
    if coms[1] == "<=":
        return(coms[0]<=coms[2])
    if coms[1] == ">=":
        return(coms[0]>=coms[2])
def run(codeIn,line):
    codeLine = codeIn[line]
    splitLine = codeLine.split()
    if len(splitLine) == 0 or splitLine[0] in ["}","#"]:
        pass
    elif splitLine[0] == "print":
        for i in splitLine[1:]:
            print(varNorm(i))
    elif splitLine[0] == "text":
        wordToPrint = ""
        for i in splitLine[1:]:
            wordToPrint += i + " "
        print(wordToPrint)
    elif splitLine[0] == "if":
        inIf = ifLine(splitLine[1:4])
        if not inIf:
            return(int(curlPairsBack[line]))
    elif splitLine[0] == "while":
        inIf = ifLine(splitLine[1:4])
        if not inIf:
            return(curlPairsBack[line])
        else:
            holdLine = line
            while ifLine(splitLine[1:4]):
                endWhile, line = curlPairsBack[holdLine], holdLine+1
                while endWhile != line:
                    line = do(code,line)
    elif splitLine[1] == "=":
        if splitLine[2] == "input":
            varriables[splitLine[0]] = int(input())
        else:
            if len(splitLine) == 5:
                varriables[splitLine[0]] = mathLine(splitLine[2:])
            else:
                varriables[splitLine[0]] = varNorm(splitLine[2])
def do(code,lineInCode):
    resultOfRun = run(code,lineInCode)
    if isinstance(resultOfRun,int):
        lineInCode = resultOfRun
    return(lineInCode + 1)
lineInCode = 0
while lineInCode < len(code):
    lineInCode = do(code,lineInCode)
