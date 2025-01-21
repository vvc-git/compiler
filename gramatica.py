# Grupo: Cristian Alexandre Alchini, João Pedro Adami do Nascimento, Marcos Henrique Kogler, Victor do Valle Cunha 
# Modificações na linguagem:
#   Foi adicionada a palavra reservada 'run' na produção: FUNCCALL -> run ident(PARAMLISTCALL)
from tabelaGlobal import tabela as ts


class Producao:
  def __init__(self, cabeca, cauda):
    self.cabeca = cabeca
    self.cauda = cauda
  
  def is_epsilon(self):
    if len(self.cauda) == 1:
      simbolo = self.cauda[0]
      if isinstance(simbolo, Terminal) and simbolo.nome == "&":
        return True
    return False

class Variavel:
  def __init__(self, nome):
    self.nome = nome    
    self.tipo = None
    self.tipo_herdado = None

class Terminal:
  def __init__(self, nome):
    self.nome = nome 
    self.vallex = None   

class Acao_Semantica:
  def __init__(self, funcao, lista_parametros):
    self.funcao = funcao
    self.parametros = lista_parametros

# Instanciando os símbolos não terminais
PROGRAM = Variavel("PROGRAM")
FUNCLIST = Variavel("FUNCLIST")
FUNCLIST1 = Variavel("FUNCLIST1")
FUNCDEF = Variavel("FUNCDEF")
TYPE = Variavel("TYPE")
PARAMLIST = Variavel("PARAMLIST")
PARAMLIST1 = Variavel("PARAMLIST1")
STATEMENT = Variavel("STATEMENT")
VARDECL = Variavel("VARDECL")
ARRAYINTCONST = Variavel("ARRAYINTCONST")
ATRIBSTAT = Variavel("ATRIBSTAT")
RVALUE = Variavel("RVALUE")
FUNCCALL = Variavel("FUNCCALL")
PARAMLISTCALL = Variavel("PARAMLISTCALL")
PARAMLISTCALL1 = Variavel("PARAMLISTCALL1")
PRINTSTAT = Variavel("PRINTSTAT")
READSTAT = Variavel("READSTAT")
RETURNSTAT = Variavel("RETURNSTAT")
IFSTAT = Variavel("IFSTAT")
ELSESTAT = Variavel("ELSESTAT")
FORSTAT = Variavel("FORSTAT")
STATELIST = Variavel("STATELIST")
STATELIST1 = Variavel("STATELIST1")
ALLOCEXPRESSION = Variavel("ALLOCEXPRESSION")
NUMEXPRARRAY = Variavel("NUMEXPRARRAY")
NUMEXPRARRAY1 = Variavel("NUMEXPRARRAY1")
RELOP = Variavel("RELOP")
EXPRESSION = Variavel("EXPRESSION")
EXPRESSION1 = Variavel("EXPRESSION1")
SIGNAL = Variavel("SIGNAL")
NUMEXPRESSION = Variavel("NUMEXPRESSION")
NUMEXPRESSION1 = Variavel("NUMEXPRESSION1")
TERM_REC = Variavel("TERM_REC")
TERM_REC1 = Variavel("TERM_REC1")
OPERATOR = Variavel("OPERATOR")
TERM = Variavel("TERM")
TERM1 = Variavel("TERM1")
UNARYEXPR_REC = Variavel("UNARYEXPR_REC")
UNARYEXPR_REC1 = Variavel("UNARYEXPR_REC1")
UNARYEXPR = Variavel("UNARYEXPR")
FACTOR = Variavel("FACTOR")
LVALUE = Variavel("LVALUE")
LVALUE1 = Variavel("LVALUE1")
NUMEXPRESSION_REC = Variavel("NUMEXPRESSION_REC")
NUMEXPRESSION_REC1 = Variavel("NUMEXPRESSION_REC1")

# Instanciando os símbolos terminais
abre_chave = Terminal("{")
fecha_chave = Terminal("}")
break_ = Terminal("break")
ponto_virgula = Terminal(";")
int_ = Terminal("int")
float_ = Terminal("float")
string_ = Terminal("string")
print_ = Terminal("print")
read = Terminal("read")
return_ = Terminal("return")
if_ = Terminal("if")
else_ = Terminal("else")
for_ = Terminal("for")
def_ = Terminal("def")
ident = Terminal("ident")
virgula = Terminal(",")
abre_colchete = Terminal("[")
fecha_colchete = Terminal("]")
new = Terminal("new")
run = Terminal("run")
mais = Terminal("+")
menos = Terminal("-")
multiplicacao = Terminal("*")
divisao = Terminal("/")
modulo = Terminal("%")
int_constant = Terminal("int_constant")
float_constant = Terminal("float_constant")
string_constant = Terminal("string_constant")
null = Terminal("null")
abre_parentese = Terminal("(")
fecha_parentese = Terminal(")")
menor = Terminal("<")
maior = Terminal(">")
menor_igual = Terminal("<=")
maior_igual = Terminal(">=")
igual_igual = Terminal("==")
diferente = Terminal("!=")
atribui = Terminal("=")
e_comercial = Terminal("&")

