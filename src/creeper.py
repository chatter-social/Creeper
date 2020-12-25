from sly import Lexer
from sly import Parser
import re
import sys

class CreeperLexer(Lexer): 
    tokens = { VAR, FUNCTION, NAME, NUMBER, STRING, FLOAT } 
    ignore = '\t '
    literals = { '=', '+', '-', '/',  
                '*', '(', ')', ',', ';', '&', '(', ')', ':', '.'}
  
  
    # define tokens as regular expressions
    VAR = r'var'
    FUNCTION = r'define'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    FLOAT = r'([1-9]\d*(\.\d*[1-9])|0\.\d*[1-9]+)'
    
    # print(re.findall(FUNCTION, '''define add(x, y):

# z = x + y

# end''')[0])

  
    # numerical token 
    @_(r'\d+') 
    def NUMBER(self, t): 
        
        # convert it into a python integer 
        t.value = int(t.value)  
        return t

    @_(r'([1-9]\d*(\.\d*[1-9])|0\.\d*[1-9]+)')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t
    
    @_(r'(?s)define.*\(.*\):.*end')
    def FUNCTION(self, t):
        t.value = str(t.value)
        return t
  
    # comment token
    @_(r'//.*') 
    def COMMENT(self, t): 
        pass
  
    @_(r'\n+') 
    def newline(self, t): 
        self.lineno = t.value.count('\n')

class CreeperParser(Parser): 
    tokens = CreeperLexer.tokens

    precedence = ( 
        ('left', '+', '-'), 
        ('left', '*', '/'), 
        ('left', '&'), 
        ('right', 'UMINUS'), 
    ) 

    start = 'statement'

    def __init__(self): 
        self.env = { } 

    @_('') 
    def statement(self, p): 
        pass

    @_('var_assign') 
    def statement(self, p): 
        return p.var_assign

    @_('function_define') 
    def statement(self, p): 
        return p.function_define

    @_('function_call') 
    def statement(self, p): 
        return p.function_call

    @_('VAR NAME "=" expr') 
    def var_assign(self, p): 
        return ('var_assign', p.NAME, p.expr) 

    @_('NAME "=" STRING ";"') 
    def var_assign(self, p): 
        return ('var_assign', p.NAME, p.STRING)
    
    @_('FUNCTION NAME "(" NAME ")" ":" STRING ";"') 
    def function_define(self, p): 
        return ('function_define', p.NAME0, p.NAME1, p.STRING)

    # NAME "(" ")" ":" STRING

    @_('NAME "(" NAME ")" ";"') 
    def function_call(self, p): 
        return ('function_call', p.NAME0, p.NAME1) 

    @_('expr') 
    def statement(self, p): 
        return (p.expr) 

    @_('expr "+" expr') 
    def expr(self, p): 
        return ('add', p.expr0, p.expr1) 

    @_('expr "-" expr') 
    def expr(self, p): 
        return ('sub', p.expr0, p.expr1) 

    @_('expr "*" expr') 
    def expr(self, p): 
        return ('mul', p.expr0, p.expr1) 

    @_('expr "/" expr') 
    def expr(self, p): 
        return ('div', p.expr0, p.expr1) 

    @_('expr "&" expr') 
    def expr(self, p): 
        return ('concat', p.expr0, p.expr1) 

    @_('"-" expr %prec UMINUS') 
    def expr(self, p): 
        return p.expr 

    @_('NAME') 
    def expr(self, p): 
        return ('var', p.NAME) 

    @_('NUMBER') 
    def expr(self, p): 
        return ('int', p.NUMBER)

    @_('FLOAT') 
    def expr(self, p): 
        return ('float', p.FLOAT)

class CreeperExecute: 
    
    def __init__(self, tree, env): 
        self.env = env 
        result = self.walkTree(tree) 
        if result is not None and isinstance(result, int): 
            print(result)
        if result is not None and isinstance(result, float): 
            print(result) 
        if isinstance(result, str) and result[0] == '"': 
            print(result) 
  
    def walkTree(self, node): 
  
        if isinstance(node, int): 
            return node
        if isinstance(node, float): 
            return node
        if isinstance(node, str): 
            return node 
  
        if node is None: 
            return None
  
        if node[0] == 'program': 
            if node[1] == None: 
                self.walkTree(node[2]) 
            else: 
                self.walkTree(node[1]) 
                self.walkTree(node[2]) 
  
        if node[0] == 'int': 
            return node[1] 
  
        if node[0] == 'str': 
            return node[1]

        if node[0] == 'float': 
            return node[1] 
  
        if node[0] == 'add': 
            return self.walkTree(node[1]) + self.walkTree(node[2]) 
        elif node[0] == 'sub': 
            return self.walkTree(node[1]) - self.walkTree(node[2]) 
        elif node[0] == 'mul': 
            return self.walkTree(node[1]) * self.walkTree(node[2]) 
        elif node[0] == 'div': 
            return self.walkTree(node[1]) / self.walkTree(node[2]) 
        elif node[0] == 'concat':
            tempString = re.sub('["]', '', str(self.walkTree(node[1])) + str(self.walkTree(node[2])))
            return f'"{tempString}"'
        
        if node[0] == 'function_define':
            self.env[node[1] + '_function'] = self.walkTree(node[2]) + ',' + self.walkTree(node[3]).replace('"', '')
            return node[1]

        if node[0] == 'function_call':
            print(node[1])
            variable_name = self.env[node[1] + '_function'].split(',')[0]
            try:
                value = self.env[variable_name]
            except KeyError:
                self.env[variable_name] = int(0)
            function_body = self.env[node[1] + '_function'].split(',')[1]
            function_body = function_body.split(';')
            lexer = CreeperLexer() 
            parser = CreeperParser()
            for line in function_body:
                tree = parser.parse(lexer.tokenize(line)) 
                CreeperExecute(tree, env)
            return node[1] 
            
        if node[0] == 'var_assign': 
            self.env[node[1]] = self.walkTree(node[2]) 
            return node[1] 
  
        if node[0] == 'var': 
            try: 
                return self.env[node[1]] 
            except LookupError: 
                print("Undefined name '"+node[1]+"' .") 
                return 0

if __name__ == '__main__':
    print('Creeper Interpreter v1.1') 
    lexer = CreeperLexer() 
    parser = CreeperParser() 
    env = {} 
    try:
        filename = sys.argv[1]
        f = open(filename, 'r')
        contents = f.read()
        contents = contents.split('\n')
        for line in contents:
            tree = parser.parse(lexer.tokenize(line)) 
            CreeperExecute(tree, env)
    except IndexError:
        print('Creeper did not detect specified filename to execute. Launching interpreter...')
      
        while True: 
          
            try: 
                text = input('Creeper >> ') 
          
            except EOFError: 
                break
          
            if text: 
                tree = parser.parse(lexer.tokenize(text)) 
                print(tree)
                CreeperExecute(tree, env)
                print(env)
