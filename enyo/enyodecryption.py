class EnyoDecryption:
    numSet = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'a', 27: 'b', 28: 'c', 29: 'd', 30: 'e', 31: 'f', 32: 'g', 33: 'h', 34: 'i', 35: 'j', 36: 'k', 37: 'l', 38: 'm', 39: 'n', 40: 'o', 41: 'p', 42: 'q', 43: 'r', 44: 's', 45: 't', 46: 'u', 47: 'v', 48: 'w', 49: 'x', 50: 'y', 51: 'z', 52: '0', 53: '1', 54: '2', 55: '3', 56: '4', 57: '5', 58: '6', 59: '7', 60: '8', 61: '9', 62:'$',63:'@'}

    charSet = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38, 'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49, 'y': 50, 'z': 51, '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61, '$':62, '@':63 }
    
    def __init__(self,text,secret,partition=2):
        self.encrypted = self.moduloDecryption(text) # Modular Decryption 
        self.secret = secret # Secret key for decryption
        self.part = self.partitionChecker(partition)
        self.ekey = self.keyPartioning(self.encode(self.secret),self.part) # Partition based encoded secret key
        self.newCharSet, self.newNumSet = self.charSetModifier(self.ekey) # Modified character sets
        self.key = self.partition(self.ekey,self.part) # Final secret key array for encryption
        self.decrypted = self.decode(self.decryption()) # Multistage XOR Decryption + Decoding
        
    def encode(self,str):
        bits = ""
        encodedWord = ""
        # Converting the ascii characters to binary
        for i in str:
            bits += format(ord(i),'08b')
        # Making the number of bits to be divisible by 6
        while(len(bits)%6!=0):
            bits+='00'
        # Base64 Encode
        for j in range(0,len(bits),6):
            encodedWord = encodedWord + self.numSet[int(bits[j:j+6],2)]
        return encodedWord
    
    def decode(self,str):
        decodedWord = ""
        bits = ""
        # Converting the ASCII values to fit in our character set.
        for i in str:
            if(ord(i)>64 and ord(i)<91):
                bits+=format(ord(i)-65,'06b')
            elif(ord(i)>96 and ord(i)<123):
                bits+=format(ord(i)-71,'06b')
            else:
                bits+=format(ord(i)+4,'06b')
        for i in range(0,len(bits),8):
            decodedWord = decodedWord+chr(int(bits[i:i+8],2))
        return decodedWord
    
    def binarySwap(self,str):
        # Binary conversion and filling zeroes for length 6
        str = str[2:]
        while(len(str)!=6):
            str = '0' + str
        # Swapping stage
        str = str[3:] + str[:3]
        str = '0b' + str
        xor = int(str,2)
        return xor

    def charSetModifier(self,encodedKey):
        total = 0
        for i in encodedKey:
            total = total + self.charSet[i]
        # Shifts the sets by sum modulus 16 
        shifter = total%16
        # Shifting both character sets by shifter
        newCharSet = {}
        newNumSet = {}
        index = 0
        for i in self.charSet:
            newCharSet[i]=(index+shifter)%64
            index += 1
        for i in self.numSet:
            newNumSet[(i+shifter)%64]=self.numSet[i]
        return (newCharSet,newNumSet)
    
    def moduloDecryption(self,encrypt):
        decrypted = ""
        for i in encrypt:
            x = self.charSet[i]
            bits = format(x,'06b')
            decrypted += self.numSet[int(bits[0:4],2)+16*int(bits[4:],2)]
        return decrypted
    
    def keyPartioning(self,encodedKey,part):
        i = len(encodedKey)%part
        while(len(encodedKey)%part!=0):
            encodedKey = encodedKey+encodedKey[i]
            i += 1
        return encodedKey
    
    def partition(self,encodedKey,part):
        key = []
        for i in range(0,len(encodedKey),len(encodedKey)//part):
            key.append(encodedKey[i:i+len(encodedKey)//part]) 
        return key
    
    def partitionChecker(self,part):
        if(part>len(self.encode(self.secret))):
            raise Exception("Number of partitions not possible.")
        else:
            return part
    
    def decryption(self):
        index = 0
        decrypted = ""
        for i in range(len(self.encrypted)):
            x = self.newCharSet[self.encrypted[i]]
            j = len(self.key)-1 
            if(i%2!=0):
                xor = x^self.newCharSet[self.key[j][index]]
                j-=1
                while(j>=0):
                    xor = xor^self.newCharSet[self.key[j][index]]
                    j -= 1
            else:
                xor = x^self.newCharSet[self.key[j][index]]
                j -= 1
                while(j>=0):
                    if(j%2!=0):
                        xor = xor^self.newCharSet[self.key[j][index]]
                    else:  
                        # Binary swapping
                        xor = self.binarySwap(bin(xor))
                        # Ciphering logic
                        xor = xor^self.newCharSet[self.key[j][index]]
                    j -= 1
            decrypted += self.newNumSet[xor]
            index += 1
            if(index>len(self.key[0])-1):
                index = 0
        return decrypted