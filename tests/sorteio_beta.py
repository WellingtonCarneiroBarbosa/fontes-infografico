number = random.randint(0, 9999999)

data_iterator.set_index('a - username', inplace=True)
username = data_iterator.index[number]

data_iterator.set_index('b - comment', inplace=True)
comment = data_iterator.index[number]


print("\rnumero da sorte => " + str(number))
print("\rUsuario que ganhou => " + str(username))
print("\rComentario do usuario => " + str(comment) )