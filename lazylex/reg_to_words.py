import traceback


class Analyser:
    escape_dict = {
        r"\e": "ε",
        r"\(": "(",
        r"\)": ")",
        r"\.": ".",
        r"\|": "|",
        r"\*": "*",
        r"\\": "\\",
        r"\n": "\n",
        r"\t": "\t",
        r"\r": "\r",
        r"\f": "\f",
        r"\v": "\v"
    }

    unescape_dict = {
        "\n": r"\n",
        "\t": r"\t",
        "\r": r"\r",
        "\f": r"\f",
        "\v": r"\v"
    }

    @staticmethod
    def split_by_escape(expr: str) -> list[str]:
        # 将字符串切割成单个字符，但转义字符和其后的字符将会连接在一起。
        ret = []
        escaping = False
        for ch in expr:
            if escaping:
                ret.append("\\" + ch)
                escaping = False
            elif ch != "\\":
                ret.append(ch)
            else:
                escaping = True
        if escaping:
            raise ValueError("意外结束的转义字符。")
        return ret

    @staticmethod
    def escape(ch: str) -> str:
        if ch in Analyser.escape_dict:
            return Analyser.escape_dict[ch]
        return ch

    @staticmethod
    def unescape(ch: str) -> str:
        if ch in Analyser.unescape_dict:
            return "'" + Analyser.unescape_dict[ch] + "'"
        return repr(ch)

    @staticmethod
    def analyse(expr: str) -> list[str]:
        return Analyser.split_by_escape(expr)


if __name__ == "__main__":
    analyser = Analyser()
    expr_str = input("输入正规表达式：\n")
    try:
        words = analyser.analyse(expr_str)
        print("单词串为：")
        print(words)
    except ValueError as err:
        print("匹配失败。")
        traceback.print_exc()
