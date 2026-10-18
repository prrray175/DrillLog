import json
from pathlib import Path
'''problems = [
    {
        "id": 1, "title": "两数之和", "topic": "哈希表", "difficulty": "简单",
        "idea": "用字典记录已经遍历过的数", "complexity": "O(n) / O(n)",
        "date": "2026-10-05", "reviewed": False
    },
]'''
print("请输入命令，输入quit结束程序。")
problems = []
p = Path("problems.json")
if not p.exists():
    p.write_text("[]", encoding="utf-8")

def load(): #从json中读取数据
    with open("problems.json", 'r', encoding= 'utf-8') as f:
         return json.load(f)

def save(problem): #保存数据回json
    with open('problems.json', 'w', encoding= 'utf-8')as f:
        json.dump(problem, f, ensure_ascii=False, indent=4)
def ask():
    while True:
        require1 = input()
        if not require1.strip():
            print("请输入内容，空格不能作为有效输入。")
        else:
            return require1
def order(): #命令判断行
    while True:
        try:
            require = input().split() #这里的命令是一连串的，其实不太合理，后期要修改
        except EOFError:
            print("输入流无可输出内容，请重新输入命令。")
        try:
            for each in require:
                if each == "add":
                    while True:
                        res = {}
                        while True:
                            print("请输入题号：")
                            s = ask()
                            if s in idic:
                                print(f"题号{s}在题集中已经存在，你是否要更新它？")
                                t = ask()
                                if t == "是":
                                    del_problem(problems, s)
                                    break
                                else:
                                    print("请重新输入题号")
                        res["id"] =s
                        print("请输入标题：")
                        s = ask()
                        res["title"] = s
                        print("请输入类型：")
                        s = ask()
                        res["topic"] = s
                        print("请输入难度：")
                        s = ask()
                        res["difficulty"] = s
                        print("请输入你的解题思路：")
                        s = ask()
                        res["idea"] = s
                        res["reviewed"] = False
                        problems.append(res)
                        print("添加题目成功！")
                        print("是否继续添加题目？")
                        s = ask()
                        if s == "是":
                            continue
                        else:
                            break
                elif each == "quit":
                        raise
                elif each == "list":
                    show(each)
                elif each == "done":
                    print("请输入你要done的题号：")
                    index = input()
                    nums = find(index)
                    if nums != False:
                        print(nums)
                        print("已修改为：")
                        nums["reviewed"] = 'done'
                        print(nums)
                elif each == "del":
                    print("请输入你要del的题号：")
                    index = input()
                    find(index)
                    if del_problem(problems, index):
                        print("成功删除！")
                    else:
                        print("删除失败！")
                else:
                    print("未知命令")
        except:
                print("数据已保存，程序已退出。")
                break

def show(command):#打印的流程都在这里
    if command == "list":
        for i in problems:
            print(f"id: {i['id']:<4} title: {i['title']:<10} topic: {i['topic']:<10} difficulty: {i["difficulty"]:<10} reviewed: {str(i['reviewed']):<10} \n idea: {i['idea']}")

def find(index):#找题号为index的数据
    for k in problems:
        if k["id"] == index:
            return k
    else:
        print("你输入的题号不存在！")
        return False
def add_reviewed(problem):
    changed = 0
    for p in problem:
        if "reviewed" not in p:
            p["reviewed"] = False
            changed += 1

    return changed

def del_problem(problem, index):
    kept = [p for p in problem if p["id"] != index]
    if len(kept) == len(problem):
        print("题号不存在！")
        return False
    else:
        problem[:] = kept
        return True
try:
    problems = load()#读取json文件中的数据
except json.decoder.JSONDecodeError:
    print("json文件语法错误！")
except UnicodeDecodeError:
    print("json文件编码错误! ")
idic = []
for each in problems:
    idic.append(each["id"])
order()

save(problems)