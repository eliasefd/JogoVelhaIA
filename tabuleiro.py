# -*- coding: utf-8 -*-

class Tabuleiro:
    DESCONHECIDO = 0
    JOGADOR_0 = 1
    JOGADOR_X = 4

    def __init__(self):
        self.matriz = [ [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO], 
                        [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO],
                        [Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO, Tabuleiro.DESCONHECIDO]]
       
    def tem_campeao(self):
        """
        Verifica se há um campeão no jogo
        Retorna JOGADOR_0, JOGADOR_X ou DESCONHECIDO
        """
        # Verifica linhas
        for linha in range(3):
            if (self.matriz[linha][0] == self.matriz[linha][1] == self.matriz[linha][2] 
                and self.matriz[linha][0] != Tabuleiro.DESCONHECIDO):
                return self.matriz[linha][0]
        
        # Verifica colunas
        for col in range(3):
            if (self.matriz[0][col] == self.matriz[1][col] == self.matriz[2][col] 
                and self.matriz[0][col] != Tabuleiro.DESCONHECIDO):
                return self.matriz[0][col]
        
        # Verifica diagonal principal (0,0) -> (2,2)
        if (self.matriz[0][0] == self.matriz[1][1] == self.matriz[2][2] 
            and self.matriz[0][0] != Tabuleiro.DESCONHECIDO):
            return self.matriz[0][0]
        
        # Verifica diagonal secundária (0,2) -> (2,0)
        if (self.matriz[0][2] == self.matriz[1][1] == self.matriz[2][0] 
            and self.matriz[0][2] != Tabuleiro.DESCONHECIDO):
            return self.matriz[0][2]
        
        # Nenhum campeão encontrado
        return Tabuleiro.DESCONHECIDO