f = open('C:\PythonProgram\score.txt', 'r', encoding='utf-8')

#with open(file_path) as f:
lines = f.readlines()

lines = [line.rstrip('\n') for line in lines]
print(lines)
list_int = list(map(int, lines)) # 정수로 변환
print(max(list_int))
f.close