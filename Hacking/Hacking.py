import random
import sys

# Символы для заполнения дисплея терминала
GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

# Подгружаем файл со словами (из 7-ми букв, уровень защиты терминала - "простой" ¯\_(ツ)_/¯)
with open('Hacking\sevenletterwords.txt', 'r') as wordListFile:
    WORDS = [word.strip().upper() for word in wordListFile.readlines()]

# Запуск игры
def main():
    print('''\nROBCO INDUSTRIES (TM) TERMILINK PROTOCOL
ENTER PASSWORD NOW\n''')

    input('Press Enter...')

    gameWords = getWords()
    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print(computerMemory)

    for triesRemaining in range(4, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print(f'>Exact match! \n>Please wait while system is accessed')
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print(f'>Entry denied \n>{numMatches}/7 correct')
    print(
        f'TERMINAL LOCKED: Please contact an administrator.\nPassword was {secretPassword}.')

# Формируем список из 12-ти слов
def getWords():
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    # 3 слова без совпадений букв
    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    # 2 слова, в которых по три совпадения букв (500 попыток подбора)
    for i in range(500):
        if len(words) == 5:
            break
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    # 7 слов, в которых хотя бы одно совпадение букв (500 попыток подбора)
    for i in range(500):
        if len(words) == 12:
            break
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    # Добавляем рандомные слова, если не хватило до 12-ти
    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)

    return words

# Исключаем повторы слов
def getOneWordExcept(blocklist=None):
    if blocklist is None:
        blocklist = []
    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord

# Считаем количество совпадений по буквам в словах при подборе пароля
def numMatchingLetters(word1, word2):
    return sum(1 for i in range(len(word1)) if word1[i] == word2[i])

# Формируем экран терминала
def getComputerMemoryString(words):
    linesWithWords = random.sample(range(16 * 2), len(words))
    memoryAddress = 16 * random.randint(0, 4000)
    computerMemory = []
    nextWord = 0

    for lineNum in range(16):
        leftHalf = ''.join(random.choice(GARBAGE_CHARS) for _ in range(16))
        rightHalf = ''.join(random.choice(GARBAGE_CHARS) for _ in range(16))

        # Вставляем слова в заполнение
        if lineNum in linesWithWords:
            insertionIndex = random.randint(0, 9)
            leftHalf = leftHalf[:insertionIndex] + \
                words[nextWord] + leftHalf[insertionIndex + 7:]
            nextWord += 1
        if lineNum + 16 in linesWithWords:
            insertionIndex = random.randint(0, 9)
            rightHalf = rightHalf[:insertionIndex] + \
                words[nextWord] + rightHalf[insertionIndex + 7:]
            nextWord += 1

        # Левая часть столбика с кодом
        computerMemory.append(
            f'0x{hex(memoryAddress)[2:].zfill(4)}  {leftHalf}    0x{hex(memoryAddress + (32 * 32))[2:].zfill(4)}  {rightHalf}')
        memoryAddress += random.randrange(16, 128, 16)

    return '\n'.join(computerMemory)

# Ввод варианта пароля
def askForPlayerGuess(words, tries):
    while True:
        print(f'\n{tries} ATTEMPT(S) LEFT: {"[]" * (tries)}')
        guess = input('> ').upper()
        if guess in words:
            return guess
        print(
            f'That is not one of the possible passwords. Try "{words[0]}" or "{words[1]}".')


# Ctrl+C завершить работу программы
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

