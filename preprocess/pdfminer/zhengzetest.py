import re
text='''asdasdas123.21
asdsadsadas

'''
reference='YOLO se-ries [23, 24, 25, 1, 7] always pursuit the optimal speed andaccuracy trade-off for real-time applications. They extract the most advanced detection technologies available at the'

yemei='''
31.1
31.1
133.13
3134.12
YOLOX-SE
YOLXX-L
YOLOX-Tiny
6
7
2133
a
u
asdwdgfea dwdda asd 
'''

reference='asdasdsa [17] asdwa[2] asdw adw'

print(re.sub('\[[\d\,\-\s]+\]','',reference))