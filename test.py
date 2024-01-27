s = "J.K. Rowling"

temp = ''.join([c.lower() if c != " " else "-" for c in s])

print(temp)
