#!/usr/bin/env python
#coding:utf-8
from collections import deque
import copy, time
ROW = "ABCDEFGHI"
COL = "123456789"
#functions for solve2 are defined here
#------------------------------------------
row_map = {}
col_map = {}
cell_map = {}
#initialize the three maps
def init_map(sudoku):
	for i in ROW:
		row_map[i] = {}
		for k in range(1,10):
			row_map[i][k] = False
	for j in COL:
		col_map[j] = {}
		for k in range(1, 10):
			col_map[j][k] = False
	#the index for cell_map is 3*row_index+col_index
	for i in range(9):
		cell_map[i] = {}
		for k in range(1, 10):
			cell_map[i][k] = False
	for i in ROW:
		for j in COL:
			value = sudoku[i+j]
			if sudoku[i+j] == 0:
				continue
			row_map[i][value] = True
			col_map[j][value] = True
			row_index = ord(i) - ord('A')
			col_index = ord(j) - ord('1')
			row_index = row_index / 3
			col_index = col_index / 3
			key = row_index * 3 + col_index
			cell_map[key][value] = True
#to count the domain of each cell based on three maps information
def count(sudoku, cell):
	count = 0
	start_row = cell[0]
	start_col = cell[1]
	row_index = (ord(start_row) - ord('A')) / 3
	col_index = (ord(start_col) - ord('1')) / 3
	cell_key = row_index*3+col_index
	for x in range(1, 10):
		if row_map[start_row][x] or col_map[start_col][x] or cell_map[cell_key][x]:
			continue
		else:
			count = count + 1
	return count
#get the next cell for dfs call
def next2(sudoku):
	min_count = 10
	min_cell = ""
	for i in ROW:
		for j in COL:
			if sudoku[i+j] == 0:
				this_count = count(sudoku, i+j)
				if this_count < min_count:
					min_count = this_count
					min_cell = i+j
	return min_cell
#the dfs function for solution2
def dfs2(sudoku, start):
	if start == "":
		return True
	start_row = start[0]
	start_col = start[1]
	row_index = (ord(start_row) - ord('A')) / 3
	col_index = (ord(start_col) - ord('1')) / 3
	cell_key = row_index*3+col_index
	if sudoku[start] == 0:
		for x in range(1, 10):
			if row_map[start_row][x] or col_map[start_col][x] or cell_map[cell_key][x]:
				continue
			sudoku[start] = x
			row_map[start_row][x] = True
			col_map[start_col][x] = True
			cell_map[cell_key][x] = True
			next_cell = next2(sudoku)
			if dfs2(sudoku, next_cell):
				return True
			#backtracking, set beack the value of sudoku and three maps
			sudoku[start] = 0
			row_map[start_row][x] = False
			col_map[start_col][x] = False
			cell_map[cell_key][x] = False
	return False
#could be called to invoke solution2
def solve2(f, sudoku):
	start = next2(sudoku)
	if dfs2(sudoku, start):
		printSudoku(sudoku)
		writeSudoku(f, sudoku)
		return True
	else:
		return False
#------------------------------------------
# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	
def writeSudoku(f,sudoku):
	f.write("-----------------\n")
	for i in ROW:
		for j in COL:
			f.write(str(sudoku[i+j]))
			f.write(" ")
		f.write("\n")
def printdomain(domain):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print domain[i + j][0],
		print ""	

def build_domain(sudoku):
	domain = {}
	for key, value in sudoku.iteritems():
		if value is 0:
			domain[key] = [1,2,3,4,5,6,7,8,9]
		else:
			domain[key] = [value]
	return domain
#used to test the validation of the domain of AC3
def valid(domain):
	for key, value in domain.iteritems():
		if len(value) < 1 or len(value) > 1:
			return False
	return True
#initialize the queue in AC3
def init_queue():
	queue = deque()
	for i in ROW:
		for j in COL:
			augment_queue(queue, i+j)
	return queue
#add constraint related to one cell into the queue
def augment_queue(queue, arc):
	arc_row = arc[0]
	arc_col = arc[1]
	for i in ROW:
		if i != arc_row:
			queue.append((i+arc_col, arc))
	for j in COL:
		if j != arc_col:
			queue.append((arc_row+j, arc))
	row_index = ord(arc_row) - ord('A')
	col_index = ord(arc_col) - ord('1')
	row_index = row_index / 3
	col_index = col_index / 3
	for i in range(3*row_index, 3*row_index+3):
		for j in range(3*col_index, 3*col_index+3):
			if ROW[i] != arc_row and COL[j] != arc_col:
				queue.append((ROW[i]+COL[j], arc))
