# Statement logic formula parser, using Reverse Polish Notation

def tokenize(formula: str):
    newFormula = ""
    n = len(formula)
    for idx, c in enumerate(formula):
        newFormula += c
        if idx != n-1 and formula[idx+1] == ")" or c == "(":
            newFormula += " "
    
    return newFormula.split()

OPERATORS = {
    "not":6, 
    "and":5, 
    "or":4, 
    "impl":3, 
    "equals":2,
    "(":1,
    ")":1
}

def isVariable(token: str) -> bool:
    return token not in OPERATORS


def rpnOf(formula: str) -> list:
    """
    Dijkstra's shunting yard algorithm to convert formulas to rpn
    """
    tokens = tokenize(formula)
    output = []
    operators = []
    for token in tokens:
        if isVariable(token):
            output.append(token)
        elif token == "(":
            operators.append(token)
        elif  token == ")":
            # print(len(operators))
            if len(operators) == 0:
                continue
            top = operators[len(operators)-1]
            while top != "(" and len(operators) != 0:
                output.append(operators.pop())
                top = operators[len(operators)-1]
            operators.pop()
        else:
            operators.append(token)
            if len(operators) == 0:
                continue
            top = operators[len(operators)-1]
            while (top != "(" and OPERATORS[top] > OPERATORS[token]):
                output.append(operators.pop())
    
    while len(operators) > 0:
        output.append(operators.pop())
        
    return output

def compute(op:str, lhs:bool, rhs:bool) -> bool:
    if op == "and":
        return lhs and rhs
    elif op == "or":
        return lhs or rhs
    elif op == "impl":
        return not lhs or rhs
    elif op == "equals":
        return (not lhs or rhs) and (not rhs or lhs)

    print("Something went wrong")
    return False

def evaluate(formula:str, model: dict):
    rpn = rpnOf(formula)
    print(rpn)
    stack = []
    for token in rpn:
        if isVariable(token):
            stack.append(model[token])
        else:
            if token == "not":
                lhs = stack.pop()
                stack.append(not lhs)
            else:
                rhs = stack.pop()
                lhs = stack.pop()
                stack.append(compute(token, lhs, rhs))
    return stack.pop()


def main():
    test = "(not asd) impl lol"
    testModel = {
        "asd":True,
        "lol": True
    }
    asd = evaluate(test, testModel)
    print(asd)

if __name__ == "__main__":
    main()