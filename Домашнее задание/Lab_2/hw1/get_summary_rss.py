def get_summary_rss(filepath: str):
    total = 0
    with open(filepath, 'r') as f:
        lines = f.readlines()[1:]  # пропускаем заголовок
        for line in lines:
            columns = line.split()
            total += int(columns[5])
    return total

def converter(size):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ', 'ПБ']
    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024


if __name__ == '__main__':
    file_path = 'output_file.txt'
    total = get_summary_rss(file_path)
    print(converter(total))
