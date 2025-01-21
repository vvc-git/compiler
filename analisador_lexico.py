# Grupo: Cristian Alexandre Alchini, João Pedro Adami do Nascimento, Marcos Henrique Kogler, Victor do Valle Cunha 
# Modificações na linguagem:
#   Foi adicionada a palavra reservada 'run' na produção: FUNCCALL -> run ident(PARAMLISTCALL)

from tabela_de_simbolos import TabelaDeSimbolos

class Token:
    def __init__(self, nome, lexema, linha=None, coluna=None):
        self.nome = nome  # Nome do token, ex: 'int', 'ident', 'if', etc.
        self.lexema = lexema  # lexema literal do token, ex: '10', 'x', '+', etc.
        self.linha = linha  # Linha no código onde o token foi encontrado
        self.coluna = coluna  # Coluna na linha onde o token foi encontrado

    def __repr__(self):
        return f"Token(nome='{self.nome}', valor='{self.valor}', linha={self.linha}, coluna={self.coluna})"

class AnalisadorLexico:
    def __init__(self, caminho_arquivo, tabela_simbolos):
        self.caminho_arquivo = caminho_arquivo
        self.tokens = []
        self.tabela_de_simbolos = tabela_simbolos
        self.relop = ['>', '<',  '=', "!"]
        self.lista_palavras_reservadas = ['def', 'if', 'return', 'run', 'print', 'read', 'return', 'new', 'null', 'break', 'else', 'for', 'null']
        self.type = ['int', 'float', 'string']
        # selfReferencingToken
        self.signal = ['+', '-']
        self.operator = ['*', '/', '=', '%']
        self.escope = ['(', ')', '{', '}', '[', ']']
        self.end = [';']
        self.parameter_separetor = [',']
        self.current_line_count = 1
        self.current_column_count = 1
        self.largura_tabulacao = 4

    def _volta_um_caracter(self, arquivo):
       self.current_column_count -= 1
       arquivo.seek(arquivo.tell() - 1)
       

    def _le_um_caracter(self, arquivo):
      self.current_column_count += 1
      return arquivo.read(1)      

     # Cria um token de identificador
    def _create_identifier_or_type_token(self, arquivo, c):
      coluna_inicio_token = self.current_column_count - 1
      state = 4
      lexema = []

      while (True):
        match state:
          case 4:
            if c.isalpha() or c == '_':
              state = 5
              lexema.append(c)
            else:
              return False
          case 5:
            c = self._le_um_caracter(arquivo)
            if c.isalpha() or c == '_' or c.isdigit():
              state = 5
              lexema.append(c)
            else:
              state = 6
          case 6:
            if "".join(lexema) in (self.type + self.lista_palavras_reservadas):
              self.tokens.append(Token("".join(lexema), "".join(lexema), self.current_line_count, coluna_inicio_token))
            else:
              self.tokens.append(Token("ident", "".join(lexema), self.current_line_count, coluna_inicio_token))
              self.tabela_de_simbolos.adiciona("".join(lexema), self.current_line_count, coluna_inicio_token)
            self._volta_um_caracter(arquivo)
            return True

     # Cria um token numérico
    def _create_numeric_token(self, arquivo, c):
      coluna_inicio_token = self.current_column_count - 1

      state = 7
      lexema = []
      while (True):
        match state:
          case 7:            
            if c.isdigit():
              state = 8
              lexema.append(c)              
            else:
              return False
          case 8:
            c = self._le_um_caracter(arquivo)
            if c.isdigit():
              state = 8
              # Se mantem como inteiro
              lexema.append(c)
            elif c == ".":
              # é um float
              lexema.append(c)
              state = 10
            else:
              state = 9
          case 9: 
            self.tokens.append(Token("int_constant", "".join(lexema), self.current_line_count, coluna_inicio_token))
            self._volta_um_caracter(arquivo)
            return True
          case 10:
            c = self._le_um_caracter(arquivo)
            if c.isdigit():
              state = 10
              lexema.append(c)
            else:
              state = 11
          case 11: 
            self.tokens.append(Token("float_constant", "".join(lexema), self.current_line_count, coluna_inicio_token))
            self._volta_um_caracter(arquivo)
            return True
    
    # Cria um token para constante string
    def _create_string_constant_token(self, arquivo, c):
      coluna_inicio_token = self.current_column_count - 1
      state = 12
      lexema = []

      while (True):
        match state:
          case 12:
            if  c == '"':
              state = 13
              lexema.append(c)
            elif  c == "'":
              state = 14
              lexema.append(c)          
          case 13:
            c = self._le_um_caracter(arquivo)            
            if  c == '"':
              state = 15
              lexema.append(c)
            elif c == '\n':
              return False
            else:
              state = 13
              lexema.append(c)
          case 14:
            c = self._le_um_caracter(arquivo)
            if  c == "'":
              state = 15
              lexema.append(c)
            elif c == '\n':
              return False
            else:
              state = 14
              lexema.append(c)              
          case 15:
            self.tokens.append(Token("string_constant", "".join(lexema), self.current_line_count, coluna_inicio_token))
            return True                        
    
    # Cria um token para operações relacionais
    def _create_relop_token(self, arquivo, c):
      coluna_inicio_token = self.current_column_count - 1
      state = 0
      lexema = []

      while (True):
        match state:
          case 0:
            if c in ['>', '<', '=', "!"]:
              state = 1
              lexema.append(c)
            else:
              return False
          case 1:
            c = self._le_um_caracter(arquivo)
            if c == '=':
              state = 2
              lexema.append(c)
            else:
               state = 3
          case 2:
            self.tokens.append(Token("".join(lexema), "".join(lexema), self.current_line_count, coluna_inicio_token))
            return True
          case 3:
            self.tokens.append(Token("".join(lexema), "".join(lexema), self.current_line_count, coluna_inicio_token))
            self._volta_um_caracter(arquivo)
            return True
        

    # Cria um token para os elementos que eles próprios são os tokens
    def _self_referencing_token(self, c):      
      self.tokens.append(Token("".join(c), "".join(c), self.current_line_count, self.current_column_count))    
        
    # Processa o arquivo caractere por caractere
    def processa_arquivo(self):
      with open(self.caminho_arquivo, 'r') as arquivo:          
          while True:
              c = arquivo.read(1)   

              if not c:  # Fim do arquivo
                  break
              
              if c == '\n':
                self.current_line_count += 1
                self.current_column_count = 1
              
              elif c == '\t':
                self.current_column_count += self.largura_tabulacao
              
              else:
                 self.current_column_count += 1
                          
              # Ignora espaços em branco
              if c.isspace():
                  continue

              # Verifica tipos de tokens
              if c.isalpha() or c == '_':  # Identificadores
                  if not self._create_identifier_or_type_token(arquivo, c):
                    raise ValueError(f"Erro léxico na linha {self.current_line_count}: Não foi possível processar identificador.")
              
              elif c.isdigit():
                  if not self._create_numeric_token(arquivo, c):
                    raise ValueError(f"Erro léxico na linha {self.current_line_count}: Não foi possível processar valor numérico.")
              
              elif c in ['"', "'"]:
                if not self._create_string_constant_token(arquivo, c):
                  raise ValueError(f"Erro léxico na linha {self.current_line_count}: Não foi possível processar o constante string.")
              
              elif c in self.relop:
                if not self._create_relop_token(arquivo, c):
                  raise ValueError(f"Erro léxico na linha {self.current_line_count}: Não foi possível processar o relop.")
              
              elif c in self.signal + self.operator + self.escope + self.end + self.parameter_separetor:
                self._self_referencing_token(c)                
              
              else:  # Outros caracteres
                raise ValueError(f"Erro léxico na linha {self.current_line_count}: Caractere inválido '{c}' encontrado.")
          
          print("Análise léxica obteve sucesso!\n")   

    # Exibe os resultados
    def exibe_tokens(self):
      print("\nTokens encontrados:")
      print(f"| {'Lexema':23} | {'Token':23} | {'Linha':5} |{'Coluna':5} |")
      print(f"|{'-'*25}|{'-'*25}|{'-'*7}|{'-'*7}|")

      for token in self.tokens:
        print(f"| {token.lexema:23} | {token.nome:23} | {token.linha:23} | {token.coluna:23} |")   