def f1(l):
  l[0].tipo = l[1]

def f_add_tipo_ts(l):
  ts.adiciona_tipo(l[1].vallex, l[0].tipo)

add_tipo_int = Acao_Semantica(f1, [TYPE, "int"])
add_tipo_float = Acao_Semantica(f1, [TYPE, "float"])
add_tipo_string = Acao_Semantica(f1, [TYPE, "string"])
add_tipo_array = Acao_Semantica(f1, [TYPE, "array"])
add_tipo_ts = Acao_Semantica(f_add_tipo_ts, [TYPE, ident])

producoes = {
    "PROGRAM": [Producao(PROGRAM, [STATEMENT]), Producao(PROGRAM, [FUNCLIST]), Producao(PROGRAM, [e_comercial])],
    "FUNCLIST": [Producao(FUNCLIST, [FUNCDEF, FUNCLIST1])],
    "FUNCLIST1": [Producao(FUNCLIST1, [FUNCLIST]), Producao(FUNCLIST1, [e_comercial])],
    "FUNCDEF": [Producao(FUNCDEF, [def_, ident, abre_parentese, PARAMLIST, fecha_parentese, abre_chave, STATELIST, fecha_chave])],
    # "TYPE": [Producao(TYPE, [int_, add_tipo_int]), Producao(TYPE, [float_, add_tipo_float]), Producao(TYPE, [string_, add_tipo_string])],
    "TYPE": [Producao(TYPE, [int_, add_tipo_int]), Producao(TYPE, [float_, add_tipo_float]), Producao(TYPE, [string_, add_tipo_string])],
    # "PARAMLIST": [Producao(PARAMLIST, [TYPE, ident, add_tipo_ts, PARAMLIST1]), Producao(PARAMLIST, [e_comercial])],
    "PARAMLIST": [Producao(PARAMLIST, [TYPE, ident, add_tipo_ts,  PARAMLIST1]), Producao(PARAMLIST, [e_comercial])],
    "PARAMLIST1": [Producao(PARAMLIST1, [virgula, PARAMLIST]), Producao(PARAMLIST1, [e_comercial])],
    "STATEMENT": [
        Producao(STATEMENT, [VARDECL, ponto_virgula]),
        Producao(STATEMENT, [ATRIBSTAT, ponto_virgula]),
        Producao(STATEMENT, [PRINTSTAT, ponto_virgula]),
        Producao(STATEMENT, [READSTAT, ponto_virgula]),
        Producao(STATEMENT, [RETURNSTAT, ponto_virgula]),
        Producao(STATEMENT, [IFSTAT]),
        Producao(STATEMENT, [FORSTAT]),
        Producao(STATEMENT, [abre_chave, STATELIST, fecha_chave]),
        Producao(STATEMENT, [break_, ponto_virgula]),
        Producao(STATEMENT, [ponto_virgula])
    ],
    # "VARDECL": [Producao(VARDECL, [TYPE, ident, add_tipo_ts, ARRAYINTCONST])],
    "VARDECL": [Producao(VARDECL, [TYPE, ident, ARRAYINTCONST, add_tipo_ts])],
    "ARRAYINTCONST": [Producao(ARRAYINTCONST, [abre_colchete, int_constant, fecha_colchete, add_tipo_array, add_tipo_ts]), Producao(ARRAYINTCONST, [e_comercial])],
    "ATRIBSTAT": [Producao(ATRIBSTAT, [LVALUE, atribui, RVALUE])],
    "RVALUE": [Producao(RVALUE, [EXPRESSION]), Producao(RVALUE, [ALLOCEXPRESSION]), Producao(RVALUE, [FUNCCALL])],
    "FUNCCALL": [Producao(FUNCCALL, [run, ident, abre_parentese, PARAMLISTCALL, fecha_parentese])],
    "PARAMLISTCALL": [Producao(PARAMLISTCALL, [ident, PARAMLISTCALL1]), Producao(PARAMLISTCALL, [e_comercial])],
    "PARAMLISTCALL1": [Producao(PARAMLISTCALL1, [virgula, PARAMLISTCALL]), Producao(PARAMLISTCALL1, [e_comercial])],
    "PRINTSTAT": [Producao(PRINTSTAT, [print_, EXPRESSION])],
    "READSTAT": [Producao(READSTAT, [read, LVALUE])],
    "RETURNSTAT": [Producao(RETURNSTAT, [return_])],
    "IFSTAT": [Producao(IFSTAT, [if_, abre_parentese, EXPRESSION, fecha_parentese, abre_chave, STATELIST, fecha_chave, ELSESTAT])],
    "ELSESTAT": [Producao(ELSESTAT, [else_, abre_chave, STATELIST, fecha_chave]), Producao(ELSESTAT, [e_comercial])],
    "FORSTAT": [Producao(FORSTAT, [for_, abre_parentese, ATRIBSTAT, ponto_virgula, EXPRESSION, ponto_virgula, ATRIBSTAT, fecha_parentese, abre_chave, STATELIST, fecha_chave])],
    "STATELIST": [Producao(STATELIST, [STATEMENT, STATELIST1])],
    "STATELIST1": [Producao(STATELIST1, [STATELIST]), Producao(STATELIST1, [e_comercial])],
    "ALLOCEXPRESSION": [Producao(ALLOCEXPRESSION, [new, TYPE, NUMEXPRARRAY])],
    "NUMEXPRARRAY": [Producao(NUMEXPRARRAY, [abre_colchete, NUMEXPRESSION, fecha_colchete, NUMEXPRARRAY1])],
    "NUMEXPRARRAY1": [Producao(NUMEXPRARRAY1, [NUMEXPRARRAY]), Producao(NUMEXPRARRAY1, [e_comercial])],
    "RELOP": [Producao(RELOP, [menor]), Producao(RELOP, [maior]), Producao(RELOP, [menor_igual]), Producao(RELOP, [maior_igual]), Producao(RELOP, [igual_igual]), Producao(RELOP, [diferente])],
    "EXPRESSION": [Producao(EXPRESSION, [NUMEXPRESSION, EXPRESSION1])],
    "EXPRESSION1": [Producao(EXPRESSION1, [RELOP, NUMEXPRESSION]), Producao(EXPRESSION1, [e_comercial])],
    "SIGNAL": [Producao(SIGNAL, [mais]), Producao(SIGNAL, [menos])],
    "NUMEXPRESSION": [Producao(NUMEXPRESSION, [TERM, NUMEXPRESSION1])],
    "NUMEXPRESSION1": [Producao(NUMEXPRESSION1, [TERM_REC])],
    "TERM_REC": [Producao(TERM_REC, [SIGNAL, TERM, TERM_REC1]), Producao(TERM_REC, [e_comercial])],
    "TERM_REC1": [Producao(TERM_REC1, [TERM_REC])],
    "OPERATOR": [Producao(OPERATOR, [multiplicacao]), Producao(OPERATOR, [divisao]), Producao(OPERATOR, [modulo])],
    "TERM": [Producao(TERM, [UNARYEXPR, TERM1])],
    "TERM1": [Producao(TERM1, [UNARYEXPR_REC])],
    "UNARYEXPR_REC": [Producao(UNARYEXPR_REC, [OPERATOR, UNARYEXPR, UNARYEXPR_REC1]), Producao(UNARYEXPR_REC, [e_comercial])],
    "UNARYEXPR_REC1": [Producao(UNARYEXPR_REC1, [UNARYEXPR_REC])],
    "UNARYEXPR": [Producao(UNARYEXPR, [SIGNAL, FACTOR]), Producao(UNARYEXPR, [FACTOR])],
    "FACTOR": [
        Producao(FACTOR, [int_constant]),
        Producao(FACTOR, [float_constant]),
        Producao(FACTOR, [string_constant]),
        Producao(FACTOR, [null]),
        Producao(FACTOR, [LVALUE]),
        Producao(FACTOR, [abre_parentese, NUMEXPRESSION, fecha_parentese])
    ],
    "LVALUE": [Producao(LVALUE, [ident, LVALUE1])],
    "LVALUE1": [Producao(LVALUE1, [NUMEXPRESSION_REC])],
    "NUMEXPRESSION_REC": [Producao(NUMEXPRESSION_REC, [abre_colchete, NUMEXPRESSION, fecha_colchete, NUMEXPRESSION_REC1]), Producao(NUMEXPRESSION_REC, [e_comercial])],
    "NUMEXPRESSION_REC1": [Producao(NUMEXPRESSION_REC1, [NUMEXPRESSION_REC])]
}

