'''
Vincent's Python 

——python知识星球02_杨辉三角
010
0110
01210
013310

'''
#n = int(input('请输入：'))

'''
杨辉三角思路
num为需要显示的层数，也代表该层有多少不为0的整数
before为上一层，初始值设定为1层[0，1，0]
after为下一层

1.(调试阶段暂未设置)判断num=1，直接输入，num>1, 进入循环

2.层计算循环(内循环)：after_l第n的一个值等于before_l(n-1)+before_l(n)

3.(外循环)：层计算完毕之后，使before_l=after_l，让before_l等于新一层的参数进入下次计算，
            再在before_l后加0，输出before_l，
循环
'''

num = 4   #输入需要显示的层数，测试阶段设置为固定值

before_l = [0, 1, 0]  #设置初始值，也就是第一层的参数
after_l = [0, 0, 0,]	#设计新层位，防止取位出错


for i in range(1,num):		#外循环，因为第一层直接输入，由于第一层是直接输入，所以第num层只需要num-1次循环，所以从1开始循环，总次数=num-1次
	print('外循环%s' % (i))

	for x in range((i+1)):		#内循环：第num层就有num个非零整数，需要循环num次计算
		after_l[(x+1)] = before_l[x] + before_l[(x+1)]		#内循环：新层(x+1)位=上层x位+上层(x+1)位
		print('内循环%s次后after=%s，	before=%s' % ((x), after_l, before_l))		#观察每次内循环计算结果

	print('第%s次内循环全部结束后，after=%s，before=%s' % ((i), after_l, before_l))		#观察一次内循环后初始结果
	before_l = after_l				#before装入新的after值
	before_l.append(0)				#新的before_l末位添加0，避免下次内循环
	#after_l.append(0)				#新的aftre_l末位添加0，避免下次内循环
	print('第%s次外循环加0后，after=%s，before=%s \n\n ' % ((i), after_l, before_l))	

'''
求和部分，上面的不对暂时没用
for ele in range(before_l):			#第num行求和
	sum += ele
print('第%s行和为：%s' %(num, sum))
'''
	
