# From https://samtools.github.io/hts-specs/SAMv1.pdf
CINS, CDEL, CMATCH, CEQUAL, CDIFF = 'IDM=X'


def parseBtop(btopString):
    """
    Parse a BTOP string.

    The format is described at https://www.ncbi.nlm.nih.gov/books/NBK279682/

    @param btopString: A C{str} BTOP sequence.
    @raise ValueError: If C{btopString} is not valid BTOP.
    @return: A generator that yields a series of integers and 2-tuples of
        letters, as found in the BTOP string C{btopString}.
    """
    isdigit = str.isdigit
    value = None
    queryLetter = None
    for offset, char in enumerate(btopString):
        if isdigit(char):
            if queryLetter is not None:
                raise ValueError(
                    'BTOP string %r has a query letter %r at offset %d with '
                    'no corresponding subject letter' %
                    (btopString, queryLetter, offset - 1))
            value = int(char) if value is None else value * 10 + int(char)
        else:
            if value is not None:
                yield value
                value = None
                queryLetter = char
            else:
                if queryLetter is None:
                    queryLetter = char
                else:
                    if queryLetter == '-' and char == '-':
                        raise ValueError(
                            'BTOP string %r has two consecutive gaps at '
                            'offset %d' % (btopString, offset - 1))
                    elif queryLetter == char:
                        raise ValueError(
                            'BTOP string %r has two consecutive identical %r '
                            'letters at offset %d' %
                            (btopString, char, offset - 1))
                    yield (queryLetter, char)
                    queryLetter = None

    if value is not None:
        yield value
    elif queryLetter is not None:
        raise ValueError(
            'BTOP string %r has a trailing query letter %r with '
            'no corresponding subject letter' % (btopString, queryLetter))


def countGaps(btopString):
    """
    Count the query and subject gaps in a BTOP string.

    @param btopString: A C{str} BTOP sequence.
    @raise ValueError: If L{parseBtop} finds an error in the BTOP string
        C{btopString}.
    @return: A 2-tuple of C{int}s, with the (query, subject) gaps counts as
        found in C{btopString}.
    """
    queryGaps = subjectGaps = 0
    for countOrMismatch in parseBtop(btopString):
        if isinstance(countOrMismatch, tuple):
            queryChar, subjectChar = countOrMismatch
            queryGaps += int(queryChar == '-')
            subjectGaps += int(subjectChar == '-')

    return (queryGaps, subjectGaps)


def btop2cigar(btopString, concise=False):
    """
    Convert a BTOP string to a CIGAR string.

    @param btopString: A C{str} BTOP sequence.
    @param concise: If C{True}, use 'M' for matches and mismatches instead
        of the more specific 'X' and '='.

    @raise ValueError: If L{parseBtop} finds an error in C{btopString}.
    @return: A C{str} CIGAR string.
    """
    result = []
    thisLength = thisOperation = currentLength = currentOperation = None

    for item in parseBtop(btopString):
        if isinstance(item, int):
            thisLength = item
            thisOperation = CMATCH if concise else CEQUAL
        else:
            thisLength = 1
            query, reference = item
            if query == '-':
                # The query has a gap. That means that in matching the
                # query to the reference a deletion is needed in the
                # reference.
                assert reference != '-'
                thisOperation = CDEL
            elif reference == '-':
                # The reference has a gap. That means that in matching the
                # query to the reference an insertion is needed in the
                # reference.
                thisOperation = CINS
            else:
                # A substitution was needed.
                assert query != reference
                thisOperation = CMATCH if concise else CDIFF

        if thisOperation == currentOperation:
            currentLength += thisLength
        else:
            if currentOperation is not None:
                result.append('%d%s' % (currentLength, currentOperation))
            currentLength, currentOperation = thisLength, thisOperation

    # We reached the end of the BTOP string. If there was an operation
    # underway, emit it.  The 'if' here should only be needed to catch the
    # case where btopString was empty.
    assert currentOperation is not None or btopString == ''
    if currentOperation is not None:
        result.append('%d%s' % (currentLength, currentOperation))

    return ''.join(result)