terminais = ["{", "}", "break", ";", "int", "float", "string", "print", "read", "return", "if", "else", "for", "def", "ident", ",", "[", "]", "new", "run", "+", "-", "*", "/", "%", "int_constant", "float_constant", "string_constant", "null", "(", ")", "<", ">", "<=", ">=", "==", "!=", "=", "&"]
terminais.extend("$")
simbolo_inicial = PROGRAM

firsts = {
  'PROGRAM': ['{', 'break', ';', 'int', 'float', 'string', 'print', 'read', 'return', 'if', 'for', 'def', 'ident', '&'],
  'FUNCLIST': ['def'],
  'FUNCLIST1': ['def', '&'],
  'FUNCDEF': ['def'],
  "TYPE": ["int", "float", "string"],
  "PARAMLIST": ["int", "float", "string", "&"],
  "PARAMLIST1": [",", "&"],
  "STATEMENT": ["{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident"],
  "VARDECL": ["int", "float", "string"],
  "ARRAY_VARDECL": ["int", "float", "string"],  
  "ATRIBSTAT": ["ident"],
  "RVALUE": ["new", "run", "+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
  "FUNCCALL": ["run"],
  "PARAMLISTCALL": ["ident", "&"],
  "PARAMLISTCALL1": [",", "&"],
  "PRINTSTAT": ["print"],
  "READSTAT": ["read"],
  "RETURNSTAT": ["return"],
  "IFSTAT": ["if"],
  "ELSESTAT": ["else"],
  "FORSTAT": ["for"],
  "STATELIST": ["{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident"],
  "STATELIST1": ["{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident", "&"],
  "ALLOCEXPRESSION": ["new"],
  "NUMEXPRARRAY": ["["],
  "NUMEXPRARRAY1": ["[", "&"],
  "RELOP": ["<", ">", "<=", ">=", "==", "!="],
  "EXPRESSION": ["(", "+", "-", "int_constant", "float_constant", "string_constant", "null", "ident", "&"],
  "EXPRESSION1": ["<", ">", "<=", ">=", "==", "!=", "&"],
  "SIGNAL": ["+", "-"],
  "NUMEXPRESSION": ["+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
  "NUMEXPRESSION1": ["+", "-", "&"],
  "TERM_REC": ["+", "-", "&"],
  "TERM_REC1": ["+", "-", "&"],
  "OPERATOR": ["*", "/", "%"],
  "TERM": ["+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
  "TERM1": ["*", "/", "%", "&"],
  "UNARYEXPR_REC": ["*", "/", "%", "&"],
  "UNARYEXPR_REC1": ["*", "/", "%", "&"],
  "UNARYEXPR": ["+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
  "FACTOR": ["int_constant", "float_constant", "string_constant", "null", "(", "ident"],
  "LVALUE": ["ident"],
  "LVALUE1": ["[", "&"],
  "NUMEXPRESSION_REC": ["[", "&"],
  "NUMEXPRESSION_REC1": ["[", "&"]
}

follows = {
    "PROGRAM": ["$"],
    "FUNCLIST": ["$"],
    "FUNCLIST1": ["$"],
    "FUNCDEF": ["def", "$"],
    "TYPE": ["ident", "["],
    "PARAMLIST": [")"],
    "PARAMLIST1": [")"],
    "STATEMENT": ["}", "{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident", "$"],
    "VARDECL": [";"],
    "ARRAYINTCONST": [";"],    
    "ATRIBSTAT": [";", ")"],
    "RVALUE": [";", ")"],
    "FUNCCALL": [";", ")"],
    "PARAMLISTCALL": [")"],
    "PARAMLISTCALL1": [")"],
    "PRINTSTAT": [";"],
    "READSTAT": [";"],
    "RETURNSTAT": [";"],
    "IFSTAT": ["}", "{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident", "$"],
    "ELSESTAT": ["}", "{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident", "$"],
    "FORSTAT": ["}", "{", "break", ";", "int", "float", "string", "print", "read", "return", "if", "for", "ident", "$"],
    "STATELIST": ["}"],
    "STATELIST1": ["}"],
    "ALLOCEXPRESSION": [";", ")"],
    "NUMEXPRARRAY": [";", ")"],
    "NUMEXPRARRAY1": [";", ")"],
    "RELOP": ["+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
    "EXPRESSION": [";", ")"],
    "EXPRESSION1": [";", ")"],
    "SIGNAL": ["+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
    "NUMEXPRESSION": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!="],
    "NUMEXPRESSION1": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!="],
    "TERM_REC": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!="],
    "TERM_REC1": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!="],
    "OPERATOR": ["+", "-", "int_constant", "float_constant", "string_constant", "null", "(", "ident"],
    "TERM": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-"],
    "TERM1": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-"],
    "UNARYEXPR_REC": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-"],
    "UNARYEXPR_REC1": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-"],
    "UNARYEXPR": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-", "*", "/", "%"],
    "FACTOR": ["]", ";", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-", "*", "/", "%"],
    "LVALUE": ["=", ";", "]", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-", "*", "/", "%"],
    "LVALUE1": ["=", ";", "]", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-", "*", "/", "%"],
    "NUMEXPRESSION_REC": ["=", ";", "]", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-", "*", "/", "%"],
    "NUMEXPRESSION_REC1": ["=", ";", "]", ")", "<", ">", "<=", ">=", "==", "!=", "+", "-", "*", "/", "%"]
}
