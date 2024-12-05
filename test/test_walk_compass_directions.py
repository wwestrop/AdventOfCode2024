from src.util.matrix import walk_compass_directions


def test_walk_compass_happy_path():
    matrix = [
        ["nw", "..", "..", "+n", "..", "..", "ne"],
        ["..", "$$", "..", "~~", "..", "!!", ".."],
        ["..", "..", "$$", "~~", "!!", "..", ".."],
        ["+w", "@@", "@@", "XX", "##", "##", "+e"],
        ["..", "..", "^^", "++", "**", "..", ".."],
        ["..", "^^", "..", "++", "..", "**", ".."],
        ["sw", "..", "..", "+s", "..", "..", "se"],
    ]

    assert matrix[3][3] == "XX"

    directions = list(walk_compass_directions(matrix, 3, 3, distance=4))

    assert directions[0] == ["XX", "~~", "~~", "+n"]  # north
    assert directions[1] == ["XX", "!!", "!!", "ne"]  # north east
    assert directions[2] == ["XX", "##", "##", "+e"]  # east
    assert directions[3] == ["XX", "**", "**", "se"]  # south east
    assert directions[4] == ["XX", "++", "++", "+s"]  # south
    assert directions[5] == ["XX", "^^", "^^", "sw"]  # south west
    assert directions[6] == ["XX", "@@", "@@", "+w"]  # west
    assert directions[7] == ["XX", "$$", "$$", "nw"]  # north west


def test_walk_compass_not_enough_space_in_any_direction():
    matrix = [
        ["nw", "..", "..", "+n", "..", "..", "ne"],
        ["..", "$$", "..", "~~", "..", "!!", ".."],
        ["..", "..", "$$", "~~", "!!", "..", ".."],
        ["+w", "@@", "@@", "XX", "##", "##", "+e"],
        ["..", "..", "^^", "++", "**", "..", ".."],
        ["..", "^^", "..", "++", "..", "**", ".."],
        ["sw", "..", "..", "+s", "..", "..", "se"],
    ]

    assert matrix[3][3] == "XX"

    directions = list(walk_compass_directions(matrix, 3, 3, distance=5))

    assert len(directions) == 8
    assert len([d for d in directions if d is None]) == 8
