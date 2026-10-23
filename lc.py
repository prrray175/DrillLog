import json
from pathlib import Path
'''problems = [
    {
        "id": 1, "title": "两数之和", "topic": "哈希表", "difficulty": "简单",
        "idea": "用字典记录已经遍历过的数", "complexity": "O(n) / O(n)",
        "date": "2026-10-05", "reviewed": False
    },
]'''


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
def judge_id():
        c = 1
        while c == 1:
            print("请输入题号：")
            s = ask()
            idic = []
            for each in problems:
                idic.append(each["id"])
            if s in idic:
                print(f"题号{s}在题集中已经存在，你是否要更新它？")
                t = ask()
                if t == "是":
                    del_problem(problems, s)
                    c = 0
                else:
                    print("请重新输入题号")
            c = 0
        return s

def add_problem():
    s = judge_id()
    while True:
        res = {}
        res["id"] = s
        print("请输入标题：")
        s = ask()
        res["title"] = s
        print("请输入类型：")
        s = ask()
        res["topic"] = s
        print("请输入难度：( easy/medium/hard )")
        while True:
            s = ask()
            if s != 'easy' and s != 'medium' and s != 'hard':
                print("请输入正确的难度。")
                continue
            break
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

def done_():
    print("请输入你要done的题号：")
    index = input()
    nums = find1(index)
    if nums != False:
        print(nums)
        print("已修改为：")
        nums["reviewed"] = 'done'
        print(nums)
    return

def del_():
    print("请输入你要del的题号：")
    index = input()
    find1(index)
    if del_problem(problems, index):
        print("成功删除！")
    else:
        print("删除失败！")
    return

def stat_():
    collections = {}
    level = {'hard': {}, 'medium': {}, 'easy': {}}
    done = 0
    sums = 0
    try:
        for e in problems:
            topic = e["topic"]
            di = e["difficulty"]
            collections[topic] = collections.get(topic, 0) + 1
            level[di][topic] = level[di].get(topic, 0) + 1  # 按照难度统计不同类型题目数量
            sums += 1
            if e['reviewed'] == done:
                done += 1
        for q in collections:
            print(f"{q}类型的题目刷了{collections[q]}道。")
        print()
        for d in ['easy', 'medium', 'hard']:
            total = sum(level[d].values())
            print(f"{d}难度的题目共{total}道")
            for t, n in sorted(level[d].items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"  {t:<8}{n}")
        print(f"已重做的题目数量为：{done}道")
        print(f"一共完成了{sums}道题目，再接再厉！")
    except Exception as e:
        print(type(e).__name__, e)
    return

def find_():
    print("请输入你要查找的关键词或题号： ")
    try:
        key = (input())
        key1 = int(key)
        mode = "id"
    except ValueError:
        mode = "text"
    res = find(key, mode)
    try:
        if not res or res[0] == False:
            print("没有找到。")

        else:
            for i in range(len(res)):
                print(res[i])

    except Exception as e:
        print(type(e).__name__, e)

def judge():
    while True:#只有输入命令为'quit'时才会退出
        requires = order()
        for each in requires:
            if each == "add":
                add_problem()
            elif each == "quit":
                return
            elif each == "list":
                show(each)
            elif each == "done":
                done_()
            elif each == "del":
                del_()
            elif each == "stat":
                stat_()
            elif each == "find":
                find_()
            else:
                print("未知命令")

def order(): #命令输入行
    while True:
        try:
            require = input().split() #这里的命令是一连串的，其实不太合理，后期要修改
            return require
        except EOFError:
            print("输入流无可输出内容，请重新输入命令。")

def show(command):#打印的流程都在这里
    if command == "list":
        for i in problems:
            print(f"id: {i['id']:<4} topic: {i['topic']:<10} ")
def find(k,mode):
    res = []
    if mode =="text":
        for p in problems:
            if k in p["topic"] or k in p['idea']:
                res.append(p)
    else:
        res.append(find1(k))
    return res

def find1(index):#找题号为index的数据
    for k in problems:
        if k["id"] == index:
            return k
    else:
        print("你输入的题号不存在。")
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



print("请输入命令，输入quit结束程序。")
problems = []
p = Path("problems.json")
if not p.exists():
    p.write_text("[]", encoding="utf-8")
try:
    problems = load()#读取json文件中的数据
except json.decoder.JSONDecodeError:
    print("json文件语法错误！")
except UnicodeDecodeError:
    print("json文件编码错误! ")
judge()
print("程序即将退出，数据已保存")
save(problems)