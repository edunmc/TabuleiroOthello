class ClaudiaEduardo_GulosoPlayer:
  def __init__(self, color):
    self.color = color

  def play(self, board):
    return self.pegaMaiorCaminho(board.valid_moves(self.color), board)
  
  
  # estrategia que escolhe de forma gulosa a jogada que "come" mais pecas do inimigo
  def pegaMaiorCaminho(self, moves, board):
    from models.board import Board
    import random
    from models.move import Move
    
    melhorDist = 0
    melhorMov = None
    
    distancias = {}
    
    # para cada jogava possivel, ver quantas pecas do inimigo sao comidas e pega a maior
    for move in moves:
      dist_total = 0
      
      # para cada jogada possivel, vamos olhar em todas as direcoes pra calcular o
      # quanto sera comido no total
      for direction in Board.DIRECTIONS:
        posicao = [move.x + direction[0], move.y + direction[1]]
        inimigo = Board.BLACK if self.color == Board.WHITE else Board.WHITE
        dist = 0
        
        casa_sendo_vista = board.get_square_color(posicao[0],posicao[1])
        
        # soma 1 a distancia se estamos num caminho valido (casas do inimigo no meio da "linha")
        while casa_sendo_vista == inimigo:
          posicao = [posicao[0] + direction[0], posicao[1] + direction[1]]
          casa_sendo_vista = board.get_square_color(posicao[0],posicao[1])
          dist = dist + 1
        
        # se o caminho termina com uma casa minha, sera valido (comecou com a casa vazia onde jogaremos)
        if casa_sendo_vista == self.color:
          dist_total = dist_total + dist
      
      # verifica se vamos "comer" mais com essa jogada
      if dist_total > melhorDist:
        melhorDist = dist_total
        melhorMov = move
      
      distancias[(move.x, move.y)] = dist_total
        
    
    # selecionar aleatoriamente entre os melhores, caso haja empate
    melhores = []
    for casa, dist in distancias.items():
    	if dist == melhorDist:
    		melhores.append(Move(casa[0], casa[1]))
    
    
    return random.choice(melhores)
    
