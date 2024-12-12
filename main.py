import tkinter as tk
 
# Singleton - Para controlar o estado do jogo
class Jogo:
    _instance = None  # A variável de classe que vai armazenar a instância única
 
    def __new__(cls):
        if cls._instance is None:
            # Garantindo que apenas uma instância de Jogo será criada
            cls._instance = super(Jogo, cls).__new__(cls)
            cls._instance.tabuleiro = cls.criar_tabuleiro()  # Criar o tabuleiro
            cls._instance.vez = 1  # Definir quem começa a jogar
            cls._instance.damas = {'P1': [], 'P2': []}  # Listas de peças damas para cada jogador
        return cls._instance  # Retorna a instância única do jogo
 
    @staticmethod
    def criar_tabuleiro():
        # Factory Method: cria e retorna o tabuleiro do jogo
        tabuleiro = [['' for _ in range(8)] for _ in range(8)]  # Inicializa o tabuleiro vazio
        for linha in range(3):  # Coloca as peças do jogador P1
            for coluna in range(8):
                if (linha + coluna) % 2 == 1:
                    tabuleiro[linha][coluna] = 'P1'
        for linha in range(5, 8):  # Coloca as peças do jogador P2
            for coluna in range(8):
                if (linha + coluna) % 2 == 1:
                    tabuleiro[linha][coluna] = 'P2'
        return tabuleiro  # Retorna o tabuleiro configurado
 
    def mover_peca(self, origem, destino):
        x1, y1 = origem
        x2, y2 = destino
        peca = self.tabuleiro[x1][y1]
 
        # Verifica se o movimento é uma captura
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
            x_meio, y_meio = (x1 + x2) // 2, (y1 + y2) // 2
            self.tabuleiro[x_meio][y_meio] = ''  # Elimina a peça adversária
 
        # Realiza o movimento
        self.tabuleiro[x2][y2] = peca
        self.tabuleiro[x1][y1] = ''
 
        # Verifica se a peça atingiu a última linha para virar dama
        if peca == "P1" and x2 == 0:
            self.tabuleiro[x2][y2] = 'D1'  # P1 vira dama
            self.damas['P1'].append((x2, y2))
        elif peca == "P2" and x2 == 7:
            self.tabuleiro[x2][y2] = 'D2'  # P2 vira dama
            self.damas['P2'].append((x2, y2))
 
        # Alterna a vez do jogador
        self.alternar_vez()
 
    def alternar_vez(self):
        self.vez = 1 if self.vez == 2 else 2  # Alterna entre os jogadores 1 e 2
 
    def capturas_possiveis(self, jogador):
        capturas = []
        for x in range(8):
            for y in range(8):
                if self.tabuleiro[x][y] == jogador:
                    capturas += self.opcoes_de_captura((x, y))  # Chama as opções de captura para cada peça
        return capturas
 
    def opcoes_de_captura(self, origem):
        x1, y1 = origem
        peca = self.tabuleiro[x1][y1]
        capturas = []
 
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Direções para movimentos de captura
        for dx, dy in direcoes:
            x2, y2 = x1 + dx, y1 + dy
            x3, y3 = x1 + 2*dx, y1 + 2*dy
            if 0 <= x3 < 8 and 0 <= y3 < 8:
                if (0 <= x2 < 8 and 0 <= y2 < 8 and
                    self.tabuleiro[x2][y2] != '' and
                    self.tabuleiro[x2][y2] != peca and
                    self.tabuleiro[x3][y3] == ''):
                    capturas.append((x3, y3))  # Adiciona a captura possível
 
        return capturas
 
    def tem_captura(self):
        # Verifica se existe captura possível para o jogador atual
        return len(self.capturas_possiveis('P1' if self.vez == 1 else 'P2')) > 0
 
 
