import compose

map = [
    ("1f61e","tester/samples/disappointed.png"),
    ("1f61f","tester/samples/worried.png"),
    ("1f600","tester/samples/grinning.png"),
    ("1f612","tester/samples/unamused.png"),
    ("1f618","tester/samples/kiss.png"),
]

compose.build_font(map, 'tester/test.ttf')
