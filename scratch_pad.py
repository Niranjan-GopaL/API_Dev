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

'''How to make symlinks in WINDOWS
mklink "C:\Users\HP\AppData\Roaming\Code\User\keybindings.json" "D:\Code Practise\dotfiles\vscode config\keybindings.json"
mklink "C:\Users\HP\AppData\Roaming\Code\User\settings.json" "D:\Code Practise\dotfiles\vscode config\settings.json"
mklink "C:\Users\HP\AppData\Roaming\Code\User\tasks.json" "D:\Code Practise\dotfiles\vscode config\tasks.json"
'''