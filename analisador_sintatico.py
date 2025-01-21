# Grupo: Cristian Alexandre Alchini, João Pedro Adami do Nascimento, Marcos Henrique Kogler, Victor do Valle Cunha 
# Modificações na linguagem:
#   Foi adicionada a palavra reservada 'run' na produção: FUNCCALL -> run ident(PARAMLISTCALL)

from gramatica import Acao_Semantica, Terminal, Variavel, Producao, simbolo_inicial, producoes, terminais, firsts, follows
from analisador_lexico import Token
import copy
from tabelaGlobal import tabela

def get_first_for_simbolo(simbolo):
    if isinstance(simbolo, Terminal):
      return [simbolo.nome]
    else:
      return firsts[simbolo.nome]

def get_first_for_producao(producao):
  firsts_producao = []
  for simbolo in producao:
    if not isinstance(simbolo, Acao_Semantica):
      firsts_producao.extend(get_first_for_simbolo(simbolo))
      if '&' not in firsts_producao:
        break
  return firsts_producao

# Constrói tabela de reconhecimento sintático
def constroi_tabela():
  tabela_as = {}

  for cabeca in producoes:
    tabela_as[cabeca] = {}
    for terminal in terminais:
      tabela_as[cabeca][terminal] = Producao(Variavel(cabeca), [])  # Produção com cauda vazia significa entrada de erro

  for cabeca in producoes:
    for producao in producoes[cabeca]:
      terminais_list = []
      terminais_list = get_first_for_producao(producao.cauda)
      if '&' in terminais_list:
        terminais_list.extend(follows[cabeca])
      
      if len(terminais_list) != len(set(terminais_list)):
        print("ERRO")
        exit(1)

      for terminal in terminais_list:
        tabela_as[cabeca][terminal] = producao
        #  tabela_as[cabeca][terminal] = ' '.join(producao)

  return tabela_as
    
# Realiza a análise sintática utilizando a tabela de reconhecimento sintático
def analisador_sintatico(tabela, entrada):
    entrada_ptr = 0
    
    # Símbolo de final de sentença    
    entrada.append(Token('$', '$'))
    
    pilha = []
    pilha.append(Terminal("$"))
    pilha.append(simbolo_inicial)

    while entrada_ptr < len(entrada):
        topo_da_pilha = pilha[-1]
        token = entrada[entrada_ptr]
        
        simbolo_cabecote = token.nome
        lexema = token.lexema

        if isinstance(topo_da_pilha, Acao_Semantica):
                acao = topo_da_pilha
                acao.funcao(acao.parametros)
                pilha.pop()

        elif isinstance(topo_da_pilha, Terminal) and topo_da_pilha.nome == simbolo_cabecote:        
            if simbolo_cabecote == '$':
                return True
            else:
                topo_da_pilha.vallex = lexema
                pilha.pop()
                entrada_ptr += 1
        elif isinstance(topo_da_pilha, Variavel):
            producao = tabela[topo_da_pilha.nome][simbolo_cabecote]            
            
            if (len(producao.cauda) == 0):  # Produção com cauda vazia significa entrada de erro                    
                raise ValueError(f"Erro sintático na linha {token.linha} coluna {token.coluna} .")
            
            pilha.pop()

            if producao.is_epsilon():        
                continue
            
            for simbolo in reversed(producao.cauda):
                pilha.append(simbolo)  # Cópia rasa, não há razão para cópia profunda

        
        else:  # Comportamento inesperado
            raise ValueError(f"Erro sintático na linha {token.linha} coluna {token.coluna} .")
    
    raise ValueError(f"Erro sintático!")
