import pygame, sys, torch
from pygame.locals import *
import random as rand


FPS = 30
FPSCLOCK = pygame.time.Clock()


BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)


SCORE3 = 1
SCORE4 = 2
SCORE5 = 3
PENALTY = 1

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH= 8
BOARDHEIGHT = 10
XMARGIN = int((WINDOWWIDTH -(BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT -(BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)






class Board:
    
    
    score = 0
    
    def __init__(self ):
        
        self.rows = 10
        self.columns = 8
        self.elements = 6
        
        self.board_size =  self.rows*self.columns
        
        self.rand_tensor = torch.randint(1, self.elements + 1,(self.rows, self.columns))

        
        


    def points_row_3(self, tensor):
        for i in range(self.rows):
            for j in range(self.columns - 2):
                if (tensor[i][j] == tensor[i][j+1] and tensor[i][j+1] == tensor[i][j+2] 
                    and (tensor[i][j] != 0)):
                    
                    tensor[i][j] = 0
                    tensor[i][j+1] = 0
                    tensor[i][j+2] = 0
                    
                    self.score += SCORE3
                    return(True)
        return(False)
    
    def points_row_4(self, tensor):
        for i in range(self.rows):
            for j in range(self.columns - 3):
                if ((tensor[i][j] == tensor[i][j+1]) and (tensor[i][j+1] == tensor[i][j+2]) and
                    (tensor[i][j+2] == tensor[i][j+3]) and (tensor[i][j] != 0)):
                    
                    tensor[i][j] = 0
                    tensor[i][j+1] = 0
                    tensor[i][j+2] = 0
                    tensor[i][j+3] = 0
                    
                    self.score += SCORE4
                    return(True)
        return(False)
    
    
    def points_row_5(self, tensor):
        for i in range(self.rows):
            for j in range(self.columns - 4):
                if ((tensor[i][j] == tensor[i][j+1]) and (tensor[i][j+1] == tensor[i][j+2]) and
                    (tensor[i][j+2] == tensor[i][j+3]) and (tensor[i][j+3] == tensor[i][j+4]) and (tensor[i][j] != 0)):
                    
                    tensor[i][j] = 0
                    tensor[i][j+1] = 0
                    tensor[i][j+2] = 0
                    tensor[i][j+3] = 0
                    tensor[i][j+4] = 0
                    
                    self.score += SCORE5
                    return(True, tensor)
        return(False)

    

    
    def points_columns_3(self, tensor):
        for j in range(self.columns):
            for i in range(self.rows -2):
                if (tensor[i][j] == tensor[i+1][j]) and (tensor[i + 1][j] == tensor[i + 2][j]) and (tensor[i][j] != 0):
                    
                    tensor[i][j] = 0
                    tensor[i+1][j] = 0
                    tensor[i + 2][j] = 0
                    
                    self.score += SCORE3
                    return(True)
        return(False)
    
    
    def points_columns_4(self, tensor):
        for j in range(self.columns):
            for i in range(self.rows -3):
                if ((tensor[i][j] == tensor[i+1][j]) and (tensor[i + 1][j] == tensor[i + 2][j]) 
                    and (tensor[i + 2][j] == tensor[i + 3][j]) and (tensor[i][j] != 0)):
                    
                    tensor[i][j] = 0
                    tensor[i+1][j] = 0
                    tensor[i + 2][j] = 0
                    tensor[i + 3][j] = 0
                    
                    self.score += SCORE4
                    return(True)
        return(False)
    
    
    def points_columns_5(self, tensor):
        for j in range(self.columns):
            for i in range(self.rows -4):
                if ((tensor[i][j] == tensor[i+1][j]) and (tensor[i + 1][j] == tensor[i + 2][j]) 
                    and (tensor[i + 2][j] == tensor[i + 3][j]) and (tensor[i + 3][j] == tensor[i + 4][j]) and (tensor[i][j] != 0)):
                   
                    tensor[i][j] = 0
                    tensor[i+1][j] = 0
                    tensor[i + 2][j] = 0
                    tensor[i + 3][j] = 0
                    tensor[i + 4][j] = 0
 
                    self.score += SCORE5
                    return(True)
        return(False)


    def trim(self, tensor):
        check = []
        while not check:  #here I'm using implicit booleanness of the empty list
        
            check.append(self.points_row_5(tensor))
            check.append(self.points_row_4(tensor))
            check.append(self.points_row_3(tensor))
            check.append(self.points_columns_5(tensor))
            check.append(self.points_columns_4(tensor))
            check.append(self.points_columns_3(tensor))
            if 1 in check:
                check = []
                
    def test_for_fall(self, tensor):
        for i in range(self.rows)[::-1]:
            for j in range(self.columns)[::-1]:
                if (tensor [i][j] == 0) and (tensor [i-1][j] != 0) and (i > 0): #Program searches for emplty place "closes" to upmost edge of the board
                    return(True)
        return(False)
                
    
    def fall(self, tensor):
        while(self.test_for_fall(tensor)):
            for i in range(self.rows)[::-1]:
                for j in range(self.columns)[::-1]:
                    if tensor [i][j] == 0:
                        if i > 0:
                            dummy = int(tensor[i-1][j])
                            tensor[i-1][j] = 0
                            tensor[i][j] = int(dummy)

          
    def is_zero(self, tensor):
        for i in range(self.rows)[::-1]:
            for j in range(self.columns)[::-1]:
                if tensor [i][j] == 0:
                    return(True)
        return(False)      

    def new_elements(self, tensor):
        for i in range(self.rows)[::-1]:
            for j in range(self.columns)[::-1]:
                if (tensor [i][j] == 0):
                    tensor[i][j] = rand.randint(1,self.elements)
                    
    def legal_board(self, tensor):
        self.trim(tensor)
        while self.is_zero(tensor):
            self.fall(tensor)
            self.new_elements(tensor)
            self.trim(tensor)
        return(tensor)
            
    def Penalty(self):
        self.score -= PENALTY
        
    def legal_move(self, tensor, i_1, j_1, i_2, j_2):
        if i_2 < 0 or i_2 > self.rows or j_2 < 0 or j_2 > self.columns:
            return(False)
        tensor_prime = tensor.clone()
        temp = int(tensor_prime[i_2][j_2])
        tensor_prime[i_2][j_2] = tensor_prime[i_1][j_1]
        tensor_prime[i_1][j_1] = temp
        
        for j in range(self.columns-2): #rows
            if (tensor_prime[i_2][j] == tensor_prime[i_2][j+1] 
                and tensor_prime[i_2][j+1] == tensor_prime[i_2][j+2]):
                #print("r", j, j+1, j+2)

                return(True)
            if (tensor_prime[i_1][j] == tensor_prime[i_1][j+1] 
                and tensor_prime[i_1][j+1] == tensor_prime[i_1][j+2]):
                return(True)
                #print("r", j, j+1, j+2)
            
        for i in range(self.rows -2): #columns
            if (tensor_prime[i][j_2] == tensor_prime[i+1][j_2]
            and tensor_prime[i + 1][j_2] == tensor_prime[i + 2][j_2]):
                return(True)
                #print("c", i, i+1, i+2)
            if (tensor_prime[i][j_1] == tensor_prime[i+1][j_1]
            and tensor_prime[i + 1][j_1] == tensor_prime[i + 2][j_1]):
                return(True)
                #print("c", i, i+1, i+2)
       
        return(False)

    def move_up(self, tensor, i, j):
        temp = int(tensor[i-1][j])
        tensor[i-1][j] = tensor[i][j]
        tensor[i][j] = temp

        
    def move_left(self, tensor, i, j):
        temp = int(tensor[i][j-1])
        tensor[i][j-1] = tensor[i][j]
        tensor[i][j] = temp

        
    def move_right(self, tensor, i, j):
        temp = int(tensor[i][j+1])
        tensor[i][j+1] = tensor[i][j]
        tensor[i][j] = temp

        
    def move_down(self, tensor, i, j):

        temp = int(tensor[i+1][j])
        tensor[i+1][j] = tensor[i][j]
        tensor[i][j] = temp

                     




class Game(Board):
    
    def __init__(self):
        
        super().__init__()
        
        self.window_size = (800,600)
        self.display_surf = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Gra")
        
        self.boxes = []
        self.move = False
        self.box_dragging = False
        self.cliked = False
        self.board = self.rand_tensor
        self.legal_board(self.board)
        self.score = 0
        self.moves = 10
        
        self.able_to_move = True
       
        
        print("działa")
        
    def create_boxes(self):
        
        self.boxes = []    
        for i in range(self.rows):
            for j in range(self.columns):
                if len(self.boxes) < self.rows*self.columns:
                    self.boxes.append(pygame.Rect(XMARGIN + j*(BOXSIZE + GAPSIZE),
                                                  YMARGIN + i*(BOXSIZE + GAPSIZE),
                                                  BOXSIZE,BOXSIZE))
        
    def draw_boxes(self):
        
        index = 0 
        
        for i in range(self.rows):
            for j in range(self.columns):
                
                
                if self.board[i][j] == 0:            
                    pygame.draw.rect(self.display_surf, NAVYBLUE, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                
                if self.board[i][j] == 1:            
                    pygame.draw.rect(self.display_surf, ORANGE, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                    
                if self.board[i][j] == 2:
                    pygame.draw.rect(self.display_surf, RED, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                    
                if self.board[i][j] == 3:
                    pygame.draw.rect(self.display_surf, BLUE, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                    
                if self.board[i][j] == 4:
                    pygame.draw.rect(self.display_surf, GREEN, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                    
                if self.board[i][j] == 5:
                    pygame.draw.rect(self.display_surf, YELLOW, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                    
                if self.board[i][j] == 6:
                    pygame.draw.rect(self.display_surf, CYAN, (self.boxes[index].x,
                                                               self.boxes[index].y,
                                                                BOXSIZE,BOXSIZE))
                    index += 1
                
        
    def draw_board(self):
            
        
        self.display_surf.fill(NAVYBLUE)
        self.draw_boxes()
             
    def draw_line_rows(self,start_box, end_box, line):
        drawing = True
        while drawing:
            self.draw_board()
            score_text = self.font.render("Score {0}".format(self.score), 1, WHITE) 
            moves_text = self.font.render("Moves {0}".format(self.moves), 1, WHITE)
            self.display_surf.blit(score_text, (5, 10))
            self.display_surf.blit(moves_text, (110, 10))
            #self.display_surf.blit(line, (line.x, line.y))
            pygame.draw.rect(self.display_surf, BLACK, (line.x, line.y, line.width, line.height))
            pygame.display.flip()
            line.width += 20
            if line.right > end_box.right:
                drawing = False
            FPSCLOCK.tick(FPS)
 
    def draw_line_columns(self,start_box, end_box, line):
        drawing = True
        while drawing:
            self.draw_board()
            score_text = self.font.render("Score {0}".format(self.score), 1, WHITE) 
            moves_text = self.font.render("Moves {0}".format(self.moves), 1, WHITE)
            self.display_surf.blit(score_text, (5, 10))
            self.display_surf.blit(moves_text, (110, 10))
            #self.display_surf.blit(line, (line.x, line.y))
            pygame.draw.rect(self.display_surf, BLACK, (line.x, line.y, line.width, line.height))
            pygame.display.flip()
            line.height += 20
            if line.bottom > end_box.bottom:
                drawing = False
            FPSCLOCK.tick(FPS)
    
    def cross_animation(self):
        board_prime = self.board.clone()
        self.able_to_move = False
        
        if self.points_row_5(board_prime):
            self.score -= SCORE5
            for i in range(self.rows):
                for j in range(self.columns-4):
                    if board_prime[i][j] == 0:
                        start_box = self.boxes[self.get_box_index(i,j)]
                        end_box = self.boxes[self.get_box_index(i,j+4)]
                        line = pygame.Rect(start_box.x, start_box.midleft[1]-5, 5, 10)
                        
                        self.draw_line_rows(start_box, end_box, line)
                    
                        self.points_row_5(self.board)
                        self.able_to_move = True
                        break
                    
        if self.points_row_4(board_prime):
            self.score -= SCORE4
            for i in range(self.rows):
                for j in range(self.columns-3):
                    if board_prime[i][j] == 0:
                        start_box = self.boxes[self.get_box_index(i,j)]
                        end_box = self.boxes[self.get_box_index(i,j+3)]
                        line = pygame.Rect(start_box.x, start_box.midleft[1]-5, 5, 10)
                        
                        self.draw_line_rows(start_box, end_box, line)
                    
                        self.points_row_4(self.board)
                        self.able_to_move = True
                        break
        
        if self.points_row_3(board_prime):
            self.score -= SCORE3
            for i in range(self.rows):
                for j in range(self.columns-2):
                    if board_prime[i][j] == 0:
                        start_box = self.boxes[self.get_box_index(i,j)]
                        end_box = self.boxes[self.get_box_index(i,j+2)]
                        line = pygame.Rect(start_box.x, start_box.midleft[1]-5, 5, 10)
                        
                        self.draw_line_rows(start_box, end_box, line)
                    
                        self.points_row_3(self.board)
                        self.able_to_move = True
                        break

        if self.points_columns_5(board_prime):
            self.score -= SCORE5
            for j in range(self.columns):
                for i in range(self.rows-4):
                
                    if board_prime[i][j] == 0:
                        start_box = self.boxes[self.get_box_index(i,j)]
                        end_box = self.boxes[self.get_box_index(i+4,j)]
                        line = pygame.Rect(start_box.midtop[0] -5, start_box.y, 10, 5)
                        
                        self.draw_line_columns(start_box, end_box, line)
                    
                        self.points_columns_5(self.board)
                        self.able_to_move = True
                        break
                    
        if self.points_columns_4(board_prime):
            self.score -= SCORE4
            for j in range(self.columns):
                for i in range(self.rows-3):
                
                    if board_prime[i][j] == 0:
                        start_box = self.boxes[self.get_box_index(i,j)]
                        end_box = self.boxes[self.get_box_index(i+3,j)]
                        line = pygame.Rect(start_box.midtop[0] -5, start_box.y, 10, 5)
                        
                        self.draw_line_columns(start_box, end_box, line)
                    
                        self.points_columns_4(self.board)
                        self.able_to_move = True
                        break

        if self.points_columns_3(board_prime):
            self.score -= SCORE3
            for j in range(self.columns):
                for i in range(self.rows-2):
                
                    if board_prime[i][j] == 0:
                        start_box = self.boxes[self.get_box_index(i,j)]
                        end_box = self.boxes[self.get_box_index(i+2,j)]
                        line = pygame.Rect(start_box.midtop[0] -5, start_box.y, 10, 5)
                        
                        self.draw_line_columns(start_box, end_box, line)
                    
                        self.points_columns_3(self.board)
                        self.able_to_move = True
                        break      
                    
        self.able_to_move = True         
                    
    def fall_animation(self):
        pass
               
    def get_position(self, x, y):
        for i in range(self.rows):
            for j in range(self.columns):
                if x >= XMARGIN + j*(BOXSIZE + GAPSIZE) and x <= XMARGIN + j*(BOXSIZE + GAPSIZE) + BOXSIZE:
                    if y >= YMARGIN + i*(BOXSIZE + GAPSIZE) and y <= YMARGIN + i*(BOXSIZE + GAPSIZE) + BOXSIZE:
                        return(i,j)
                    
    def get_box_index(self, i, j):
        return((i*self.columns + j)%(self.rows*self.columns))
    
    def legal_board_animation(self):
        self.cross_animation()
        while self.is_zero(self.board):
            self.fall(self.board)
            self.create_boxes()
            self.new_elements(self.board)
            self.create_boxes()
            self.cross_animation()
            self.create_boxes()
            

    def start(self):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 20)
        self.mid_font = pygame.font.SysFont("monospace", 50)
        self.big_font = pygame.font.SysFont("monospace", 100)
        
        self.run()
        self.game_over()
           

    def run(self):

        
        left, right, up, down = False, False, False, False
        count=0
        
        self.create_boxes()
        self.draw_board()

        while self.moves > 0:  #main game loop
    
        
            for event in pygame.event.get():
                
                if event.type == QUIT or(event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.able_to_move:
                        for box in self.boxes:
                            if box.collidepoint(event.pos):
                                selected_box = self.boxes[self.boxes.index(box)]
                                basic_x, basic_y = selected_box.x,  selected_box.y
                                
                                mouse_x, mouse_y = event.pos
                                basic_mouse_x, basic_mouse_y = mouse_x, mouse_y
                                
                                i,j = self.get_position(mouse_x, mouse_y)
                                
                                box_up = self.boxes[self.get_box_index(i-1,j)]
                                basic_u_x, basic_u_y = box_up.x, box_up.y
                                
                                box_down = self.boxes[self.get_box_index(i+1,j)]
                                basic_d_x, basic_d_y = box_down.x, box_down.y
                                
                                box_left = self.boxes[self.get_box_index(i,j-1)]
                                basic_l_x, basic_l_y = box_left.x, box_left.y
                                
                                box_right = self.boxes[self.get_box_index(i,j + 1)]
                                basic_r_x, basic_r_y = box_right.x, box_right.y
                                
                                self.box_dragging = True
                                self.cliked = True

                                offset_x = selected_box.x - mouse_x #offset is difference between box upper left corner and mouse position
                                offset_y = selected_box.y - mouse_y
                                break
                                
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1 and self.cliked:
                         self.box_dragging = False
                         self.cliked = False
                         
                         
                         if (left and selected_box.x == XMARGIN + (j-1)*(BOXSIZE + GAPSIZE)):
                             
                             if self.legal_move(self.board, i, j, i, j-1):
                                 #print(self.board, "\n")
                                 self.move_left(self.board, i,j)
                                 self.create_boxes()
                                 #self.trim(self.board)
                                 self.legal_board_animation()
                                 self.create_boxes()
                                 self.moves -=1
                                 
                             else:
                                selected_box.x,  selected_box.y = basic_x, basic_y
                                box_left.x, box_left.y = basic_l_x, basic_l_y
                             
                             
                         elif right and selected_box.x == XMARGIN + (j+1)*(BOXSIZE + GAPSIZE):
                              
                             if self.legal_move(self.board, i, j, i, j+1):
                                 
                                 #print(self.board, "\n")
                                 self.move_right(self.board, i,j)
                                 #print(self.board, "\n")
                                 self.create_boxes()
                                 #self.cross_animation()
                                 self.legal_board_animation()
                                 self.create_boxes()
                                 self.moves -=1
                             else:
                                 selected_box.x,  selected_box.y = basic_x, basic_y
                                 box_right.x, box_right.y = basic_r_x, basic_r_y
                                                        
                         elif up and selected_box.y == YMARGIN + (i-1)*(BOXSIZE + GAPSIZE):
                                                             
                             if self.legal_move(self.board, i, j, i-1 ,j):
                                 
                                 
                                 #print(self.board, "\n")
                                 self.move_up(self.board,i,j) 
                                 #print(self.board, "\n")
                                 self.create_boxes()
                                 #self.cross_animation()
                                 self.legal_board_animation()
                                 self.create_boxes()
                                 
                                 self.moves -=1
                             else:
                                 selected_box.x,  selected_box.y = basic_x, basic_y
                                 box_up.x, box_up.y = basic_u_x, basic_u_y
                             
                         elif down and selected_box.y == YMARGIN + (i+1)*(BOXSIZE + GAPSIZE):
                             
                             if self.legal_move(self.board, i, j, i+1, j):
                                 
                                 #print(self.board, "\n")
                                 self.move_down(self.board,i,j) 
                                 #print(self.board, "\n")
                                 self.create_boxes()
                                 #self.cross_animation()
                                 self.legal_board_animation()
                                 self.create_boxes()
                                 self.moves -=1
                             else:
                                 selected_box.x,  selected_box.y = basic_x, basic_y
                                 box_down.x, box_down.y = basic_d_x, basic_d_y
                             
           
                             
                         else:
                             
                             selected_box.x,  selected_box.y = basic_x, basic_y
                             box_up.x, box_up.y = basic_u_x, basic_u_y
                             box_down.x, box_down.y = basic_d_x, basic_d_y
                             box_left.x, box_left.y = basic_l_x, basic_l_y
                             box_right.x, box_right.y = basic_r_x, basic_r_y
                         
                         left, right, up, down = False, False, False, False
                         count=0
                         
                if event.type == MOUSEMOTION:
                    if self.box_dragging:
                        
                        mouse_x, mouse_y = event.pos
                        if not left and not right and not up and not down:
                            
                            
                            if count < 10:
                                count += 1
                                break
                            
                            diff_x = basic_mouse_x - mouse_x
                            diff_y = basic_mouse_y - mouse_y
                            
                            if diff_x > 0 and abs(diff_x) > abs(diff_y) and j>0:
                                left = True
                                
                            if diff_x < 0 and abs(diff_x) > abs(diff_y)and j < self.columns -1:
                                right = True
                                
                            if diff_y > 0 and abs(diff_x) < abs(diff_y) and i > 0:
                                up = True
                                
                            if diff_y < 0 and abs(diff_x) < abs(diff_y) and i < self.rows -1:
                                down = True
                                
                        
                        
                        if left:
                            selected_box.x = mouse_x + offset_x
                            selected_box.y = basic_y
                            
                            box_left.y = basic_l_y
                            
                            if selected_box.x > basic_x:
                                selected_box.x = basic_x
                                
                            elif selected_box.x < XMARGIN + (j-1)*(BOXSIZE + GAPSIZE):
                                selected_box.x = XMARGIN + (j-1)*(BOXSIZE + GAPSIZE)
                                box_left.x = XMARGIN + (j)*(BOXSIZE + GAPSIZE)
                                    
                            else:
                                selected_box.x = mouse_x + offset_x
                                box_left.x = basic_l_x + (basic_mouse_x - mouse_x)
                                
                        if right:
                            selected_box.x = mouse_x + offset_x
                            selected_box.y = basic_y
                            
                            box_right.y = basic_r_y
                            
                            if selected_box.x < basic_x:
                                selected_box.x = basic_x
                                
                            elif selected_box.x > XMARGIN + (j+1)*(BOXSIZE + GAPSIZE):
                                selected_box.x = XMARGIN + (j+1)*(BOXSIZE + GAPSIZE)
                                box_right.x = XMARGIN + (j)*(BOXSIZE + GAPSIZE)
                                    
                            else:
                                selected_box.x = mouse_x + offset_x
                                box_right.x = basic_r_x + (basic_mouse_x - mouse_x)
                                
                        if up:
                            selected_box.x = basic_x
                            selected_box.y = mouse_y + offset_y
                            
                            box_up.x = basic_u_x
                            
                            if selected_box.y > basic_y:
                                selected_box.y = basic_y
                                
                            elif selected_box.y < YMARGIN + (i-1)*(BOXSIZE + GAPSIZE):
                                selected_box.y = YMARGIN + (i-1)*(BOXSIZE + GAPSIZE)
                                box_up.y = YMARGIN + (i)*(BOXSIZE + GAPSIZE)
                                    
                            else:
                                selected_box.y = mouse_y + offset_y
                                box_up.y = basic_u_y + (basic_mouse_y - mouse_y)
                                  
                                
                        if down:
                            selected_box.x = basic_x
                            selected_box.y = mouse_y + offset_y
                            
                            box_down.x = basic_d_x
                            
                            if selected_box.y < basic_y:
                                selected_box.y = basic_y
                                
                            elif selected_box.y > YMARGIN + (i+1)*(BOXSIZE + GAPSIZE):
                                selected_box.y = YMARGIN + (i+1)*(BOXSIZE + GAPSIZE)
                                box_down.y = YMARGIN + (i)*(BOXSIZE + GAPSIZE)
                                    
                            else:
                                selected_box.y = mouse_y + offset_y
                                box_down.y = basic_d_y + (basic_mouse_y - mouse_y)
                            
                        
                        
                        
                self.draw_board()
                score_text = self.font.render("Score {0}".format(self.score), 1, WHITE) 
                moves_text = self.font.render("Moves {0}".format(self.moves), 1, WHITE)
                self.display_surf.blit(score_text, (5, 10))
                self.display_surf.blit(moves_text, (110, 10))
                pygame.display.flip()
                FPSCLOCK.tick(FPS)
            
        
        
    def game_over(self):
        
        
        self.display_surf.fill(NAVYBLUE)
        
        restart_text = self.mid_font.render("Restart", 1, WHITE)
        restart_button = restart_text.get_rect()
        restart_button.midtop = (WINDOWWIDTH / 4, WINDOWHEIGHT/2)
        self.display_surf.blit(restart_text, (restart_button.x, restart_button.y))
        
        quit_text = self.mid_font.render("Quit", 1, WHITE)
        quit_button = quit_text.get_rect()
        quit_button.midtop = (3*WINDOWWIDTH / 4, WINDOWHEIGHT/2)
        self.display_surf.blit(quit_text, (quit_button.x, quit_button.y))
        
        while True:
            for event in pygame.event.get():
                
                if event.type == QUIT or(event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if restart_button.collidepoint(event.pos):
                            self.board = self.rand_tensor
                            self.legal_board(self.board)
                            self.score = 0
                            self.moves = 10
                            
                            self.start()
                        if quit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                
            game_over_text = self.big_font.render("Game Over", 1, WHITE)
            go_text_rec = game_over_text.get_rect()
            go_text_rec.midtop = (WINDOWWIDTH / 2, 10)
            self.display_surf.blit(game_over_text,  (go_text_rec.x, go_text_rec.y))

            score_text = self.big_font.render("Score {0}".format(self.score), 1, WHITE)
            score_rec = score_text.get_rect()
            score_rec.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/4)
            self.display_surf.blit(score_text, (score_rec.x, score_rec.y))
            
            pygame.display.flip()
            FPSCLOCK.tick(FPS)



def start_AI(self):

    pygame.init()
    self.font = pygame.font.SysFont("monospace", 20)
    self.mid_font = pygame.font.SysFont("monospace", 50)
    self.big_font = pygame.font.SysFont("monospace", 100)


def run_AI(self, tensor):
    
    self.create_boxes()
    self.draw_board()
    
    while self.moves > 0:
    
        for i in range(self.rows):
            for j in range(self.columns):
                for k in range(4):
                
                    if tensor[i][j][k] == 0:
                        self.move_left
                    
                    if tensor[i][j][k] == 1:
                        self.move_right
                    
                    if tensor[i][j][k] == 0:
                        self.move_up
                    
                    if tensor[i][j][k] == 0:
                        self.move_down
                    
                
    
    
    
                
if __name__ == "__main__":     
    g = Game()
    g.start()

