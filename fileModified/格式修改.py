import re

file_path = "../file/超神机械师.txt"

with open(file_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        obj = re.match(r'^[0-9]+', line)
        if obj:
            # print(obj.group())
            # print(re.sub(r'^[0-9]+',"第"+obj.group()+"章",line))
            line = re.sub(r'^[0-9]+', "第" + obj.group() + "章", line)
        print(line)
        with open('../file/超神机械师1.txt', 'a',encoding="utf-8") as f:
            f.write(str(line))

