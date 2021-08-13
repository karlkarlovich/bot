def write_dictionary(questions, answers):
    DRFO = open('dictionary.py', 'r')  # DRFO - dictionary read file object
    ftext = DRFO.read()
    DRFO.close()

    ftext = f'{ftext[:len(ftext)-2]}, quanswer(['

    for i in questions:
        ftext = f'{ftext}"{i}", '

    ftext = f'{ftext[:len(ftext) - 2]}], ['

    for i in answers:
        ftext = f'{ftext}"{i}", '

    ftext = f'{ftext[:len(ftext) - 2]}])]/n'
    DWFO = open('dictionary.py', 'w')
    DWFO.write(ftext)
    DWFO.close()


def input_word_list():
    word_list = []

    text = input('-> ')

    while text != '':
        word_list.append(text)
        text = input('-> ')

    return word_list


def main():
    print('input questions:')
    questions = input_word_list()

    print('input answers:')
    answers = input_word_list()

    write_dictionary(questions, answers)


main()
