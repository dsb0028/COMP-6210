import argparse
import tokenizer
import parserC
import optimizer
from ThreeAddressCode import *
import x86
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-p', action='store_true')
    parser.add_argument('-O1',action='store_true')
    parser.add_argument('-O2',action='store_true')
    parser.add_argument('-S',action='store_true')
    parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()
    #print(args._get_args)
    #breakpoint()
    #print(args)
    s = args.file.read()
    #breakpoint()
    tokens = tokenizer.tokenize(s)
    #if -t is passed, print tokens
    if  args.t == True:
        print("Tokens",tokens,'\n')
    # if c file just contains comments, there will be no tokens and no parse tree
    if not tokens:
        raise RuntimeError("Nothing to Parse")
    #breakpoint()
    parseTree,astTree,symbolTable = parserC.createParseTree(tokens)
    #ast = parserC.createAST(parseTree)
    if args.p == True: 
        #from https://stackoverflow.com/questions/17280534/prettyprint-to-a-file  
        with open('parseTree.txt', 'wt') as out:
            pprint(parseTree, stream=out,sort_dicts=False)
        #print("Parse Tree",parseTree,'\n',"Symbol Table",symbolTable.table,'\n')
        #from https://stackoverflow.com/questions/17280534/prettyprint-to-a-file  
        with open('astTree.txt', 'wt') as out:
            pprint(astTree, stream=out,sort_dicts=False)
        #print("AST",astTree,'\n')
    #breakpoint()
    threeAddressCode,symbolTable = createThreeAddressCode(astTree,symbolTable)
    #print(threeAddressCode)
    #function_names = list(astTree.keys())
    #breakpoint()
    if args.O1 == True:
        for function_name in threeAddressCode:
            parameters = symbolTable.table[function_name]['Parameters']
            param_str = [str(parameters[parm]) + ' ' + str(parm) for parm in parameters]
            param_str = ','.join(param_str)
            function_header = function_name+'(' + param_str + ')'
            #print('{')
            print(function_header)
            print('{')
            variables = symbolTable.table[function_name]['Variables']
            #breakpoint()
            for var in variables:
                #breakpoint()
                width = len(function_header) + 13
                if len(var) < 2:
                    width = width - 2 
                printedLine = variables[var] + ' ' + var + ';'
                print(printedLine.center(width,' '))
            #breakpoint()
            tac = threeAddressCode[function_name]
            for line in tac:
                #breakpoint()
                width = len(function_header) + 15
                printedLine = ' '
                if line.statement['STATEMENT'] == 'return':
                    printedLine = str(line.statement['STATEMENT']) + ' ' + str(line.arg1['ARG1']) + ';'
                    #width = width + 15
                    #breakpoint()
                    #print(printedLine.center(20," "))
                else:
                    if line.operation['Operation'] != '=':
                        
                        if len(line.result['RESULT']) > 1:
                            width = width + len(str(line.result['RESULT'])) - 1
                        #breakpoint()
                        if len(str(line.arg1['ARG1'])) > 1:
                            width = width + len(str(line.arg1['ARG1']))
                        if len(str(line.arg2['ARG2'])) > 1:
                            width = width + len(str(line.arg2['ARG2']))
                        if len(str(line.arg1['ARG1'])) > 1 or len(str(line.arg2['ARG2'])) > 1:
                            width = width - 1
                        printedLine = str(line.result['RESULT']) + ' = ' \
                            + str(line.arg1['ARG1']) + ' ' + str(line.operation['Operation']) \
                            + ' ' + str(line.arg2['ARG2']) + ';'
                        #width = 20
                    else:
                        printedLine = str(line.result['RESULT']) + ' ' + str(line.operation['Operation']) \
                            + ' '+str(line.arg1['ARG1']) + ';'
                        width = width - 4
                        if len(str(line.arg1['ARG1'])) > 1:
                            width = width + 1
                print(printedLine.center(width,' '))
            #elif threeAddrCode.statement == 'return':
            #    pass
            print('}')
            print('\n')
           
        #print(ThreeAddressCode.__str__(threeAddressCode,threeAddressCodeDict=threeAddressCode))
    optimizedCode = None
    if args.O2 == True:
        breakpoint()
        optimizedCode = optimizer.performOptimizations(threeAddressCode,symbolTable)
        """
        for threeAddrCode in optimizedCode:
            print(threeAddrCode.operation,threeAddrCode.arg1, 
              threeAddrCode.arg2, 
              threeAddrCode.result, threeAddrCode.statement)
        """
        breakpoint()
        print("Optimized",'\n')
        for function_name in optimizedCode:
            function_header = function_name+':'
            print(function_header)
            variables = symbolTable.table[function_name]['Variables']
            #breakpoint()
            for var in variables:
                #breakpoint()
                width = len(function_header) + 13
                if len(var) < 2:
                    width = width - 2 
                printedLine = variables[var] + ' ' + var + ';'
                print(printedLine.center(width,' '))
            #breakpoint()
            tac = optimizedCode[function_name]
            for line in tac:
                #breakpoint()
                width = len(function_header) + 15
                printedLine = ' '
                if line.statement['STATEMENT'] == 'return':
                    printedLine = str(line.statement['STATEMENT']) + ' ' + str(line.arg1['ARG1']) + ';'
                    #width = width + 15
                    #breakpoint()
                    #print(printedLine.center(20," "))
                else:
                    if line.operation['Operation'] != '=':
                        if len(line.result['RESULT']) > 1:
                            width = width + len(str(line.result['RESULT'])) - 1
                        #breakpoint()
                        if len(str(line.arg1['ARG1'])) > 1:
                            width = width + len(str(line.arg1['ARG1'])) - 1
                        if len(str(line.arg2['ARG2'])) > 1:
                            width = width + len(str(line.arg2['ARG2'])) - 1
                        printedLine = str(line.result['RESULT']) + ' = ' \
                            + str(line.arg1['ARG1']) + ' ' + str(line.operation['Operation']) \
                            + ' ' + str(line.arg2['ARG2']) + ';'
                        #width = 20
                    else:
                        printedLine = str(line.result['RESULT']) + ' ' + str(line.operation['Operation']) \
                            + ' '+str(line.arg1['ARG1']) + ';'
                        width = width - 3
                print(printedLine.center(width,' '))
        print('\n')
    if args.O2 == True:
        assembly =  x86.createAssemblyCode(optimizedCode,symbolTable)
    else:
        breakpoint()
        assembly =  x86.createAssemblyCode(threeAddressCode,symbolTable)

    if args.S == True or (args.t == False and args.p == False and args.O1 == False and args.O2 == False):
        breakpoint()
        for func in assembly:
            function_header = func+':'
            print(function_header)
            func_asm = assembly[func]
            for line in func_asm:
                #breakpoint()
                width = len(function_header) + 15
                printedLine = ' '
                #breakpoint()
                if line.label != None:
                    if len(line.operands) == 2:
                        width = width + 20
                        #print(line.operands[0],line.operands[1])
                        if line.operands[0].startswith('['):
                            if len(str(line.operands[0])) < 3:
                                width = width - 2
                           
                            if len(str(line.operands[1])) < 3:
                                width = width - 1    
                            elif len(str(line.operands[1])) >= 3:
                                width = width + 1
                            printedLine = line.mnemonic + ' '+ line.label + ' ' + str(line.operands[0]) \
                                + ' , ' + str(line.operands[1])
                        else:
                            if len(str(line.operands[0])) == 3:
                                width = width + 1
                            printedLine = line.mnemonic + ' ' + str(line.operands[0]) \
                                + ' , ' + line.label + ' ' + str(line.operands[1])
                    else:
                        printedLine = line.mnemonic + ' ' + line.operands
                else:
                    if len(line.operands) == 2:
                        width = width + 5
                        #breakpoint()
                        if len(line.mnemonic) > 3:
                            width = width + 1
                        if len(str(line.operands[0])) < 3:
                            width = width - 2

                        if len(str(line.operands[1])) < 3:
                            width = width - 2

                        printedLine = line.mnemonic + ' ' + str(line.operands[0]) \
                            + ' , ' + str(line.operands[1])
                    elif len(line.operands) == 1:
                        width = width - 1
                        printedLine = line.mnemonic + ' '+ line.operands[0]
                    elif line.operands == []:
                        width = width - 5
                        printedLine = line.mnemonic
                print(printedLine.center(width,' '))
if __name__ == "__main__":
    main()
