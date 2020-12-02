from itertools import combinations
## 로또번호 세트 개수 (고정)
lottery_set = 6
## 뽑힐거 같은 번호 모아놓기
perspect_nums = [1, 3, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 28, 30, 31, 35]

## nCm 패턴
comb = combinations(perspect_nums, lottery_set)

### 모든 조합 출력해보기
'''
for i in list(comb):
    print(i)
'''
## 모든 조합 text file 만들기 ##
f = open('combination_reslut.txt', mode='wt', encoding='utf-8')

for i in list(comb):
    f.write(str(i)+'\n')
f.close()