<div align="center">
  <img src="Imagens/logo_Ilum-CNPEM.png" alt="Descrição da imagem" width="1000"/>
</div>

<h1 align="center"> A senha de tamanho variável 🕵️‍♀️:</h1>
<h2 align="center">Encontrando a senha com algoritmo genético</h2>

<p align="center"><strong>Autoras:</strong>Júlia Guedes A. dos Santos e Maria Emily Nayla Gomes da Silva</p>
<p align="center"><strong>Orientador:</strong> Prof. Dr. Daniel R. Cassar</p>


<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>


## 📝 Descrição
<p align="justify">
Os algoritmos genétivos são baseados em conceitos biológicos, como seleção natural e genético, com o objetico de direcionar a busca para regiões de melhor performance em um espaço de soluções e resolver problemas de otimização <a href="#ref1"><sup>1</sup></a>. Neste trabalho, resolvemos o problema de encontrar senhas de tamanho variável utilizando um algoritmo genético. Ou seja, a função que gera cada indivíduo da população não conhece o tamanho exato da senha, apenas que este varia entre 1 e 30 caracteres — compostos por letras minúsculas, letras maiúsculas e dígitos numéricos. Nesse contexto, para que o algoritmo encontre a senha correta, é necessário que ele consiga inferir que indivíduos com tamanhos diferentes estão mais distantes da solução ideal. Para isso, a função objetivo aplica uma penalização proporcional à diferença entre o tamanho dos indivíduos e o da senha correta.
</p>


## 📔 Notebooks e arquivos do projeto
* `ATP - 4.9 A senha de tamanho variável.ipynb`: Notebook principal que implementa um algoritmo genético para resolver o problema da senha variável.
* `funcoes_sv.py`: Script das funções do notebook. 

## 🎢 Modificando a Função Objetivo
<p align="justify">
  O código de algoritmo genético foi desenvolvido para resolver um problema de minimização: encontrar a senha correta. Para isso, foi necessário modificar a função objetivo, ajustando a forma como o fitness é calculado para cada indivíduo. Isso porque desejamos avaliar não apenas a distância entre os caracteres das senhas, mas também a diferença entre os seus tamanhos. Em relação ao tamanho, aplicamos uma penalização proporcional ao produto da diferença entre o tamanho da senha correta e o tamanho representado por um indivíduo, pelo total de possibilidades de caracteres.
</p>

  
````Python
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
````

## 🐇 Criando uma nova função de mutação
<p align="justify">
Para tentar fazer o código convergir mais rapidamente, implementamos mais um tipo de função de mutação: a <code>mutacao_insercao_delecao</code>. Como ocorre com outras mutações, ela só será executada se o valor sorteado por <code>random.random</code> for menor que a chance de mutação. Caso isso ocorra, a função irá sortear entre as opções "inserção" e "deleção". No caso da inserção, um ou mais genes são adicionados de modo que o indivíduo atinja, no máximo, 30 genes. Já no caso da deleção, dois valores são sorteados, e os genes são removidos antes do menor valor e após o maior.
</p>


