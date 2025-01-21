# Grupo: Cristian Alexandre Alchini, João Pedro Adami do Nascimento, Marcos Henrique Kogler, Victor do Valle Cunha 
# Modificações na linguagem:
#   Foi adicionada a palavra reservada 'run' na produção: FUNCCALL -> run ident(PARAMLISTCALL)

class NodoTabelaDeSimbolos:
    def __init__(self, pai=None):
        self.tabela = {}  # Dicionário de símbolos no escopo atual
        self.pai = pai  # Referência para o escopo pai

    def _adiciona(self, name, linha, coluna):
        """Declara um identificador no escopo atual.

        Args:
            name (str): Nome do identificador.
            type (str): Tipo do identificador ('int', 'string', 'function', etc.).

        Raises:
            ValueError: Se o identificador já foi declarado no escopo atual.
        """
        if name in self.tabela:
            self.tabela[name].linhas_colunas.append((linha, coluna))
        else:
            self.tabela[name] = ElementoTabelaDeSimbolos(name, (linha, coluna))

    def lookup(self, name):
        """Procura um identificador no escopo atual e nos escopos ancestrais.

        Args:
            name (str): Nome do identificador.

        Returns:
            str or None: O tipo do identificador, ou None se não for encontrado.
        """
        if name in self.tabela:
            return self.tabela[name]
        if self.pai:
            return self.pai.lookup(name)
        return None
    
    def _exibe_tabela(self):
      print("\nTabela de símbolos:")
      print(f"| {'Identificador':35} | {'Tipo':10} | {'Linha e Coluna':5} ")
      print(f"|{'-'*37}|{'-'*12}|{'-'*37}")
      
      for identificador, elemento in self.tabela.items():
        print(f"| {identificador:35} | {elemento.tipo:10} |  {', '.join(str(x) for x in elemento.linhas_colunas):5} ")
    
class ElementoTabelaDeSimbolos:
    def __init__(self, identificador, lc, tipo=None):
        self.identificador = identificador  
        self.linhas_colunas = [lc]
        self.tipo = "Sem tipo"

class TabelaDeSimbolos:
    def __init__(self):
        self.current_scope = NodoTabelaDeSimbolos()  # Começa com o escopo global

    def push_scope(self):
        """Cria um novo escopo aninhado."""
        self.current_scope = NodoTabelaDeSimbolos(pai=self.current_scope)

    def pop_scope(self):
        """Sai do escopo atual e retorna ao escopo pai."""
        if self.current_scope.pai is not None:
            self.current_scope = self.current_scope.pai
        else:
            raise RuntimeError("Cannot exit global scope")

    def adiciona(self, name, linha, coluna):
        """Declara um identificador no escopo atual."""
        self.current_scope._adiciona(name, linha, coluna)
    

    def lookup(self, name):
        """Procura um identificador nos escopos."""
        return self.current_scope.lookup(name)

    def adiciona_tipo(self, name, tipo):
        self.current_scope.tabela[name].tipo = tipo

    def exibe_tabela(self):
        """Procura um identificador nos escopos."""
        return self.current_scope._exibe_tabela()

