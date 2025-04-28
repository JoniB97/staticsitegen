from textnode import *

def main():
    print("hello world")
    textNode = TextNode("This is some anchor text", TextType["link"], "https://www.boot.dev")
    print(textNode)

if __name__ == "__main__":
    main()