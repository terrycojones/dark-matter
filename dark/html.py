from __future__ import print_function

from IPython.display import HTML


def NCBISequenceLinkURL(title, default=None):
    """
    Given a sequence title, like "gi|42768646|gb|AY516849.1| Homo sapiens",
    return the URL of a link to the info page at NCBI.

    title: the sequence title to produce a link URL for.
    default: the value to return if the title cannot be parsed.
    """
    try:
        ref = title.split('|')[3].split('.')[0]
    except IndexError:
        return default
    else:
        return 'http://www.ncbi.nlm.nih.gov/nuccore/%s' % (ref,)


def NCBISequenceLink(title, default=None):
    """
    Given a sequence title, like "gi|42768646|gb|AY516849.1| Homo sapiens",
    return an HTML A tag dispalying a link to the info page at NCBI.

    title: the sequence title to produce an HTML link for.
    default: the value to return if the title cannot be parsed.
    """
    url = NCBISequenceLinkURL(title)
    if url is None:
        return default
    else:
        return '<a href="%s" target="_blank">%s</a>' % (url, title)


def _sortHTML(titlesAlignments, by, limit=None):
    """
    Return an C{IPython.display.HTML} object with the alignments sorted by the
    given attribute.

    @param titlesAlignments: A L{dark.titles.TitlesAlignments} instance.
    @param by: A C{str}, one of 'length', 'maxScore', 'medianScore',
        'readCount', or 'title'.
    @param limit: An C{int} limit on the number of results to show.
    @return: An HTML instance with sorted titles and information about
        hit read count, length, and e-values.
    """
    out = []
    for i, title in enumerate(titlesAlignments.sortTitles(by), start=1):
        if limit is not None and i > limit:
            break
        titleAlignments = titlesAlignments[title]
        link = NCBISequenceLink(title, title)
        out.append(
            '%3d: reads=%d, len=%d, max=%s median=%s<br/>'
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s' %
            (i, titleAlignments.readCount(), titleAlignments.subjectLength,
             titleAlignments.bestHsp().score.score,
             titleAlignments.medianScore(), link))
    return HTML('<pre>' + '<br/>'.join(out) + '</pre>')


def summarizeTitlesByTitle(titlesAlignments, limit=None):
    """
    Sort match titles by title

    @param titlesAlignments: A L{dark.titles.TitlesAlignments} instance.
    @param limit: An C{int} limit on the number of results to show.
    @return: An C{IPython.display.HTML} instance with match titles sorted by
        title.
    """
    return _sortHTML(titlesAlignments, 'title', limit)


def summarizeTitlesByCount(titlesAlignments, limit=None):
    """
    Sort match titles by read count.

    @param titlesAlignments: A L{dark.titles.TitlesAlignments} instance.
    @param limit: An C{int} limit on the number of results to show.
    @return: An C{IPython.display.HTML} instance with match titles sorted by
        read count.
    """
    return _sortHTML(titlesAlignments, 'readCount', limit)


def summarizeTitlesByLength(titlesAlignments, limit=None):
    """
    Sort match titles by sequence length.

    @param titlesAlignments: A L{dark.titles.TitlesAlignments} instance.
    @param limit: An C{int} limit on the number of results to show.
    @return: An C{IPython.display.HTML} instance with match titles sorted by
        sequence length.
    """
    return _sortHTML(titlesAlignments, 'length', limit)


def summarizeTitlesByMaxScore(titlesAlignments, limit=None):
    """
    Sort hit titles by maximum score.

    @param titlesAlignments: A L{dark.blast.BlastMatchs} instance.
    @param limit: An C{int} limit on the number of results to show.
    @return: An C{IPython.display.HTML} instance with hit titles sorted by
        max score.
    """
    return _sortHTML(titlesAlignments, 'maxScore', limit)


def summarizeTitlesByMedianScore(titlesAlignments, limit=None):
    """
    Sort match titles by median score.

    @param titlesAlignments: A L{dark.titles.TitlesAlignments} instance.
    @param limit: An C{int} limit on the number of results to show.
    @return: An C{IPython.display.HTML} instance with match titles sorted by
        median score.
    """
    return _sortHTML(titlesAlignments, 'medianScore', limit)


