from itertools import chain, combinations


def get_list_of_proper_subsets(iterable):
    """Generates a list of all proper subsets of the given iterable.

    A proper subset of a set `S` is any subset of `S` that is not equal
    to `S` itself. This includes the empty set. The function uses
    `itertools.combinations` to efficiently generate all subsets of
    lengths from 0 up to, but not including, the length of the original
    iterable.

    Args:
        iterable: An iterable (e.g., list, tuple, set) from which to
            generate subsets.

    Returns:
        list[list]: A list containing all proper subsets of the input
                    iterable. Each subset is represented as a list.

    Example:
        >>> get_list_of_proper_subsets([1, 2, 3])
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3]]

        >>> get_list_of_proper_subsets(['a', 'b'])
        [[], ['a'], ['b']]
    """
    s = list(iterable)

    return [
        list(item)
        for item in chain.from_iterable(combinations(s, r) for r in range(len(s)))
    ]
