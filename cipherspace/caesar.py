import sys

def decrypt(ciphertext):
    ciphertext = ciphertext.upper()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for key in range(len(alpha)):
        plaintext = ""
        for letter in ciphertext:
            if letter in alpha:
                letter_index = (alpha.find(letter)) - key % len(alpha) 
                plaintext += alpha[letter_index]
            else:
                plaintext = plaintext + letter
        print(f"Trying {key}: {plaintext}")

def main():
    if len(sys.argv) != 2:
        print("[!] Usage: %s <ciphertext>" % sys.argv[0])
        print("[!] Example: %s 'Example text'\n" % sys.argv[0])

    ciphertext = sys.argv[1]
    print("[+] Deciphering....")

    decrypt(ciphertext)

if __name__ == "__main__":
    main()


    