class AlignmentPanelHTMLWriter(object):
    """
    Produces HTML details of a rectangular panel of graphs that each
    contain an alignment graph against a given sequence. This is
    supplementary output info for the AlignmentPanel class in graphics.py.

    @param outputDir: The C{str} directory to write files into.
    @param titlesAlignments: A L{dark.titles.TitlesAlignments} instance.
    """
    def __init__(self, outputDir, titlesAlignments):
        self._outputDir = outputDir
        self._titlesAlignments = titlesAlignments
        self._images = []

    def addImage(self, imageBasename, title, graphInfo):
        self._images.append({
            'graphInfo': graphInfo,
            'imageBasename': imageBasename,
            'title': title
        })

    def close(self):
        with open('%s/index.html' % self._outputDir, 'w') as fp:
            self._writeHeader(fp)
            self._writeBody(fp)
            self._writeFooter(fp)
        with open('%s/style.css' % self._outputDir, 'w') as fp:
            self._writeCSS(fp)

    def _writeHeader(self, fp):
        fp.write("""\
<html>
  <head>
    <title>Read alignments for %d matched subjects</title>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div id="content">
        """ % len(self._images))

    def _writeBody(self, fp):
        fp.write('<h1>Read alignments for %d matched subjects</h1>\n' %
                 len(self._images))

        # Write out an alignment panel as a table.
        cols = 6
        fp.write('<table><tbody>\n')

        for i, image in enumerate(self._images):
            title = image['title']

            if i % cols == 0:
                fp.write('<tr>\n')

            fp.write(
                '<td><a id="small_%d"></a><a href="#big_%d"><img src="%s" '
                'class="thumbnail"/></a></td>\n' %
                (i, i, image['imageBasename']))

            if i % cols == cols - 1:
                fp.write('</tr>')

        # Add empty cells to the final table row, and close the row, if
        # necessary.
        if i % cols < cols - 1:
            while i % cols < cols - 1:
                fp.write('<td>&nbsp;</td>\n')
                i += 1
            fp.write('</tr>\n')

        fp.write('</tbody></table>\n')

        # Write out the full images with additional detail.
        for i, image in enumerate(self._images):
            title = image['title']
            titleAlignments = self._titlesAlignments[title]
            graphInfo = image['graphInfo']
            self._writeFASTA(i, image)
            fp.write("""
      <a id="big_%d"></a>
      <h3>%d: %s</h3>
      <p>
            Length: %d.
            Read count: %d.
            HSP count: %d.
            <a href="%d.fasta">fasta</a>.
            <a href="#small_%d">Top panel.</a>
"""
                     % (i, i, title,
                        titleAlignments.subjectLength,
                        titleAlignments.readCount(),
                        titleAlignments.hspCount(), i, i))

            url = NCBISequenceLinkURL(title)
            if url:
                fp.write('<a href="%s" target="_blank">NCBI</a>.' % url)

            # Write out feature information.
            if graphInfo['features'] is None:
                # Feature lookup was False (or we were offline).
                pass
            elif len(graphInfo['features']) == 0:
                fp.write('There were no features.')
            else:
                fp.write('<a href="%s">Features</a>' %
                         self._writeFeatures(i, image))

            # Write out the titles that this title invalidated due to its
            # read set.
            readSetFilter = self._titlesAlignments.readSetFilter
            if readSetFilter:
                invalidated = readSetFilter.invalidates(title)
                if invalidated:
                    nInvalidated = len(invalidated)
                    fp.write('<br/>This title invalidated %d other%s due to '
                             'its read set:<ul>'
                             % (nInvalidated,
                                '' if nInvalidated == 1 else 's'))
                    for title in invalidated:
                        fp.write('<li>%s</li>' % title)
                    fp.write('</ul>')

            fp.write(
                '</p><img src="%s" class="full-size"/>' %
                image['imageBasename'])

    def _writeFooter(self, fp):
        fp.write("""\
    </div>
  </body>
</html>
""")

    def _writeCSS(self, fp):
        fp.write("""\
#content {
  width: 95%;
  margin: auto;
}
img.thumbnail {
  height: 300px;
}
img.full-size {
  height: 900px;
}
""")

    def _writeFASTA(self, i, image):
        """
        Write a FASTA file containing the set of reads that hit a sequence.

        @param i: The number of the image in self._images.
        @param image: A member of self._images.
        """
        filename = '%s/%d.fasta' % (self._outputDir, i)
        titleAlignments = self._titlesAlignments[image['title']]
        with open(filename, 'w') as fp:
            for titleAlignment in titleAlignments:
                fp.write(titleAlignment.read.toString('fasta'))

    def _writeFeatures(self, i, image):
        """
        Write a text file containing the features as a table.

        @param i: The number of the image in self._images.
        @param image: A member of self._images.
        @return: The C{str} features file name - just the base name, not
            including the path to the file.
        """
        basename = 'features-%d.txt' % i
        filename = '%s/%s' % (self._outputDir, basename)
        featureList = image['graphInfo']['features']
        with open(filename, 'w') as fp:
            for feature in featureList:
                fp.write('%s\n\n' % feature.feature)
        return basename
