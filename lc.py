import json
import os
from pathlib import Path
import unicodedata


DATA_DIR = Path(os.getenv("APPDATA")) / "DrillLog"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = DATA_DIR / "problems.json"

old = Path("problems.json")
if old.exists() and not DATA_FILE.exists():
    DATA_FILE.write_bytes(old.read_bytes())

'''problems = [
    {
        "id": 1, "title": "两数之和", "topic": "哈希表", "difficulty": "简单",
        "idea": "用字典记录已经遍历过的数", "complexity": "O(n) / O(n)",
        "date": "2026-10-05", "reviewed": False
    },
]'''

def dw(s):#计算每个字符需要占的格数
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)

def row(cmd, desc, w=18):#cmd:命令名 desc:说明，w = 18 默认宽度参数
    return f"  {cmd}{' ' * (w - dw(cmd))}{desc}"

def load(): #从json中读取数据
    with open(DATA_FILE, 'r', encoding= 'utf-8') as f:
         return json.load(f)
def save(problem): #保存数据回json
    with open(DATA_FILE, 'w', encoding= 'utf-8')as f:
        json.dump(problem, f, ensure_ascii=False, indent=4)
def ask():
    while True:
        require1 = input()
        if not require1.strip():
            print("请输入内容，空格不能作为有效输入。")
        else:
            return require1
def judge_id():
        while True:
            print("请输入题号：")
            s = ask()
            if any(p["id"] == s for p in problems):
                print(f"题号{s}在题集中已经存在，你是否要更新它？")
                t = ask()
                if t == "是":
                    del_problem(problems, s)
                    return s
                else:
                    print("请重新输入题号")
                    continue
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
        save(problems)
        print("是否继续添加题目？")
        s = ask()
        if s == "是":
            continue
        else:
            break

def done_(args = None):
    if args == None:
        print("请输入你要done的题号：")
        args = input()
    nums = find1(args)
    if nums != False:
        print("已修改为：")
        nums["reviewed"] = 'done'
        print(nums)
        save(problems)
    return

def del_(args = None):
    if not args:
        print("请输入你要del的题号：")
        args = input().split()
    for each in args:
        find1(each)
        if del_problem(problems, each):
            print(f"{each}号题成功删除！")
            save(problems)
        else:
            print(f"{each}题删除失败！")

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
            if e['reviewed'] == "done":
                done += 1
        for q in collections:
            print(row(f"{q}类型的题目刷了",f"{collections[q]}道",23))
        print()
        for d in ['easy', 'medium', 'hard']:
            total = sum(level[d].values())
            print(row(f"{d}难度的题目共:", f"{total}道",23))
            '''for t, n in sorted(level[d].items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"  {t:<8}{n}")'''
        print(row(f"已重做的题目数量为：",f"{done}道",23))
        print(f"一共完成了{sums}道题目，再接再厉！")
    except Exception as e:
        print(type(e).__name__, e)
    return

def find_(key = None):
    if key is None:
        print("请输入你要查找的关键词或题号： ")
        key = input()
    try:
        int(key)
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

def help_():
    print()
    print("添加与修改")
    print(row("add","添加一道题"))
    print(row("done <题号>","标记为重做(例如done 15)"))
    print(row("del <题号>","删除一条记录(例如del 15)"))
    print()
    print("查询")
    print(row("list[类型]","列出全部题目/只看某一类型的题目"))
    print(row("find<关键词/题号>","搜索题目"))
    print()
    print("其他")
    print(row("stat","统计已做题目难度与类型"))
    print(row("help/quit","查看帮助/退出"))
    print(row("save", "保存"))
    print()
def judge():
    while True:#只有输入命令为'quit'时才会退出
        print("请输入命令，输入quit结束程序。")
        each, args = order()
        if each == "add":
            add_problem()
        elif each == "quit":
            return
        elif each == "list":
            show(args[0] if args else None)
        elif each == "done":
            done_(args[0] if args else None)
        elif each == "del":
            del_(args)
        elif each == "stat":
            stat_()
        elif each == "find":
            find_(args[0] if args else None)
        elif each == "help":
            help_()
        elif each == "save":
            save(problems)

        else:
            print("未知命令，输入help可查看帮助。")

def order(): #命令输入行
    while True:
        try:
            require = input().split()
            if not require:
                continue
            return require[0], require[1:]
        except EOFError:
            return "quit", []

def show(args = None):#打印的流程都在这里
    if not problems:
        print("题库中无数据！")
        return
    if args == None:
        print(row("题号","类型",20))
        print()
        for i in problems:
            print(row(i["id"],i["topic"],20))
    else:
        for i in problems:
            if  i["id"] == args or args in i["topic"] or args in i["idea"]:
                print(i)
def find(k,mode):
    if mode == "id":
        p = find1(k)
        return [] if p is False else [p]
    return [p for p in problems if k in p["topic"] or k in p["idea"]]

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




def backup_broken_file():
    backup = DATA_FILE.with_name("problems.broken.json")
    try:
        backup.write_bytes(DATA_FILE.read_bytes())
        print(f"原文件已备份到：{backup}")
    except OSError as e:
        print(f"备份失败：{e}")

problems = []
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]", encoding="utf-8")
try:
    problems = load()#读取json文件中的数据
except json.decoder.JSONDecodeError:
    print("json文件语法错误！")
    backup_broken_file()
    print("本次从空题库开始，修复后可参考备份文件恢复。")
except UnicodeDecodeError:
    print("json文件编码错误！")
    backup_broken_file()
    print("本次从空题库开始，修复后可参考备份文件恢复。")
try:
    judge()
except KeyboardInterrupt:
    print()
except Exception as e:
    print("程序出错：", type(e).__name__, e)
finally:
    save(problems)
