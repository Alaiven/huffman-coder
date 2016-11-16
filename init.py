""" Huffman coder menu """

import coder

OPTION = ''

IN_FILE = None
DI_FILE = None
OUT_FILE = None

FRAME_LEN = 0

while OPTION != '0':
    print '1. Tworzenie slownika'
    print '2. Kodowanie'
    print '3. Dekodowanie'
    print '0. Wyjscie'
    OPTION = raw_input('Podaj opcje: ')

    if OPTION == '1':
        IN_FILE = raw_input('Podaj plik wejsciowy: ')
        DI_FILE = raw_input('Podaj plik slownika: ')
        FRAME_LEN = raw_input('Podaj max dlugosc slowa: ')

        with open(IN_FILE, 'r') as input_file:
            with open(DI_FILE, 'w') as dict_file:
                coder.make_dict(input_file, dict_file, int(FRAME_LEN))

    elif OPTION == '2':
        IN_FILE = raw_input('Podaj plik wejsciowy: ')
        DI_FILE = raw_input('Podaj plik slownika: ')
        OUT_FILE = raw_input('Podaj plik wyjsciowy: ')
        FRAME_LEN = raw_input('Podaj max dlugosc slowa: ')

        with open(IN_FILE, 'r') as input_file:
            with open(DI_FILE, 'r') as dict_file:
                with open(OUT_FILE, 'wb') as out_file:
                    coder.encode(input_file, dict_file, out_file, int(FRAME_LEN))

    elif OPTION == '3':
        IN_FILE = raw_input('Podaj plik kodu: ')
        DI_FILE = raw_input('Podaj plik slownika: ')
        OUT_FILE = raw_input('Podaj plik wyjsciowy: ')

        with open(IN_FILE, 'rb') as input_file:
            with open(DI_FILE, 'r') as dict_file:
                with open(OUT_FILE, 'w') as out_file:
                    coder.decode(input_file, dict_file, out_file)