#forward checking used in backtracking
def forward_check(sudoku, domain, start):
	#check consistency, and update domain of neighbour
	start_row = start[0]
	start_col = start[1]
	#check value validation in this row
	for i in ROW:
		if i != start_row:
			if sudoku[i+start_col] == 0:
				temp_list = domain[i+start_col]
				if sudoku[start] in temp_list:
					temp_list.remove(sudoku[start])
					#no value possible for that cell, conflict!
					if len(temp_list) == 0:
						return False
					else:
						domain[i+start_col] = temp_list
			elif sudoku[start] == sudoku[i+start_col]:
				return False
	#check value validation in this column
	for j in COL:
		if j != start_col:
			if sudoku[start_row+j] == 0:
				temp_list = domain[start_row+j]
				if sudoku[start] in temp_list:
					temp_list.remove(sudoku[start])
					if len(temp_list) == 0:
						return False
					else:
						domain[start_row+j] = temp_list
			elif sudoku[start] == sudoku[start_row+j]:
				return False
	#check value validation in this box
	row_index = ord(start_row) - ord('A')
	col_index = ord(start_col) - ord('1')
	row_index = row_index / 3
	col_index = col_index / 3
	for i in range(3*row_index, 3*row_index+3):
		for j in range(3*col_index, 3*col_index+3):
			if ROW[i] != start_row and COL[j] != start_col:
				key = ROW[i] + COL[j]
				if sudoku[key] == 0:
					temp_list = domain[key]
					if sudoku[start] in temp_list:
						temp_list.remove(sudoku[start])
						if len(temp_list) == 0:
							return False
						else:
							domain[key] = temp_list
				elif sudoku[start] == sudoku[key]:
					return False
	return True
#AC3 algorithm to reduce the domain complexity
def AC3(domain):
	queue = init_queue()
	while queue:
		arc = queue.pop()
		if remove(arc, domain):
			augment_queue(queue, arc[0])
def remove(arc, domain):
	removed = False
	# print arc
	x_list = domain[arc[0]]
	y_list = domain[arc[1]]
	if len(y_list) == 1 and y_list[0] in x_list:
		removed = True
		x_list.remove(y_list[0])
	domain[arc[0]] = x_list
	return removed
#get next minimal available cell, return "" if all set
def next(sudoku, domain):
	min_len = 10
	min_key = ""
	for i in ROW:
		for j in COL:
			key = i+j
			if sudoku[key] != 0:
				continue
			value = domain[key]
			if len(value) < min_len:
				min_len = len(value)
				min_key = key
	return min_key
#backtracing dfs call in solution1
def dfs(sudoku, domain, start):
	# print start
	if start == "":
		return True
	#if all set, return true
	for x in domain[start]:
		domain_copy = copy.deepcopy(domain)
		sudoku[start] = x
		domain_copy[start] = [x]
		if not forward_check(sudoku, domain_copy, start):
			continue
		next_cell = next(sudoku, domain)
		if dfs(sudoku, domain_copy, next_cell):
			return True
	#enter here, no solution found, return False
	sudoku[start] = 0
	return False
#solution1
def solve(f, sudoku, domain):
	print "solving..."
	start = next(sudoku, domain)
	if dfs(sudoku, domain, start):
		printSudoku(sudoku)
		writeSudoku(f, sudoku)
		return True
	else:
		print "No solution"
		return False

if __name__ == "__main__":
	try:
		f = open("sudokus.txt", "r")
		f_out = open("output.txt", "w")
		sudokuList = f.read()
	# 1.5 count number of sudokus solved by AC-3
	# write your AC3 algorithms here, update num_ac3_solved	
		num_ac3_solved = 0
		for line in sudokuList.split("\n"):
			# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
			sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
			domain = build_domain(sudoku)
			AC3(domain)
			if (valid(domain)):
				num_ac3_solved = num_ac3_solved + 1
				printdomain(domain)
		print num_ac3_solved
	# 1.6 solve all sudokus by backtracking
		count_solved = 0
		start_time = time.time()
		for line in sudokuList.split("\n"):
			# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
			sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
			#if you want to run solution2, just comment out the solution1 code and uncomment the solution2 code
			#solution 1
			domain = build_domain(sudoku)
			AC3(domain)
			if solve(f_out, sudoku, domain):
				count_solved = count_solved + 1

			#solution 2
			# init_map(sudoku)
			# if solve2(f_out, sudoku):
			# 	count_solved = count_solved + 1
		print "time is ",
		print time.time() - start_time
		print "count is "+str(count_solved)
	except Exception as e:
		print e
		exit()
