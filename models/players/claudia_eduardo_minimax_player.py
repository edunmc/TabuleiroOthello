class ClaudiaEduardo_MinimaxPlayer:
  def __init__(self, color):
    self.color = color

  def play(self, board):
    (melhor_val, melhor_mov) = self.maxi(board, 4, 0, 10000)
    
    if melhor_mov == None:
      import random
      return random.choice(board.valid_moves(self.color))
    
    return melhor_mov
  
  
  # funcao de avaliacao: (quanto mais, melhor para mim)
  #
  # soma de todos os abaixo:
  #  - oposto da distancia manhattan (dist_manh*(-1)) de cada peca minha para o canto mais proximo
  #  - distancia manhattan de cada peca do oponente para o canto mais proximo
  #
  # exceto em casos extraordinarios, em que sao somados/subtraidos os valores abaixo:
  #  - peca minha no canto: soma 10000
  #  - peca minha num semicanto (3 casas que cercam cada canto): subtrai 100000
  #  - peca minha numa parede: soma 5000
  #  - peca do inimigo num canto: subtrai 100000
  #  - peca do inimigo num semicanto: soma 10000
  def avalia(self, estado):
    from models.board import Board
    
    total = 0
    
    eu = self.color
    inimigo = Board.BLACK if self.color == Board.WHITE else Board.WHITE
    
    import math
    corners = [[1,1],[1,8],[8,1],[8,8]]
    semicorners = [[1,2],[2,1],[2,2],[1,7],[2,7],[2,8],[7,1],[7,2],[8,2],[7,7],[7,8],[8,7]]
    
    for i in range(1, 9):
      for j in range(1, 9):
      
      	casa = estado.board[i][j]
        
        if casa == eu or casa == inimigo:
          
          # distancia ate o canto mais proximo
          menor_dist = 100
        
          for corner in corners:
            dist_x = abs(corner[0] - i)
            dist_y = abs(corner[1] - j)
            
            dist = dist_x + dist_y
            
            if dist < menor_dist:
              menor_dist = dist
          
          # eu
          if casa == eu:
            if [i,j] in corners:
              total = total + 10000
            elif [i,j] in semicorners:
              total = total - 100000
            elif i == 1 or i == 8 or j == 1 or j == 8:
              total = total + 5000
            else:
              total = total - menor_dist
              
          # inimigo
          else:
            if [i,j] in corners:
              total = total - 100000
            elif [i,j] in semicorners:
              total = total + 10000
            else:
              total = total + menor_dist
    
    return total
          


  # retorna True se o tabuleiro estiver completo (sem casas vazias)  
  def fim_de_jogo(self, estado):
    for i in range(1, 9):
      for j in range(1, 9):
        if estado.board[i][j] == '.':
          return False
    return True

  
  
  # escolha do maior entre os estados seguintes possiveis
  def maxi(self, estado, prof_max, prof_atual, beta):
    from models.board import Board
    
    eu = self.color
    inimigo = Board.BLACK if self.color == Board.WHITE else Board.WHITE
    
    # condicoes de parada
    if prof_atual == prof_max:
      return (self.avalia(estado), None)
    
    if self.fim_de_jogo(estado):
      return (-1000, None)
    
    melhor_val = -10000
    melhor_mov = None
    
    moves = estado.valid_moves(self.color)
    
    # jogador sem movimentos
    if len(moves) == 0:
      return (self.avalia(estado), None)
    
    for move in moves:
      
      # criamos de um novo tabuleiro igual ao atual,
      # e fazemos o movimento
      estado_novo = Board(estado.board)
      estado_novo.play(move, eu)
      
      # cada estado seguinte eh o minimo entre seus seguintes
      (valor, mov) = self.mini(estado_novo, prof_max, prof_atual+1, melhor_val)
      
      # se o valor de um dos filhos (ou seja, alfa >= esse valor)
      # for maior que o beta do pai (mini que chamou o max atual),
      # podemos parar esse ramo por aqui
      # (e nao importa o que for retornado, ja que quem definiu o beta do pai eh melhor)
      if valor > beta:
        return (-1000, None)
      
      if valor > melhor_val:
        melhor_val = valor
        melhor_mov = move
      
    return (melhor_val, melhor_mov)
          
  
  
  # escolha do menor entre os estados seguintes possiveis
  def mini(self, estado, prof_max, prof_atual, alfa):
    from models.board import Board
    
    eu = self.color
    inimigo = Board.BLACK if self.color == Board.WHITE else Board.WHITE
    
    # condicoes de parada
    if prof_atual == prof_max:
      return (self.avalia(estado), None)
    
    if self.fim_de_jogo(estado):
      return (1000, None)
    
    melhor_val = 10000
    melhor_mov = None
    
    moves = estado.valid_moves(self.color)
    
    # jogador sem movimentos
    if len(moves) == 0:
      return (self.avalia(estado), None)
    
    for move in moves:
      
      # criamos de um novo tabuleiro igual ao atual,
      # e fazemos o movimento
      estado_novo = Board(estado.board)
      estado_novo.play(move, inimigo)
      
      # cada estado seguinte eh o maximo entre seus seguintes
      (valor, mov) = self.maxi(estado_novo, prof_max, prof_atual+1, melhor_val)
      
      # se o valor de um dos filhos (ou seja, beta <= esse valor)
      # for menor que o alfa do pai (max que chamou o mini atual),
      # podemos parar esse ramo por aqui
      # (e nao importa o que for retornado, ja que quem definiu o alfa do pai eh melhor)
      if valor < alfa:
        return (1000, None)
      
      if valor < melhor_val:
        melhor_val = valor
        melhor_mov = move
      
    return (melhor_val, melhor_mov)
    
