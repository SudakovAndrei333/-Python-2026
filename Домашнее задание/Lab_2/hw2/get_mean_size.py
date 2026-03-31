import sys

def get_mean_size(data_lines):
    size = 0
    count = 0
    for line in data_lines:
        if not line.strip():
            continue
        parts = line.split()
        size += int(parts[4])
        count += 1
    return size / count if count > 0 else 0.0

if __name__ == '__main__':
    lines = sys.stdin.readlines()
    if len(lines) > 1:
        data = lines[1:]
        mean_size = get_mean_size(data)
        print(mean_size)
    else:
        print(0)
