# Grupo: Cristian Alexandre Alchini, João Pedro Adami do Nascimento, Marcos Henrique Kogler, Victor do Valle Cunha 
# Modificações na linguagem:
#   Foi adicionada a palavra reservada 'run' na produção: FUNCCALL -> run ident(PARAMLISTCALL)

from analisador_lexico import AnalisadorLexico
from analisador_sintatico import constroi_tabela, analisador_sintatico
from tabelaGlobal import tabela

print("Trabalho Final de INE5426\n\nGrupo:\nCristian Alexandre Alchini\nJoão Pedro Adami do Nascimento\nMarcos Henrique Kogler\nVictor do Valle Cunha\n")


arquivo_fonte = input('Digite o caminho para o arquivo à ser compilado: ')
if len(arquivo_fonte) == 0:
    arquivo_fonte = 'exemplos/calc_geometria.convcc'

print("\nIniciando compilação...\n")
al = AnalisadorLexico(arquivo_fonte, tabela)
al.processa_arquivo()

tabelaLL1 = constroi_tabela()
pertence_a_gramatica = analisador_sintatico(tabelaLL1, al.tokens)
tabela.exibe_tabela()

if pertence_a_gramatica:
    print(f"\nAnálise sintática obteve sucesso!\n\nA palavra pertence à linguagem gerada por esta gramática!")
else:
    print(f"\nErro durante a análise sintática.\n\nA palavra não pertence à linguagem gerada por esta gramática.")