import colorsys 


def rgb2hsv(red,green,blue):
	lista=[red,green,blue]

	r2 = red / 255
	g2 = green / 255
	b2 = blue / 255

	maximo = max(lista)
	minimo = min(lista)

	delta = maximo - minimo

	for i in range(len(lista)):
		if (lista[i] == maximo):
			print i
			break

	if (i == 2):
		print "blue"

	if (i == 1):
		print "verde"

	if (i == 0):
		print "Rojo"




if __name__ == '__main__':
	rgb2hsv(25,100,56)