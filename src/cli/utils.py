import typing as t


def transform(data: t.List[t.List]) -> t.List[t.List]:
    if data == [[]]:
        return [[]]

    data_c = []
    for col_idx in range(len(data[0])):
        column = []
        for row in data:
            column.append(row[col_idx])
        data_c.append(column)
    return data_c


def get_column_widths(table: t.List[t.List]) -> t.List[int]:
    data_c = transform(table)
    return [max(map(len, cell)) for cell in data_c]


def format_table(table: t.List[t.List], has_header=False) -> str:
    widths = get_column_widths(table)

    formatted_table = []

    def to_table_row(widths: t.List[int], row: t.List[str]) -> str:
        line = ["|"]
        for index, cell in enumerate(row):
            line.append(f" {cell.rjust(widths[index], ' ')} |")
        return ''.join(line)

    if has_header:
        data = table[1:]
        formatted_table.append(to_table_row(widths, table[0]))
        break_line = ["|"]
        for index, column_name in enumerate(table[0]):
            break_line.append(f"{'-'*(widths[index] + 2)}|")
        formatted_table.append(''.join(break_line))
    else:
        data = table

    for row in data:
        formatted_table.append(to_table_row(widths, row))

    return "\n".join(formatted_table)


def dicts2table(data: t.List[dict]) -> t.List[t.List]:
    table_data = []
    if len(data) > 0:
        header = data[0].keys()
        table_data.append(list(header))

        for row in data:
            table_data.append(list(row.values()))
        return table_data
    return [[]]
