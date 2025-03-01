# TODO: покрыть логами
# TODO: отрефакторить
# TODO: покрыть тестами

def parse_select_query(query_str: str) -> tuple[str, list, str]:
    ENDED = True
    columns: list[str] = []
    keyword = ""
    table = ""
    condition = ""

    if query_str[-1] != ";":
        ENDED = False

    if ENDED:
        query = query_str[:-1].split(" ")
    else:
        query = query_str.split(" ")

    print(query)

    if query[0] != "SELECT":
        print("Запрос должен начинаться с SELECT")
        return (table, columns, condition)

    for i in range(0, len(query)):
        query_part = query[i]

        if query_part == "":
            continue

        elif query_part == "SELECT":
            if keyword == "":
                keyword = "SELECT"
                continue
            else:
                print("Запрос должен содержать только одно ключевое слово SELECT")
                return (table, columns, condition)

        elif query_part == "FROM":
            if keyword == "SELECT":
                keyword = "FROM"
                continue
            else:
                print("В запросе должно содержаться ровно одно ключевое слово FROM, находящееся после SELECT")
                return (table, columns, condition)

        elif query_part == "WHERE":
            if keyword == "FROM":
                keyword = "WHERE"
                continue
            else:
                print("В запросе должно быть ровно одно ключевое слово WHERE, стоящее после FROM")
                return (table, columns, condition)

        else:
            if keyword == "SELECT":
                if query_part[-1] == ",":
                    columns.append(query_part[:-1])
                else:
                    columns.append(query_part)
            elif keyword == "FROM":
                if (i != len(query) - 1) and (query[i+1] != "WHERE"):
                    print("После указания имени таблицы запрос должен либо заканчиваться, либо должно идти ключевое слово WHERE")
                    return (table, columns, condition)
                else:
                    table = query_part
            elif keyword == "WHERE":
                if condition == "":
                    delimiter = ""
                else:
                    delimiter = " "
                condition = delimiter.join((condition, query_part))
    return (table, columns, condition)
