from rag import RAG
from gui import GUI


def main():
    rag = RAG()
    gui = GUI(rag=rag)
    gui.mainloop()


if __name__ == '__main__':
    main()
