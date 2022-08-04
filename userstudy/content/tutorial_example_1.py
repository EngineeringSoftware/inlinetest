import sys
from inline import Here

input_list = sys.argv[1:]
res = list(map(str.split, input_list))
Here().given(input_list, ["Hello World!", "Have a good day"]).check_eq(
    res, [["Hello", "World!"], ["Have", "a", "good", "day"]]
)
