# Definir o interpretador Python
PYTHON = python3.10

# Nome do arquivo principal
MAIN = main.py

# Rodar o código Python
run:
	$(PYTHON) $(MAIN)


# Exibir ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make run       - Executa o programa"	
