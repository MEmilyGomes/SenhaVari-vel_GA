import random
from functools import partial
# import numpy as np

###############################################################################
#                                 Cria População                              #
###############################################################################
def gene_senha(letras_possiveis):
    """Sorteia uma letra.

    Args:
      letras: letras possíveis de serem sorteadas.

    """
    letra = random.choice(letras_possiveis)
    return letra

def cria_candidato_senha(tamanho_senha, letras_possiveis):
    """Cria um candidato para o problema da senha

    Args:
      tamanho_senha: inteiro representando o tamanho da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    candidato = []

    for _ in range(tamanho_senha):
        candidato.append(gene_senha(letras_possiveis))

    return candidato

def cria_candidato_senha_sv(letras_possiveis):
    """Cria um candidato para o problema da senha de tamanho variável
 
    Args:
      letras_possiveis: letras possíveis de serem sorteadas.
 
    """
    tamanho_senha = random.randint(1, 30)
   
    candidato = []
 
    for _ in range(tamanho_senha):
        candidato.append(gene_senha(letras_possiveis))
 
    return candidato

def populacao_senha(tamanho_populacao, letras_possiveis):
    """Cria população inicial no problema da senha variável

    Args
      tamanho_populacao: tamanho da população.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    populacao = []

    for _ in range(tamanho_populacao):
        populacao.append(cria_candidato_senha_sv(letras_possiveis))

    return populacao


###############################################################################
#                                Função Objetivo                              #
###############################################################################

def funcao_objetivo_senha_sv(candidato, senha_verdadeira, letras_possiveis):
    """Computa a funcao objetivo de um candidato no problema da senha 
    de tamanho variável

    Args:
      candidato: um palpite para a senha que você quer descobrir
      senha_verdadeira: a senha que você está tentando descobrir

    """
    distancia = 0
    
    menor_senha = min(len(candidato), len(senha_verdadeira))
    maior_senha = max(len(candidato), len(senha_verdadeira))
    
    diferenca_quant_letras = maior_senha - menor_senha


    for letra_candidato, letra_senha in zip(candidato, senha_verdadeira):
        num_letra_candidato = ord(letra_candidato)
        num_letra_senha = ord(letra_senha)
        distancia += abs(num_letra_candidato - num_letra_senha)
        
    adicional_distancia = diferenca_quant_letras * len(letras_possiveis)
    distancia += adicional_distancia

    return distancia

def funcao_objetivo_pop_senha_sv(populacao, senha_verdadeira, letras_possiveis):
    """Computa a funcao objetivo de uma populaçao no problema da senha
    de tamanho variável.

    Args:
      populacao: lista contendo os individuos do problema
      senha_verdadeira: a senha que você está tentando descobrir

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_senha_sv(individuo, senha_verdadeira, letras_possiveis))

    return fitness
###############################################################################
#                                 Seleção                                     #
###############################################################################

def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

    Args:
      populacao: lista contendo os individuos do problema
      fitness: lista contendo os valores computados da funcao objetivo
      tamanho_torneio: quantidade de invíduos que batalham entre si

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


###############################################################################
#                                  Cruzamento                                 #
###############################################################################
def cruzamento_ponto_simples_senha_sv(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto simples

    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento

    """
    tamanho_menor = min(len(pai), len(mae))

    if random.random() < chance_de_cruzamento and tamanho_menor > 2:
        corte = random.randint(1, tamanho_menor - 1)
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
        return filho1, filho2
    else:
        return pai, mae
    
def cruzamento_ponto_duplo(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto duplo

    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento

    """
    tamanho_menor = min(len(pai), len(mae))
    
    if random.random() < chance_de_cruzamento and tamanho_menor > 2:
        corte1 = random.randint(1, len(mae) - 2)
        corte2 = random.randint(corte1 + 1, len(mae) - 1)
        filho1 = pai[:corte1] + mae[corte1:corte2] + pai[corte2:]
        filho2 = mae[:corte1] + pai[corte1:corte2] + mae[corte2:]
        return filho1, filho2
    else:
        return pai, mae

    
    
###############################################################################
#                                Mutação                                      #
###############################################################################
def mutacao_salto(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([ 36, 26, 10, 1, -1, -10, -26, -36])
            indice_letra %= len(valores_possiveis)
            individuo[gene] = valores_possiveis[indice_letra]
            
def mutacao_insercao_delecao(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza inserção ou deleção de um gene

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for i, individuo in enumerate(populacao):
        if random.random() < chance_de_mutacao:
            forma_mutacao = random.choices(["insercao", "delecao"])
            if forma_mutacao[0] == "insercao":
                quant_max = 30 - len(individuo) 
                if quant_max != 0:
    
                    tamanho_insercao = random.randint(1, quant_max)
                    insercao = cria_candidato_senha(tamanho_insercao, valores_possiveis)
                    individuo = individuo.extend(insercao)
            elif forma_mutacao[0] == "delecao": 
                if len(individuo) > 2:
                    nos = random.sample(range(1, len(individuo)), k=2)
                    nos = sorted(nos)
                    populacao[i] = individuo[nos[0]:nos[1]]