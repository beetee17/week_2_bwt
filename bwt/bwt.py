# python3
import sys

def BWT(text):

    M = []

    for i in range(len(text)):
        temp = text[i:] + text[:i]
        M.append(temp)
        
    M.sort()

    return ''.join([item[-1] for item in M])



if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(BWT(text))