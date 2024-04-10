queries = []
unique = ()
with open("../php/src/collated_union.txt", "r") as f:
    for line in f:
        queries.append(line)

unique = set(queries)

print(len(unique))
print(len(queries))

        


