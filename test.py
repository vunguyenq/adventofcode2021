segments = {0: 'abcefg', 1:'cf', 2:'acdeg', 3:'acdfg', 4:'bcdf', 5:'abdfg', 6:'abdefg', 7:'acf', 8:'abcdefg', 9:'abcdfg'}
segments = {key: set(segments[key]) for key in segments}
print(segments.values())