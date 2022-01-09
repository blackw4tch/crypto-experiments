def readCipher(filename):
    file = open(filename, 'r')
    strCipher = file.read()
    cipher = []
    index = 0
    while index < len(strCipher):
        cipher.append(int(strCipher[index:index+2], 16))
        index += 2
    return cipher

def getCipherGroup(keyLength, cipher):
    cipherGroup = [[] for a in range(keyLength)]
    count = 0
    while count < len(cipher):
        cipherGroup[(count) % keyLength] += [cipher[count]]
        count += 1
    return cipherGroup


def getKeyRange(keyLength, cipher):
    cipherGroup = getCipherGroup(keyLength, cipher)
    keyGroup = [[] for a in range(keyLength)]

    count=0
    for perCipherGroup in cipherGroup:
        for keyTest in range(1,255):
            for perCipher in perCipherGroup:
                plainChar = perCipher^keyTest
                if plainChar not in range(32,127):
                    break
            else:
                keyGroup[count].append(keyTest)
        count+=1

    return keyGroup

def getLetterFrequency(key, perCipher):
    frequencies = {"e": 0.12702, "t": 0.09056, "a": 0.08167, "o": 0.07507, "i": 0.06966,
                   "n": 0.06749, "s": 0.06327, "h": 0.06094, "r": 0.05987, "d": 0.04253,
                   "l": 0.04025, "c": 0.02782, "u": 0.02758, "m": 0.02406, "w": 0.02360,
                   "f": 0.02228, "g": 0.02015, "y": 0.01974, "p": 0.01929, "b": 0.01492,
                   "v": 0.00978, "k": 0.00772, "j": 0.00153, "x": 0.00150, "q": 0.00095,
                   "z": 0.00074}

    count={}
    for ch in perCipher:
        plainChar = key^ch
        if plainChar in range(65,91) or plainChar in range(97,123):
            char = chr(plainChar).lower()
            count[char] = count.setdefault(char, 0)+1

    freq = 0.0
    for a in count:
        freq += frequencies[a]*count[a]/len(perCipher)

    return freq

def getKeyConfirmValue(keyGroup,cipher):
    cipherGroup = getCipherGroup(len(keyGroup), cipher)
    key = []

    count=0
    for perKey in keyGroup:
        maxFreq = 0
        tempKey = 0
        for a in perKey:
            freq = getLetterFrequency(a, cipherGroup[count])
            if freq>maxFreq:
                maxFreq = freq
                tempKey = a
        key.append(tempKey)
        count += 1
    
    return key

def cipherDecrypt(key, cipher):
    plainText = ''
    index = 0
    for a in cipher:
        plainText += chr(key[index%len(key)]^a)
        index += 1
    return plainText

def controlFlow():
    keyLengthRange = range(1,15)
    cipher = readCipher('miwen.txt')
    for i in keyLengthRange:
        keyGroup = getKeyRange(i, cipher)
        for a in keyGroup:
            if 0 == len(a):
                break;          
        else:               
            key = getKeyConfirmValue(keyGroup, cipher)
            print('密钥:', key,'\n')
            plainText = cipherDecrypt(key, cipher)
            print('明文:', plainText,'\n')

if __name__=='__main__':
    controlFlow()
