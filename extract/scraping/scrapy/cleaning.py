from bs4 import BeautifulSoup

def soup_to_text(soup, new_lines=False):
    if type(soup) is str:
        soup = BeautifulSoup(
            soup, features="lxml"
        )

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()  # rip it out

    # get text
    text = soup.get_text("\n")

    text = text.replace("\xa0", " ")

    # break into lines and remove leading and trailing space on each
    lines = (
        line.strip() for line in text.splitlines()
    )

    # break multi-headlines into a line each
    chunks = (
        phrase.strip()
        for line in lines
        for phrase in line.split("  ")
    )

    # remove single character words and numbers
    chunks = [
        " ".join(
            [
                word
                for word in chunk.split(" ")
                if len(word) > 1
                and not is_numeric(word)
            ]
        )
        for chunk in chunks
    ]

    # drop blank lines

    if new_lines:
        joiner = "\n"

    else:
        joiner = "   "

    text = joiner.join(
        [chunk for chunk in chunks if chunk]
    )

    # normalise characters
    # text = gensim.utils.deaccent(text)

    # except:
    #
    #     print(text)

    return text

def is_numeric(word):
    if len(word) > 10:
        are_numeric = sum(
            [c.isnumeric() for c in word]
        ) / len(word)
        if are_numeric > 0.5:
            return True
    return False