import timeit


def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0

    bad_char = {}

    for i in range(m):
        bad_char[pattern[i]] = i

    shift = 0

    while shift <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            return shift

        shift += max(
            1,
            j - bad_char.get(text[shift + j], -1)
        )

    return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)

    length = 0
    i = 1

    while i < len(pattern):

        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    if len(pattern) == 0:
        return 0

    lps = compute_lps(pattern)

    i = 0
    j = 0

    while i < len(text):

        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == len(pattern):
                return i - j

        elif j != 0:
            j = lps[j - 1]

        else:
            i += 1

    return -1


def rabin_karp_search(text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length == 0:
        return 0

    if pattern_length > text_length:
        return -1

    base = 256
    prime = 101

    pattern_hash = 0
    text_hash = 0

    h = pow(base, pattern_length - 1, prime)

    for i in range(pattern_length):
        pattern_hash = (
            base * pattern_hash + ord(pattern[i])
        ) % prime

        text_hash = (
            base * text_hash + ord(text[i])
        ) % prime

    for i in range(text_length - pattern_length + 1):

        if pattern_hash == text_hash:

            if text[i:i + pattern_length] == pattern:
                return i

        if i < text_length - pattern_length:

            text_hash = (
                base * (
                    text_hash
                    - ord(text[i]) * h
                )
                + ord(text[i + pattern_length])
            ) % prime

    return -1



def read_file(filename):
    with open(filename, "r", encoding="cp1251") as file:
        return file.read().lower()


def measure_time(search_function, text, pattern):
    result = timeit.timeit(
        lambda: search_function(text, pattern),
        number=500
    )

    return result / 500


def test_algorithms(article_name, text, existing, fake):

    algorithms = {
        "Boyer-Moore": boyer_moore_search,
        "KMP": kmp_search,
        "Rabin-Karp": rabin_karp_search
    }

    print(f"\n{'=' * 60}")
    print(article_name)
    print("=" * 60)

    patterns = {
        "Existing substring": existing,
        "Fake substring": fake
    }

    for pattern_type, pattern in patterns.items():

        print(f"\n{pattern_type}:")
        print(f'"{pattern}"')

        results = {}

        for name, algorithm in algorithms.items():

            execution_time = measure_time(
                algorithm,
                text,
                pattern
            )

            results[name] = execution_time

            print(
                f"{name:<15}: "
                f"{execution_time:.8f} seconds"
            )

        fastest = min(results, key=results.get)

        print(f"Fastest: {fastest}")


def main():

    article_1 = read_file("стаття 1.txt")
    article_2 = read_file("стаття 2.txt")

    test_algorithms(
        "ARTICLE 1",
        article_1,
        "експоненціальний пошук використовується",
        "квантовий пошук у зеленому лабіринті"
    )

    test_algorithms(
        "ARTICLE 2",
        article_2,
        "профілювання тестового коду показало",
        "квантова база даних зоряного каталогу"
    )


if __name__ == "__main__":
    main()