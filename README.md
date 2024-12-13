
# Jogo de Damas

## O que foi feito
Este é um jogo de Damas implementado utilizando Python e a biblioteca Tkinter para a interface gráfica. O jogo segue as regras tradicionais de Damas e permite que dois jogadores joguem alternadamente. O objetivo é capturar as peças do adversário ou bloquear seus movimentos, fazendo com que o oponente não tenha mais jogadas possíveis.

## Como executar
1. Clone o repositório para o seu computador:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. Instale a biblioteca Tkinter, caso não tenha:
   ```bash
   pip install tk
   ```
3. Execute o script `jogo_damas.py`:
   ```bash
   python jogo_damas.py
   ```
   A janela do jogo será aberta e você poderá começar a jogar.

## Padrões de Projeto Utilizados

1. **Singleton**: Garantiu que o jogo tenha apenas uma instância do estado do jogo, controlando as peças e as jogadas. A classe `Jogo` implementa esse padrão, sendo responsável por controlar o fluxo do jogo e garantir que não existam múltiplas instâncias dessa classe.

2. **Factory Method**: A criação do tabuleiro é feita através do método `criar_tabuleiro`, que é responsável por configurar as peças e o layout inicial do tabuleiro de Damas.

3. **Observer**: A interface gráfica foi projetada para "observar" o estado do jogo. Sempre que o estado do jogo muda (como após uma peça ser movida ou capturada), a interface é atualizada automaticamente para refletir as mudanças.

4. **Command**: O padrão Command é utilizado ao armazenar as ações dos jogadores (mover peças ou realizar capturas). Cada ação é encapsulada em um comando que pode ser executado ou desfeito (não implementado no código, mas a estrutura permite essa expansão).

5. **Strategy**: O jogo adota a estratégia de movimentação e captura. As opções de movimento e captura para cada peça dependem da estratégia do jogador e da posição da peça no tabuleiro.

## Autor
Julia de Lima e Valentina Leite

## Link do vídeo
https://youtu.be/BJUKdwCYCJk
