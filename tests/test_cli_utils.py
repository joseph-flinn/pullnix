from src.cli.utils import transform, get_column_widths, format_table, dicts2table


def test_transform():
    data_1 = [
        ['a', 'b'],
        ['c', 'd']
    ]
    data_2 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    assert transform([[]]) == [[]]

    assert transform(data_1) == [
        ['a', 'c'],
        ['b', 'd']
    ]
    assert transform(data_2) == [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9]
    ]


def test_get_column_widths():
    table0 = [
        ["", "", ""]
    ]

    table1 = [
        ["     ", "     ", "     "]
    ]

    table2 = [
        ["City", "State", "Population"],
        ["Spokane", "Washington", "229,071"],
        ["Belgrade", "Montana", "11,608"]
    ]

    assert get_column_widths(table0) == [0, 0, 0]
    assert get_column_widths(table1) == [5, 5, 5]
    assert get_column_widths(table2) == [8, 10, 10]


def test_format_table():
    table0 = [
        ["a", "b", "c"],
        ["d", "e", "f"],
        ["g", "h", "i"]
    ]
    table1 = [
        ["City", "State", "Population"],
        ["Spokane", "Washington", "229,071"],
        ["Belgrade", "Montana", "11,608"]
    ]
    assert format_table(table0) == "| a | b | c |\n| d | e | f |\n| g | h | i |"
    assert format_table(table1, has_header=True) == "|     City |      State | Population |\n|----------|------------|------------|\n|  Spokane | Washington |    229,071 |\n| Belgrade |    Montana |     11,608 |"


def test_dicts2table():
    data0 = [
        {"City": "Spokane", "State": "Washington", "Population": "229,071"},
        {"City": "Belgrade", "State": "Montana", "Population": "11,608"},
    ]

    assert dicts2table(data0) == [
        ["City", "State", "Population"],
        ["Spokane", "Washington", "229,071"],
        ["Belgrade", "Montana", "11,608"]
    ]

