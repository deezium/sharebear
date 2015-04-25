import random

def nameGenerator():
	vowels = ['a','e','i','o','u','y']
	consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']
	word = []

	for i in range(5):
		v = random.randint(0,5)
		c = random.randint(0,19)
		if i % 2 == 1:
			word.append(vowels[v])
		else:
			word.append(consonants[c])

	print ''.join(word)

nameGenerator()
