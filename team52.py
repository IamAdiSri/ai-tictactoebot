#!/usr/bin/python
import sys
import random
import signal
import time
import copy

class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()

class Player52():
	def __init__(self):
		pass

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		maxval = -100000
		bm = []
		alpha = -100000
		beta = 100000
		cells = board.find_valid_move_cells(old_move)
		for cell in cells:
			if flag=='x':
				fl = 'o'
			else:
				fl = 'x'
			board.update(old_move,cell,flag)
			val = self.minimax(board, 0, 0, fl, cell, alpha, beta)
			#print val
			self.revert(board, cell,'-')
			if val > maxval:
				maxval = val
				bm = cell	

		print bm
		return bm

	def minimax(self, board, depth, isMax, flag, old_move, alpha, beta):
		#to check for the best optimal move
		k = board.find_terminal_state()
		if flag=='x':
			fl = 'o'
		else:
			fl = 'x'
		if k[1]=="WON" and k[0]=='x':
			return -100
		elif k[1]=="WON" and k[0]=='o':
			return 100
		elif k[0]=='NONE' and k[1]=="DRAW":
			return 0

		if depth >= 3: # run heuristic
			#print "yayay"
			return self.heuristic2(board, depth, isMax, flag, old_move)

		cells = board.find_valid_move_cells(old_move)

		if isMax:	
			best = -100000
			for cell in cells:
				if board.board_status[cell[0]][cell[1]]=='-':
					board.update(old_move,cell,flag)
					best = max(best,self.minimax(board, depth+1, (isMax+1)%2, fl, cell, alpha, beta))
					self.revert(board, cell,'-')
					alpha = max(best,alpha)
					if beta<=alpha:
						break
			ans = best
		else:
			best = 100000 
			for cell in cells:
				if board.board_status[cell[0]][cell[1]]=='-':
					board.update(old_move,cell,flag)
					best = min(best,self.minimax(board, depth+1, (isMax+1)%2, fl, cell, alpha, beta))
					self.revert(board, cell,'-')
					beta = min(best,beta)
					if beta<=alpha:
						break
			ans = best
		return ans

	def heuristic1(self, board, depth, isMax, flag, old_move):
		alt_flag = 'x'
		if flag == 'x' and isMax == 1:
			alt_flag = 'o'
		if flag == 'o' and isMax == 0:
			flag = 'x'
			alt_flag = '0'
		if flag == 'x' and isMax == 0:
			flag = 'o'
			alt_flag = 'x'

		bs = board.block_status
		score = 0
		for i in range(4):
			for j in range(4):
				if bs[i][j] == flag:
					score += 1
				elif bs[i][j] == 'd':
					score += 0.5
				elif bs[i][j] == alt_flag:
					score -= 1
		return score
	
	def heuristic2(self, board, depth, isMax, flag, old_move): # add possibilities of oo-o/o-oo
		#print "hi"
		alt_flag = 'x'
		if flag == 'x' and isMax == 1:
			alt_flag = 'o'
		if flag == 'o' and isMax == 0:
			flag = 'x'
			alt_flag = '0'
		if flag == 'x' and isMax == 0:
			flag = 'o'
			alt_flag = 'x'

		bs = board.block_status
		bds = board.board_status
		score = 0
		#checking for x/o  at corner, center and any other position of the block status for max and min
		for i in range(4):
			for j in range(4):
				if bs[i][j] == flag:
					if (i==0 or i==3) and (j==0 or j==3):
						score+=3
					elif ((i==1 or i==2) and (j==0 or j==3)) or ((i==0 or i==3) and (j==1 or j==2)):
						score+=5
					else:
						score+=10
				elif bs[i][j] == 'd':
					score += 0.5
				elif bs[i][j] == alt_flag:
					if (i==0 or i==3) and (j==0 or j==3):
						score-=3
					elif ((i==1 or i==2) and (j==0 or j==3)) or ((i==0 or i==3) and (j==1 or j==2)):
						score-=5
					else:
						score-=10
		#print score
		
		#checking for 3 continuous x/o in a column/row/diagonal of the board_status for given max player
		for x in range(4):
			for y in range(4):
				for i in range(4):
					if (((bds[4*x+i][4*y] == bds[4*x+i][4*y+1] == bds[4*x+i][4*y+2]) and bds[4*x+i][4*y] == flag and (not bds[4*x+i][4*y+3] == alt_flag)) or ((bds[4*x+i][4*y+1] == bds[4*x+i][4*y+2] 
						== bds[4*x+i][4*y+3]) and bds[4*x+i][4*y+1] == flag and (not bds[4*x+i][4*y] == alt_flag))):
						score += 3
					if (((bds[4*x][4*y+i] == bds[4*x+1][4*y+i] == bds[4*x+2][4*y+i]) and bds[4*x][4*y+i] == flag and (not bds[4*x+3][4*y+i] == alt_flag)) or ((bds[4*x+1][4*y+i] == bds[4*x+2][4*y+i]
						== bds[4*x+3][4*y+i]) and bds[4*x+1][4*y+i] == flag and (not bds[4*x][4*y+i] == alt_flag))):
						score += 3
					if (((bds[4*x+i][4*y] == bds[4*x+i][4*y+1] == bds[4*x+i][4*y+3]) and bds[4*x+i][4*y] == flag and (not bds[4*x+i][4*y+2] == alt_flag)) or ((bds[4*x+i][4*y+0] == bds[4*x+i][4*y+2] 
						== bds[4*x+i][4*y+3]) and bds[4*x+i][4*y] == flag and (not bds[4*x+i][4*y+1] == alt_flag))):
						score += 3
					if (((bds[4*x][4*y+i] == bds[4*x+1][4*y+i] == bds[4*x+3][4*y+i]) and bds[4*x][4*y+i] == flag and (not bds[4*x+2][4*y+i] == alt_flag)) or ((bds[4*x+0][4*y+i] == bds[4*x+2][4*y+i]
						== bds[4*x+3][4*y+i]) and bds[4*x][4*y+i] == flag and (not bds[4*x+1][4*y+i] == alt_flag))):
						score += 3
				
				if (((bds[4*x][4*y] == bds[4*x+1][4*y+1] == bds[4*x+2][4*y+2]) and (bds[4*x][4*y] == flag) and (not bds[4*x+3][4*y+3] == alt_flag)) 
					or ((bds[4*x+1][4*y+1] == bds[4*x+2][4*y+2] == bds[4*x+3][4*y+3]) and (bds[4*x+1][4*y+1] == flag) and (not bds[4*x][4*y] == alt_flag))):
					score += 2
				if (((bds[4*x+3][4*y] == bds[4*x+2][4*y+1] == bds[4*x+1][4*y+2])  and (bds[4*x+3][4*y] == flag) and (not bds[4*x][4*y+3] == alt_flag))
					or ((bds[4*x+2][4*y+1] == bds[4*x+1][4*y+2] == bds[4*x][4*y+3]) and (bds[4*x][4*y+3]==flag) and (not bds[4*x+3][4*y] == alt_flag))):
					score += 2
				if (((bds[4*x][4*y] == bds[4*x+1][4*y+1] == bds[4*x+3][4*y+3]) and (bds[4*x][4*y] == flag) and (not bds[4*x+2][4*y+2] == alt_flag)) 
					or ((bds[4*x][4*y] == bds[4*x+2][4*y+2] == bds[4*x+3][4*y+3]) and (bds[4*x][4*y] == flag) and (not bds[4*x+1][4*y+1] == alt_flag))):
					score += 2
				if (((bds[4*x+3][4*y] == bds[4*x+2][4*y+1] == bds[4*x][4*y+3])  and (bds[4*x+3][4*y] == flag) and (not bds[4*x+1][4*y+2] == alt_flag))
					or ((bds[4*x+3][4*y+1] == bds[4*x+1][4*y+2] == bds[4*x][4*y+3]) and (bds[4*x][4*y+3] == flag) and (not bds[4*x+2][4*y+1] == alt_flag))):
					score += 2
		
		#checking for 3 continuous x/o in a column/row/diagonal of the board_status for given min player
		for x in range(4):
			for y in range(4):
				for i in range(4):
					if (((bds[4*x+i][4*y] == bds[4*x+i][4*y+1] == bds[4*x+i][4*y+2]) and bds[4*x+i][4*y] == alt_flag and (not bds[4*x+i][4*y+3] == flag)) or ((bds[4*x+i][4*y+1] == bds[4*x+i][4*y+2] 
						== bds[4*x+i][4*y+3]) and bds[4*x+i][4*y+1] == alt_flag and (not bds[4*x+i][4*y] == flag))):
						score -= 3
					if (((bds[4*x][4*y+i] == bds[4*x+1][4*y+i] == bds[4*x+2][4*y+i]) and bds[4*x][4*y+i] == alt_flag and (not bds[4*x+3][4*y+i] == flag)) or ((bds[4*x+1][4*y+i] == bds[4*x+2][4*y+i]
						== bds[4*x+3][4*y+i]) and bds[4*x+1][4*y+i] == alt_flag and (not bds[4*x][4*y+i] == flag))):
						score -= 3
						if (((bds[4*x+i][4*y] == bds[4*x+i][4*y+1] == bds[4*x+i][4*y+3]) and bds[4*x+i][4*y] == alt_flag and (not bds[4*x+i][4*y+2] == flag)) or ((bds[4*x+i][4*y+0] == bds[4*x+i][4*y+2] 
						== bds[4*x+i][4*y+3]) and bds[4*x+i][4*y] == alt_flag and (not bds[4*x+i][4*y+1] == flag))):
						score -= 3
					if (((bds[4*x][4*y+i] == bds[4*x+1][4*y+i] == bds[4*x+3][4*y+i]) and bds[4*x][4*y+i] == alt_flag and (not bds[4*x+2][4*y+i] == flag)) or ((bds[4*x+0][4*y+i] == bds[4*x+2][4*y+i]
						== bds[4*x+3][4*y+i]) and bds[4*x][4*y+i] == alt_flag and (not bds[4*x+1][4*y+i] == flag))):
						score -= 3
				
				if (((bds[4*x][4*y] == bds[4*x+1][4*y+1] == bds[4*x+2][4*y+2]) and (bds[4*x][4*y] == alt_flag) and (not bds[4*x+3][4*y+3] == flag)) 
					or ((bds[4*x+1][4*y+1] == bds[4*x+2][4*y+2] == bds[4*x+3][4*y+3]) and (bds[4*x+1][4*y+1] == alt_flag) and (not bds[4*x][4*y] == flag))):
					score -= 2
				if (((bds[4*x+3][4*y] == bds[4*x+2][4*y+1] == bds[4*x+1][4*y+2])  and (bds[4*x+3][4*y] == alt_flag) and (not bds[4*x][4*y+3] == flag))
					or ((bds[4*x+2][4*y+1] == bds[4*x+1][4*y+2] == bds[4*x+3][4*y]) and (bds[4*x][4*y+3] == alt_flag) and (not bds[4*x+3][4*y] == flag))):
					score -= 2
				if (((bds[4*x][4*y] == bds[4*x+1][4*y+1] == bds[4*x+3][4*y+3]) and (bds[4*x][4*y] == alt_flag) and (not bds[4*x+2][4*y+2] == flag)) 
					or ((bds[4*x][4*y] == bds[4*x+2][4*y+2] == bds[4*x+3][4*y+3]) and (bds[4*x][4*y] == alt_flag) and (not bds[4*x+1][4*y+1] == flag))):
					score -= 2
				if (((bds[4*x+3][4*y] == bds[4*x+2][4*y+1] == bds[4*x][4*y+3])  and (bds[4*x+3][4*y] == alt_flag) and (not bds[4*x+1][4*y+2] == flag))
					or ((bds[4*x+3][4*y+1] == bds[4*x+1][4*y+2] == bds[4*x][4*y+3]) and (bds[4*x][4*y+3] == alt_flag) and (not bds[4*x+2][4*y+1] == flag))):
					score -= 2
		
		#checking for 3 continuous x/o in a column/row/diagonal of the block_status for max player
		for i in range(4):
			if  (((bs[i][0] == bs[i][1] == bs[i][2]) and (bs[i][0] == flag) and (not bs[i][3] == alt_flag)) or ((bs[i][3] == bs[i][1] == bs[i][2]) and (bs[i][3] == flag) 
				and (not bs[i][0] == alt_flag))):
				score += 4
			if  (((bs[0][i] == bs[1][i] == bs[2][i]) and (bs[0][i] == flag) and (not bs[3][i] == alt_flag)) or ((bs[3][i] == bs[1][i] == bs[2][i]) and (bs[3][i] == flag) 
				and (not bs[i][0] == alt_flag))):
				score += 4
			if  (((bs[i][0] == bs[i][1] == bs[i][3]) and (bs[i][0] == flag) and (not bs[i][2] == alt_flag)) or ((bs[i][3] == bs[i][0] == bs[i][2]) and (bs[i][3] == flag) 
				and (not bs[i][1] == alt_flag))):
				score += 4
			if  (((bs[0][i] == bs[1][i] == bs[3][i]) and (bs[0][i] == flag) and (not bs[2][i] == alt_flag)) or ((bs[3][i] == bs[0][i] == bs[2][i]) and (bs[3][i] == flag) 
				and (not bs[i][1] == alt_flag))):
				score += 4

		if (((bs[3][3] == bs[1][1] == bs[2][2]) and bs[3][3] == flag and (not bs[0][0] == alt_flag)) or ((bs[0][0] == bs[1][1] == bs[2][2]) and bs[0][0] == flag 
			and (not bs[3][3] == alt_flag))):
			score += 4
		if (((bs[0][3] == bs[1][2] == bs[2][1]) and bs[0][3] == flag and (not bs[3][0] == alt_flag)) or ((bs[3][0] == bs[1][2] == bs[2][1]) and bs[3][0] == flag 
			and (not bs[0][3] == alt_flag))):
			score += 4
		if (((bs[3][3] == bs[0][0] == bs[2][2]) and bs[3][3] == flag and (not bs[1][1] == alt_flag)) or ((bs[0][0] == bs[1][1] == bs[3][3]) and bs[0][0] == flag 
			and (not bs[2][2] == alt_flag))):
			score += 4
		if (((bs[0][3] == bs[1][2] == bs[3][0]) and bs[0][3] == flag and (not bs[2][1] == alt_flag)) or ((bs[3][0] == bs[2][1] == bs[0][3]) and bs[3][0] == flag 
			and (not bs[1][2] == alt_flag))):
			score += 4	

		#checking for 3 continuous x/o in a column/row/diagonal of the block_status for min player
		for i in range(4):
			if  (((bs[i][0] == bs[i][1] == bs[i][2]) and (bs[i][0] == alt_flag) and (not bs[i][3] == flag)) or ((bs[i][3] == bs[i][1] == bs[i][2]) and (bs[i][3] == alt_flag) 
				and (not bs[i][0] == flag))):
				score -= 4
			if  (((bs[0][i] == bs[1][i] == bs[2][i]) and (bs[0][i] == alt_flag) and (not bs[3][i] == flag)) or ((bs[3][i] == bs[1][i] == bs[2][i]) and (bs[3][i] == alt_flag) 
				and (not bs[i][0] == flag))):
				score -= 4
			if  (((bs[i][0] == bs[i][1] == bs[i][3]) and (bs[i][0] == alt_flag) and (not bs[i][2] == flag)) or ((bs[i][3] == bs[i][0] == bs[i][2]) and (bs[i][3] == alt_flag) 
				and (not bs[i][1] == flag))):
				score -= 4
			if  (((bs[0][i] == bs[1][i] == bs[3][i]) and (bs[0][i] == alt_flag) and (not bs[2][i] == flag)) or ((bs[3][i] == bs[0][i] == bs[2][i]) and (bs[3][i] == alt_flag) 
				and (not bs[i][1] == flag))):
				score -= 4

		if (((bs[3][3] == bs[1][1] == bs[2][2]) and bs[3][3] == alt_flag and (not bs[0][0] == flag)) or ((bs[0][0] == bs[1][1] == bs[2][2]) and bs[0][0] == alt_flag 
			and (not bs[3][3] == flag))):
			score -= 4
		if (((bs[0][3] == bs[1][2] == bs[2][1]) and bs[0][3] == alt_flag and (not bs[3][0] == flag)) or ((bs[3][0] == bs[1][2] == bs[2][1]) and bs[3][0] == alt_flag 
			and (not bs[0][3] == flag))):
			score -= 4
		if (((bs[3][3] == bs[0][0] == bs[2][2]) and bs[3][3] == alt_flag and (not bs[1][1] == flag)) or ((bs[0][0] == bs[1][1] == bs[3][3]) and bs[0][0] == alt_flag 
			and (not bs[2][2] == flag))):
			score -= 4
		if (((bs[0][3] == bs[1][2] == bs[3][0]) and bs[0][3] == alt_flag and (not bs[2][1] == flag)) or ((bs[3][0] == bs[2][1] == bs[0][3]) and bs[3][0] == alt_flag 
			and (not bs[1][2] == flag))):
			score -= 4	
		#print score
		return score

	#def heurestic3()
	def revert(self, board, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguments
		board.board_status[new_move[0]][new_move[1]] = ply
		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0
		board.block_status[x][y]=ply
		return "SUCCESSFUL"

class Manual_Player:
	def __init__(self):
		pass
	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		cells = board.find_valid_move_cells(old_move)
		return cells[random.randrange(len(cells))]

class Board:

	def __init__(self):
		# board_status is the game board
		# block status shows which blocks have been won/drawn and by which player
		self.board_status = [['-' for i in range(16)] for j in range(16)]
		self.block_status = [['-' for i in range(4)] for j in range(4)]

	def print_board(self):
		# for printing the state of the board
		print '==============Board State=============='
		for i in range(16):
			if i%4 == 0:
				print
			for j in range(16):
				if j%4 == 0:
					print "",
				print self.board_status[i][j],
			print 
		print

		print '==============Block State=============='
		for i in range(4):
			for j in range(4):
				print self.block_status[i][j],
			print 
		print '======================================='
		print
		print


	def find_valid_move_cells(self, old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules

		if old_move != (-1,-1) and self.block_status[allowed_block[0]][allowed_block[1]] == '-':
			for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if self.board_status[i][j] == '-':
						allowed_cells.append((i,j))
		else:
			for i in range(16):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
						allowed_cells.append((i,j))
					
			if allowed_cells == []:
				for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
					for j in range(16):
						if self.board_status[i][j] == '-' and self.block_status[i/4][j/4] == '-':
							allowed_cells.append((i,j))
			#print allowed_cells
		return allowed_cells	

	def find_terminal_state(self):
		#checks if the game is over(won or drawn) and returns the player who have won the game or the player who has higher blocks in case of a draw
		bs = self.block_status

		cntx = 0
		cnto = 0
		cntd = 0

		for i in range(4):						#counts the blocks won by x, o and drawn blocks
			for j in range(4):
				if bs[i][j] == 'x':
					cntx += 1
				if bs[i][j] == 'o':
					cnto += 1
				if bs[i][j] == 'd':
					cntd += 1

		for i in range(4):
			row = bs[i]							#i'th row 
			col = [x[i] for x in bs]			#i'th column
			#print row,col
			#checking if i'th row or i'th column has been won or not
			if (row[0] =='x' or row[0] == 'o') and (row.count(row[0]) == 4):	
				return (row[0],'WON')
			if (col[0] =='x' or col[0] == 'o') and (col.count(col[0]) == 4):
				return (col[0],'WON')
		#checking if diagonals have been won or not
		if(bs[0][0] == bs[1][1] == bs[2][2] ==bs[3][3]) and (bs[0][0] == 'x' or bs[0][0] == 'o'):
			return (bs[0][0],'WON')
		if(bs[0][3] == bs[1][2] == bs[2][1] ==bs[3][0]) and (bs[0][3] == 'x' or bs[0][3] == 'o'):
			return (bs[0][3],'WON')

		if cntx+cnto+cntd <16:		#if all blocks have not yet been won, continue
			return ('CONTINUE', '-')
		elif cntx+cnto+cntd == 16:							#if game is drawn
			return ('NONE', 'DRAW')

	def check_valid_move(self, old_move, new_move):
		#checks if a move is valid or not given the last move
		if (len(old_move) != 2) or (len(new_move) != 2):
			return False 
		if (type(old_move[0]) is not int) or (type(old_move[1]) is not int) or (type(new_move[0]) is not int) or (type(new_move[1]) is not int):
			return False
		if (old_move != (-1,-1)) and (old_move[0] < 0 or old_move[0] > 16 or old_move[1] < 0 or old_move[1] > 16):
			return False
		cells = self.find_valid_move_cells(old_move)
		return new_move in cells

	def update(self, old_move, new_move, ply):
		#updating the game board and block status as per the move that has been passed in the arguments
		if(self.check_valid_move(old_move, new_move)) == False:
			return 'UNSUCCESSFUL'
		self.board_status[new_move[0]][new_move[1]] = ply

		x = new_move[0]/4
		y = new_move[1]/4
		fl = 0
		bs = self.board_status
		#print "yo"
		#checking if a block has been won or drawn or not after the current move
		for i in range(4):
			#checking for horizontal pattern(i'th row)
			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
				self.block_status[x][y] = ply
				#self.print_board()
				return 'SUCCESSFUL'
			#checking for vertical pattern(i'th column)
			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
				self.block_status[x][y] = ply
				#self.print_board()

				return 'SUCCESSFUL'

		#checking for diagnol pattern
		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'
		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
			self.block_status[x][y] = ply
			return 'SUCCESSFUL'

		#checking if a block has any more cells left or has it been drawn
		for i in range(4):
			for j in range(4):
				if bs[4*x+i][4*y+j] =='-':
					return 'SUCCESSFUL'
		self.block_status[x][y] = 'd'
		return 'SUCCESSFUL'

def gameplay(obj1, obj2):				#game simulator

	game_board = Board()
	fl1 = 'x'
	fl2 = 'o'
	old_move = (-1,-1)
	WINNER = ''
	MESSAGE = ''
	TIME = 15
	pts1 = 0
	pts2 = 0

	game_board.print_board()
	signal.signal(signal.SIGALRM, handler)
	while(1):
		#player 1 turn
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)

		try:									#try to get player 1's move			
			p1_move = obj1.move(game_board, old_move, fl1)
		except TimedOutExc:					#timeout error
#			print e
			WINNER = 'P2'

			MESSAGE = 'TIME OUT'
			pts2 = 16
			break
		except Exception as e:
			WINNER = 'P2'
			MESSAGE = 'INVALID MOVE'
			pts2 = 16			
			break
		signal.alarm(0)

		#check if board is not modified and move returned is valid
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = 'P2'
			MESSAGE = 'MODIFIED THE BOARD'
			pts2 = 16
			break
		if game_board.update(old_move, p1_move, fl1) == 'UNSUCCESSFUL':
			WINNER = 'P2'
			MESSAGE = 'INVALID MOVE'
			pts2 = 16
			break

		status = game_board.find_terminal_state()		#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':							#if the game has ended after a player1 move, player 1 would win
			pts1 = 16
			WINNER = 'P1'
			MESSAGE = 'WON'
			break
		elif status[1] == 'DRAW':						#in case of a draw, each player gets points equal to the number of blocks won
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			break

		old_move = p1_move
		game_board.print_board()

		#do the same thing for player 2
		temp_board_status = copy.deepcopy(game_board.board_status)
		temp_block_status = copy.deepcopy(game_board.block_status)
		signal.alarm(TIME)

		try:
			p2_move = obj2.move(game_board, old_move, fl2)
		except TimedOutExc:
			WINNER = 'P1'
			print "suhan"

			MESSAGE = 'TIME OUT'
			pts1 = 16
			break
		except Exception as e:
			WINNER = 'P1'
			MESSAGE = 'INVALID MOVE by P2'
			pts1 = 16			
			break
		signal.alarm(0)
		if (game_board.block_status != temp_block_status) or (game_board.board_status != temp_board_status):
			WINNER = 'P1'
			MESSAGE = 'MODIFIED THE BOARD'
			pts1 = 16
			break
		if game_board.update(old_move, p2_move, fl2) == 'UNSUCCESSFUL':
			WINNER = 'P1'
			MESSAGE = 'INVALID MOVE'
			pts1 = 16
			break

		status = game_board.find_terminal_state()	#find if the game has ended and if yes, find the winner
		print status
		if status[1] == 'WON':						#if the game has ended after a player move, player 2 would win
			pts2 = 16
			WINNER = 'P2'
			MESSAGE = 'WON'
			break
		elif status[1] == 'DRAW':					
			WINNER = 'NONE'
			MESSAGE = 'DRAW'
			break
		game_board.print_board()
		old_move = p2_move

	game_board.print_board()

	print "Winner:", WINNER
	print "Message", MESSAGE

	x = 0
	d = 0
	o = 0
	for i in range(4):
		for j in range(4):
			if game_board.block_status[i][j] == 'x':
				x += 1
			if game_board.block_status[i][j] == 'o':
				o += 1
			if game_board.block_status[i][j] == 'd':
				d += 1
	print 'x:', x, ' o:',o,' d:',d
	if MESSAGE == 'DRAW':
		pts1 = x
		pts2 = o
	return (pts1,pts2)



if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Player52 vs. Player52'
		print '                2 => Rand_Func vs. Player52'
		print '                3 => Rand_Func vs. Rand_Func'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player52()
		obj2 = Player52()

	elif option == '2':
		obj2 = Player52()
		obj1 = Manual_Player()
	elif option == '3':
		obj1 = Manual_Player()
		obj2 = Manual_Player()
	else:
		print 'Invalid option'
		sys.exit(1)

	x = gameplay(obj1, obj2)
	print "Player 1 points:", x[0] 
	print "Player 2 points:", x[1]
