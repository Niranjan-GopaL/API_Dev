dictionary = {
    1 : "one",
    2 : "two",
    3 : "three",
    4 : "four",
}

if 5 not in dictionary:
    dictionary[5] = "five"

print(dictionary)

# So if the result of a .fetchall() is empty, REMEMBER IT IS `[]`
# if updated_post == []  <--- correct way
# if not updated_post    <--- safest way
print(  None is [] )
print(  None == [] )