class TabuleiroVisual:
    def __init__(self, jogo, canvas):
        self.jogo = jogo
        self.canvas = canvas
        self.pecas = {}
        self.criar_interface()
 
    def criar_interface(self):
        # Cria a interface gráfica do tabuleiro e posiciona as peças
        for linha in range(8):
            for coluna in range(8):
                x1, y1 = coluna * 60, linha * 60
                x2, y2 = x1 + 60, y1 + 60
                cor = "white" if (linha + coluna) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor)
                if self.jogo.tabuleiro[linha][coluna] == "P1":
                    self.desenhar_peca(x1, y1, "white")
                elif self.jogo.tabuleiro[linha][coluna] == "P2":
                    self.desenhar_peca(x1, y1, "black")
                elif self.jogo.tabuleiro[linha][coluna] == "D1":
                    self.desenhar_peca(x1, y1, "white", True)
                elif self.jogo.tabuleiro[linha][coluna] == "D2":
                    self.desenhar_peca(x1, y1, "black", True)
 
        # Exibe de quem é a vez
        self.exibir_vez()
 
    def desenhar_peca(self, x, y, cor, dama=False):
        # Desenha as peças no tabuleiro, incluindo as damas
        self.canvas.create_oval(x + 10, y + 10, x + 50, y + 50, fill=cor, outline="white")
        if dama:
            self.canvas.create_text(x + 30, y + 30, text="D", font=("Helvetica", 16), fill="white")
 
    def exibir_vez(self):
        # Exibe na tela de quem é a vez (Jogador 1 ou Jogador 2)
        jogador = "Jogador 1 (Vermelho)" if self.jogo.vez == 1 else "Jogador 2 (Azul)"
        self.canvas.create_text(240, 480, text=f"É a vez de: {jogador}", font=("Helvetica", 16), fill="black")
 
    def atualizar(self):
        # Atualiza a interface gráfica do tabuleiro
        self.canvas.delete("all")
        self.criar_interface()
 
 
class JogoDamasVisual:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jogo de Damas")
        self.canvas = tk.Canvas(self.root, width=480, height=520)  # Aumentei a altura para caber o texto
        self.canvas.pack()
        self.jogo = Jogo()  # A classe Jogo já garante que só há uma instância
        self.tabuleiro_visual = TabuleiroVisual(self.jogo, self.canvas)  # Instancia a interface visual
        self.tabuleiro_visual.atualizar()
        self.peca_selecionada = None
        self.opcoes_movimento = []
 
        self.canvas.bind("<Button-1>", self.selecionar_peca)  # Associa a ação de clicar para selecionar peça
 
    def selecionar_peca(self, event):
        coluna = event.x // 60
        linha = event.y // 60
 
        if self.peca_selecionada is None:
            if (linha + coluna) % 2 == 1 and self.jogo.tabuleiro[linha][coluna]:
                peca = self.jogo.tabuleiro[linha][coluna]
                if (peca == "P1" and self.jogo.vez == 1) or (peca == "P2" and self.jogo.vez == 2):
                    self.peca_selecionada = (linha, coluna)
                    self.mostrar_opcoes_movimento()  # Exibe as opções de movimento
        else:
            destino = (linha, coluna)
            if destino in self.opcoes_movimento:
                self.mover_peca(self.peca_selecionada, destino)
            self.limpar_opcoes_movimento()
            self.peca_selecionada = None
 
    def mostrar_opcoes_movimento(self):
        # Exibe as opções de movimento ou captura para a peça selecionada
        x, y = self.peca_selecionada
        self.opcoes_movimento = []
 
        # Se o jogador tem capturas possíveis, mostra as opções de captura
        capturas = self.jogo.capturas_possiveis("P1" if self.jogo.vez == 1 else "P2")
        if capturas:
            for captura in capturas:
                x1, y1 = captura[1] * 60, captura[0] * 60
                x2, y2 = x1 + 60, y1 + 60
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="orange")
                self.opcoes_movimento.append(captura)
        else:
            # Senão, apenas mostra os movimentos normais
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and not self.jogo.tabuleiro[nx][ny]:
                    self.opcoes_movimento.append((nx, ny))
                    x1, y1 = ny * 60, nx * 60
                    x2, y2 = x1 + 60, y1 + 60
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="yellow")
 
    def limpar_opcoes_movimento(self):
        # Limpa as opções de movimento mostradas
        self.opcoes_movimento = []
        self.tabuleiro_visual.atualizar()
 
    def mover_peca(self, origem, destino):
        # Move a peça e atualiza a interface
        self.jogo.mover_peca(origem, destino)
        self.tabuleiro_visual.atualizar()
 
    def iniciar(self):
        self.root.mainloop()  # Inicia a interface gráfica
 
if __name__ == "__main__":
    jogo_visual = JogoDamasVisual()
    jogo_visual.iniciar()  # Inicia o jogo