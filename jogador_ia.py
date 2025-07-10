# -*- coding: utf-8 -*-
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)
        self.oponente = Tabuleiro.JOGADOR_X if tipo == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0

    def getJogada(self) -> (int, int):
        """
        Sistema especialista com regras na ordem:
        R1. Ganhar ou bloquear (duas em sequência)
        R2. Criar duas sequências de duas marcações
        R3. Marcar centro se livre
        R4. Marcar canto oposto se oponente marcou canto
        R5. Marcar canto vazio
        R6. Marcar qualquer posição vazia
        """
        
        # R1: Ganhar ou bloquear (duas em sequência)
        jogada = self.regra1_ganhar_ou_bloquear()
        if jogada:
            return jogada
            
        # R2: Criar duas sequências de duas marcações
        jogada = self.regra2_criar_duas_sequencias()
        if jogada:
            return jogada
            
        # R3: Marcar centro se livre
        jogada = self.regra3_marcar_centro()
        if jogada:
            return jogada
            
        # R4: Marcar canto oposto
        jogada = self.regra4_canto_oposto()
        if jogada:
            return jogada
            
        # R5: Marcar canto vazio
        jogada = self.regra5_canto_vazio()
        if jogada:
            return jogada
            
        # R6: Marcar qualquer posição vazia
        return self.regra6_posicao_vazia()

    def regra1_ganhar_ou_bloquear(self):
        """
        R1: Se você ou seu oponente tiver duas marcações em sequência, marque o quadrado restante.
        Prioridade: primeiro tenta ganhar, depois bloquear
        """
        # Primeiro tenta ganhar
        jogada = self.encontrar_duas_em_sequencia(self.tipo)
        if jogada:
            return jogada
            
        # Depois tenta bloquear o oponente
        jogada = self.encontrar_duas_em_sequencia(self.oponente)
        if jogada:
            return jogada
            
        return None

    def encontrar_duas_em_sequencia(self, jogador):
        """
        Encontra uma linha/coluna/diagonal com duas marcações do jogador e uma vazia
        """
        # Verifica linhas
        for linha in range(3):
            if self.conta_na_linha(linha, jogador) == 2 and self.conta_na_linha(linha, Tabuleiro.DESCONHECIDO) == 1:
                for col in range(3):
                    if self.matriz[linha][col] == Tabuleiro.DESCONHECIDO:
                        return (linha, col)
        
        # Verifica colunas
        for col in range(3):
            if self.conta_na_coluna(col, jogador) == 2 and self.conta_na_coluna(col, Tabuleiro.DESCONHECIDO) == 1:
                for linha in range(3):
                    if self.matriz[linha][col] == Tabuleiro.DESCONHECIDO:
                        return (linha, col)
        
        # Verifica diagonal principal (0,0) -> (2,2)
        if self.conta_na_diagonal_principal(jogador) == 2 and self.conta_na_diagonal_principal(Tabuleiro.DESCONHECIDO) == 1:
            for i in range(3):
                if self.matriz[i][i] == Tabuleiro.DESCONHECIDO:
                    return (i, i)
        
        # Verifica diagonal secundária (0,2) -> (2,0)
        if self.conta_na_diagonal_secundaria(jogador) == 2 and self.conta_na_diagonal_secundaria(Tabuleiro.DESCONHECIDO) == 1:
            for i in range(3):
                if self.matriz[i][2-i] == Tabuleiro.DESCONHECIDO:
                    return (i, 2-i)
        
        return None

    def conta_na_linha(self, linha, valor):
        """Conta quantas ocorrências do valor existem na linha"""
        return sum(1 for col in range(3) if self.matriz[linha][col] == valor)

    def conta_na_coluna(self, col, valor):
        """Conta quantas ocorrências do valor existem na coluna"""
        return sum(1 for linha in range(3) if self.matriz[linha][col] == valor)

    def conta_na_diagonal_principal(self, valor):
        """Conta quantas ocorrências do valor existem na diagonal principal"""
        return sum(1 for i in range(3) if self.matriz[i][i] == valor)

    def conta_na_diagonal_secundaria(self, valor):
        """Conta quantas ocorrências do valor existem na diagonal secundária"""
        return sum(1 for i in range(3) if self.matriz[i][2-i] == valor)

    def regra2_criar_duas_sequencias(self):
        """
        R2: Se houver uma jogada que crie duas sequências de duas marcações, use-a.
        """
        posicoes_vazias = self.get_posicoes_vazias()
        
        for linha, col in posicoes_vazias:
            # Simula a jogada
            self.matriz[linha][col] = self.tipo
            
            # Conta quantas sequências de 2 essa jogada criaria
            sequencias_de_2 = self.conta_sequencias_de_2()
            
            # Desfaz a simulação
            self.matriz[linha][col] = Tabuleiro.DESCONHECIDO
            
            # Se criar 2 ou mais sequências de 2, é uma boa jogada
            if sequencias_de_2 >= 2:
                return (linha, col)
        
        return None

    def conta_sequencias_de_2(self):
        """
        Conta quantas sequências de exatamente 2 marcações do jogador tem
        (sem ser bloqueada pelo oponente)
        """
        count = 0
        
        # Verifica linhas
        for linha in range(3):
            if (self.conta_na_linha(linha, self.tipo) == 2 and 
                self.conta_na_linha(linha, self.oponente) == 0):
                count += 1
        
        # Verifica colunas
        for col in range(3):
            if (self.conta_na_coluna(col, self.tipo) == 2 and 
                self.conta_na_coluna(col, self.oponente) == 0):
                count += 1
        
        # Verifica diagonal principal
        if (self.conta_na_diagonal_principal(self.tipo) == 2 and 
            self.conta_na_diagonal_principal(self.oponente) == 0):
            count += 1
        
        # Verifica diagonal secundária
        if (self.conta_na_diagonal_secundaria(self.tipo) == 2 and 
            self.conta_na_diagonal_secundaria(self.oponente) == 0):
            count += 1
        
        return count

    def regra3_marcar_centro(self):
        """
        R3: Se o quadrado central estiver livre, marque-o.
        """
        if self.matriz[1][1] == Tabuleiro.DESCONHECIDO:
            return (1, 1)
        return None

    def regra4_canto_oposto(self):
        """
        R4: Se seu oponente tiver marcado um dos cantos, marque o canto oposto.
        """
        cantos_opostos = [
            ((0, 0), (2, 2)),  # canto superior esquerdo <-> inferior direito
            ((0, 2), (2, 0)),  # canto superior direito <-> inferior esquerdo
            ((2, 2), (0, 0)),  # canto inferior direito <-> superior esquerdo
            ((2, 0), (0, 2))   # canto inferior esquerdo <-> superior direito
        ]
        
        for canto_oponente, canto_oposto in cantos_opostos:
            linha_op, col_op = canto_oponente
            linha_meu, col_meu = canto_oposto
            
            if (self.matriz[linha_op][col_op] == self.oponente and 
                self.matriz[linha_meu][col_meu] == Tabuleiro.DESCONHECIDO):
                return (linha_meu, col_meu)
        
        return None

    def regra5_canto_vazio(self):
        """
        R5: Se houver um canto vazio, marque-o.
        """
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        
        for linha, col in cantos:
            if self.matriz[linha][col] == Tabuleiro.DESCONHECIDO:
                return (linha, col)
        
        return None

    def regra6_posicao_vazia(self):
        """
        R6: Marcar arbitrariamente um quadrado vazio.
        """
        posicoes_vazias = self.get_posicoes_vazias()
        
        if len(posicoes_vazias) > 0:
            indice = randint(0, len(posicoes_vazias) - 1)
            return posicoes_vazias[indice]
        
        return None

    def get_posicoes_vazias(self):
        """
        Retorna uma lista com todas as posições vazias do tabuleiro
        """
        posicoes = []
        for linha in range(3):
            for col in range(3):
                if self.matriz[linha][col] == Tabuleiro.DESCONHECIDO:
                    posicoes.append((linha, col))
        return posicoes