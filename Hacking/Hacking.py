import random
import sys

GARBAGE_CHARS = '~!@#$%^&*()_+-={}[]|;:,.<>?/'

# Load the list of 7-letter words from the text file.
with open('sevenletterwords.txt', 'r') as wordListFile:
    WORDS = [word.strip().upper() for word in wordListFile.readlines()]


def main():
    print('''Hacking Minigame
Find the password in the computer's memory. You are given clues after each guess.
For example, if the secret password is MONITOR and you guess CONTAIN, you are 
told how many letters are correct. You get four guesses.\n''')

    input('Press Enter to begin...')

    gameWords = getWords()
    computerMemory = getComputerMemoryString(gameWords)
    secretPassword = random.choice(gameWords)

    print(computerMemory)

    for triesRemaining in range(4, 0, -1):
        playerMove = askForPlayerGuess(gameWords, triesRemaining)
        if playerMove == secretPassword:
            print('ACCESS GRANTED')
            return
        else:
            numMatches = numMatchingLetters(secretPassword, playerMove)
            print(f'Access Denied ({numMatches}/7 correct)')
    print(f'Out of tries. Secret password was {secretPassword}.')


def getWords():
    secretPassword = random.choice(WORDS)
    words = [secretPassword]

    while len(words) < 3:
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 0:
            words.append(randomWord)

    for i in range(500):
        if len(words) == 5:
            break
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) == 3:
            words.append(randomWord)

    for i in range(500):
        if len(words) == 12:
            break
        randomWord = getOneWordExcept(words)
        if numMatchingLetters(secretPassword, randomWord) != 0:
            words.append(randomWord)

    while len(words) < 12:
        randomWord = getOneWordExcept(words)
        words.append(randomWord)

    return words


def getOneWordExcept(blocklist=None):
    if blocklist is None:
        blocklist = []
    while True:
        randomWord = random.choice(WORDS)
        if randomWord not in blocklist:
            return randomWord


def numMatchingLetters(word1, word2):
    return sum(1 for i in range(len(word1)) if word1[i] == word2[i])


def getComputerMemoryString(words):
    linesWithWords = random.sample(range(16 * 2), len(words))
    memoryAddress = 16 * random.randint(0, 4000)
    computerMemory = []
    nextWord = 0

    for lineNum in range(16):
        leftHalf = ''.join(random.choice(GARBAGE_CHARS) for _ in range(16))
        rightHalf = ''.join(random.choice(GARBAGE_CHARS) for _ in range(16))

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

        computerMemory.append(
            f'0x{hex(memoryAddress)[2:].zfill(4)}  {leftHalf}    0x{hex(memoryAddress + (16 * 16))[2:].zfill(4)}  {rightHalf}')
        memoryAddress += 16

    return '\n'.join(computerMemory)


def askForPlayerGuess(words, tries):
    while True:
        print(f'Enter password: ({tries} tries remaining)')
        guess = input('> ').upper()
        if guess in words:
            return guess
        print(
            f'That is not one of the possible passwords. Try "{words[0]}" or "{words[1]}".')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
