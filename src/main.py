from rag import RAG


def main():
    rag = RAG()
    while True:
        user_input = input('Keresés: ')
        result = rag.query(text=user_input)
        print(result)
        print()

# TODO: Reset requirements


if __name__ == '__main__':
    main()
