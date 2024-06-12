immutable_var = ([1, 2, 3, 4, 5, 6, 7, 8, 9], "String", 1, True)
print(immutable_var)
#Элементы кортежа нельзя изменить. Но можно изменить элементы списка, если он содержится в кортеже, например:
mutable_list = ([1, 2, 3], "Second element")  #1-м элементом кортежа является список
print(mutable_list)
mutable_list[0][1] = 222                      #Меняем 2-й элемент списка
print(mutable_list)
