def count():
    c = 0
    try:
        with open('count.txt', 'r') as f:
            c = int(f.readline().strip())
    except:
        pass

    with open('count.txt', 'w') as f:
        f.write(str(c + 1))
    return c + 1
