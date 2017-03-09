import curses #curses工作在屏幕，窗口和子窗口之上。屏幕是设备全部可用显示面积（对终端是该窗口内所有可用字符位置），窗口与具体例程有关。如基本的stdscr窗口等。
from random import randrange, choice  #随机函数库
from collections import defaultdict	#collections是Python内建的一个集合模块，提供了许多有用的集合类。

#random.randrange
#从指定范围内，按指定基数递增的集合中 获取一个随机数。如：random.randrange(10, 100, 2)，结果相当于从[10, 12, 14, 16, ... 96, 98]序列中获取一个随机数。

#random.choice
#从序列中获取一个随机元素。参数sequence表示一个有序类型。这里要说明 一下：sequence在python不是一种特定的类型，而是泛指一系列的类型。list, tuple, 字符串都属于sequence。

#random.shuffle
#用于将一个列表中的元素打乱。

#用户操作行为

actions 	=	['Up', 'Left', 'Down', 'Right',  'Restart',  'Exit']

#用户输入键

letter_codes=	[ord(ch) for ch in 'WASDRQwasdrq']

#将行为和输入键绑定为一个dict
#zip函数接受任意多个（包括0个和1个）序列作为参数，返回一个tuple列表
actions_dict=	dict(zip(letter_codes, actions*2))



#状态机   在游戏中  在当前状态 进行操作 转变为另外的状态

def main(stdscr):

	def init():
		return "Game"	#重置游戏棋盘

	def not_game(state):
		responses 	=	defaultdict(lambda:state)	#默认是当前状态 ，没有行为就会一直处于这个状态
		responses['Restart'],	responses['Exit']	=	'Init', 'Exit'
		return responses[action]

	def game():
		#画出当前棋盘状态
		#读取用户输入得到的action
		if action == 'Restart':
			return 'Init'

		if action == 'Exit':
			return 'Exit'

		# if 移动了一步	#游戏移动

		# 	if 胜利了
		# 		return 'Win'	#游戏胜利

		# 	if 失败了

		# 		return 'Gameover'	#游戏结束

		return 'Game'	#游戏中



	state_actions 	=	{
		'Init'	:	init,
		'Win'	:	lambda:not_game('Win'),
		'Gameover'	:	lambda:not_game('Gameover'),
		'Game'	:	game
	}

	state 	=	"Init"

	while state != 'Exit':
		state 	=	state_actions[state]()


def get_user_action(keyboard):
	char 	=	"N"
	while char not in actions_dict:
		char 	=	keyboard.getch()# ????
	return actions_dict[char]


def transpose(field):
	return [list(row) for row in zip(*field)]	#矩阵转置  ？？

def invert(field):
	return [row[::-1] for row in field]	#矩阵逆转 ？？    seq[start:end:step]   重开始到结束切片的间隔 负数只表示倒叙



# invert  矩阵逆转  表示  把横排转换为竖排 or  反过来       下面例子 括号里面表示坐标 外面表示坐标的值
# 1(1, 1)   2(1, 2)  3(1, 3)

# 1(1, 1)

# 2(2, 1)

# 3(3, 1)


#transpose  矩阵转置  定义A的转置为这样一个n×m阶矩阵B，满足B=a(j,i)，即 b (i,j)=a (j,i)（B的第i行第j列元素是A的第j行第i列元素），记A'=B。(有些书记为AT=B，这里T为A的上标）  大学数学知识

	

# l 	=	[(1, 1), (1, 2), (1, 3)]
# print(l)
# # print(transpose(l))
# print(invert(l))

# print(randrange(1, 10, 3))

# print(randrange(100))

#创建棋盘

class GameFiled(object):
	def __init__(self, height = 4, width = 4, win = 2048):
		self.height 	=	height
		self.width 		=	width
		self.win_value	=	win #胜利的分数
		self.score 		=	0	#当前分数
		self.highscore 	=	0	#最高分
		self.reset()

	def spawn(self):#随机生成一个2 或者 4
		new_element 		=	4 if randrange(100) > 89 else 2 	#随机取出一个1到100 直接的数 判断和89的大小（89自定义 想写多少就多少 就看是想出4的概率和出2的概率）
		(i, j) 				=	choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])#循环棋盘坐标  随机返回一个 没有值或者值为0 的坐标  然后把刚生成的随机数 赋值给这个坐标
		self.field[i][j]	=	new_element;


	def reset(self):#重置棋盘
		if self.score > self.highscore :
			self.highscore 	=	 self.score
		self.score 		=	0;
		self.field		=	[[0 for i in range(self.width) for j in range(self.height)]]

		self.spawn()
		self.spawn()	#重置的时候 随机生成2个数

	def move(self, direction):

		def move_row_left(row):

			def tighten(row):	#把零散的非0单元 挤一块

				new_row 	=	[i for i in row if i != 0]
				new_row 	+=	[0 for i in range(len(row) - len(new_row))]

				return new_row

			def merge(row):	#相邻元素一样的合并

				pair 	=	False
				new_row =	[]

				for i in range(len(row)):
					if pair:
						new_row.append(2 * row[i])
						self.score 	+=	2 * row[i]
						pair 	=	False
					else:
						if i + 1 < len(row) and row[i] == row[i +  1]:
							pair 	=	True
							new_row.append(0)
						else:
							new_row.append(row[i])

				assert len(new_row) == len(row)
				return new_row

			return tighten(merge(tighten(row)))

		moves 	=	{}
		moves['Left']	=	lambda field:[move_row_left[row] for row in field]
		moves['Right']	=	lambda field:invert[moves['Left'](invert(field))]
		moves["Up"]		=	lambda field:transpose[moves['Left'](transpose(field))]
		moves["Down"]	=	lambda field:transpose[moves['Right'](transpose(field))]



























