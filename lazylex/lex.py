import dill

if __name__ == "__main__":
    pickle_filename = input("输入词法器模型路径(xxx.lexer)：\n")
    with open(pickle_filename, "rb") as file:
        analyser = dill.load(file)
    expr_filename = input("输入待匹配文件路径：\n")
    with open(expr_filename, "r", encoding="utf-8") as file:
        program = file.read()

    ans = analyser.analyse(program)
    print("匹配成功。")

    out_filename = input("输入分析结果文件路径(xxx.tokens)：\n")
    with open(out_filename, "w", encoding="utf-8") as file:
        for token in ans:
            file.write(str(token) + "\n")
