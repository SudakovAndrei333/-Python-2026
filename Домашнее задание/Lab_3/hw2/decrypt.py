import sys

def decrypt(encrypted):
    stack = []
    i = 0
    n = len(encrypted)
    while i < n:
        ch = encrypted[i]
        if ch == '.':
            if i + 1 < n and encrypted[i+1] == '.':
                if stack:
                    stack.pop()
                i += 2
            else:
                i += 1
        else:
            stack.append(ch)
            i += 1
    return ''.join(stack)

if __name__ == '__main__':
    encrypted = sys.stdin.read().strip()
    print(decrypt(encrypted))

