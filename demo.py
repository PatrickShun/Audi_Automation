l1 = '2022年元旦是2022年1月1日， 农历十一月二十九。'
l2 = '2022年元旦是2022年1月1日, 农历十一月二十九.'
a1 = '2022年龙抬头是2022年3月4日, 农历二月初二.'
a2 = '2022年龙抬头是2022年1月1日, 农历十一月二十九.'

l1 = l1.replace('，',',').replace('。','.').replace(' ','')
l2 = l2.replace('，',',').replace('。','.').replace(' ','')

print(l1,l2)
if l1 == l2:
    print('pass')