````Python
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
                    populacao[i] = individuo[nos[0]:nos[1]
````

## 🔢 Resultados obtidos
<p align="center">
  <img src="Imagens/histograma.png" width="600" alt="Gráfico de exemplo">
</p>
<p align="justify">
Ao final dos experimentos, observou-se que 151 testes não convergiram para a solução correta. Esse resultado está relacionado à natureza não determinística dos algoritmos genéticos: como se baseiam em operações aleatórias e estocásticas, eles nem sempre conseguem encontrar a solução ideal para um dado problema. No presente caso, o critério de parada adotado foi estritamente o acerto da senha. Portanto, é possível que alguns testes tenham ficado presos em mínimos locais, onde as soluções candidatas se aproximaram da senha correta, mas não o suficiente para atingi-la exatamente — ou que simplesmente exigiriam mais gerações do que o limite estabelecido para convergência.
</p>
<p align="justify">
A partir do histograma, é possível concluir que a maior parte dos testes convergiram antes das 100 gerações, estando a distribuição centrada próxima a 90. Isso pode sinalizar que o algoritmo está bem otimizado e é capaz de encontrar, na majoritária parcela dos testes, a solução para o problema da senha em poucas gerações (considerando a complexidade do espaço de busca).
</p>

## 😁 Conclusão
<p align= "justify">
Em resumo, as modificações realizadas nas funções de criação da população e de avaliação do fitness mostraram-se eficazes para a resolução do problema da senha variável. Dos 1000 testes realizados, apenas 15% não convergiram dentro do limite de gerações estabelecido, indicando um bom desempenho do algoritmo mesmo diante da maior complexidade imposta pela variação do comprimento das senhas.
</p>

<p align= "justify">
Como principal contribuição criativa, destaca-se a implementação da função de mutação por deleção ou inserção, inspirada em processos biológicos homônimos. Essa função permite a remoção ou introdução de genes, proporcionando ao algoritmo maior flexibilidade para explorar soluções com diferentes comprimentos, o que é essencial para esse tipo de problema.
</p>

<p align= "justify">
Por fim, a análise das distribuições dos resultados evidenciou a natureza probabilística dos algoritmos genéticos. Embora geralmente consigam encontrar soluções próximas da ótima, esses algoritmos não garantem a convergência para a melhor solução em todos os casos, especialmente quando sujeitos a espaços de busca grandes ou com múltiplos ótimos locais. Ainda assim, os bons resultados obtidos comprovam a eficácia desses algoritmos para a resolução desse tipo de problema.
</p>

## 🖇️ Informações técnicas
* Linguagem de programação: `Python 3.9`
* Software:  `Jupyter Notebook`
* **Bibliotecas e Módulos:** `torch`, `torchvision`, `torchvision.datasets`, `torchvision.transforms`, `torch.utils.data.random_split`, `torch.utils.data.DataLoader`, `torch.nn`, `torch.nn.functional`, `torch.optim`, `matplotlib.pyplot`, `os`, `random`

<!-- Referencias lindinhas -->
<h2 id="ref1">👩‍🦳 Referências</h2>
<p>
1. <a href="https://www.geeksforgeeks.org/genetic-algorithms/" target="_blank"> GeeksforGeeks - Genetic Algorithms
  </a>
</p>


## 🧠 Contribuições dos Colaboradores
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/172424779?v=4" width=115><br><sub>Julia Guedes A. Santos</sub>](https://github.com/JuliaGuedesASantos)<br> [<sub>Ilum - CNPEM</sub>](https://ilum.cnpem.br/)<br> [<sub>Currículo Lattes</sub>](https://lattes.cnpq.br/9504021537643847)<br> [<sub>Linkedin</sub>](https://www.linkedin.com/in/j%C3%BAlia-guedes-546542283/) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/172424897?v=4" width=115><br><sub> Maria Emily Nayla</sub>](https://github.com/MEmilyGomes)<br> [<sub>Ilum - CNPEM</sub>](https://ilum.cnpem.br/)<br> [<sub>Currículo Lattes</sub>](http://lattes.cnpq.br/9482558334105708)<br> | [<img loading="lazy" src="https://github.com/user-attachments/assets/463d4753-7fa4-4a42-aa54-409e4150bb51" width=115><br> <sub> Prof. Dr. Daniel R. Cassar </sub>](https://github.com/drcassar)<br> [<sub>Ilum - CNPEM</sub>](https://ilum.cnpem.br/)<br> [<sub>Currículo Lattes</sub>](http://lattes.cnpq.br/1717397276752482) | 
| :---: | :---: | :---: | 

#### Para o Projeto:
* Júlia Guedes: Ajustou a função objetivo para resolver um problema de minimização e implementou uma nova função de mutação, a mutacao_insercao_delecao.
* Emily Gomes: Ajustou a função objetivo para resolver um problema de minimização e implementou uma nova função de mutação, a mutacao_insercao_delecao.

#### Para o Repositório GitHub:
* Júlia Guedes: README.
* Emily Gomes: README.

**Orientação:** Prof. Dr. Daniel R. Cassar.
