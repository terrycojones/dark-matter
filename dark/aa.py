# From https://en.wikipedia.org/wiki/Amino_acid
#
# Alanine          Ala     A
# Arginine         Arg     R
# Asparagine       Asn     N
# Aspartic acid    Asp     D
# Cysteine         Cys     C
# Glutamic acid    Glu     E
# Glutamine        Gln     Q
# Glycine          Gly     G
# Histidine        His     H
# Isoleucine       Ile     I
# Leucine          Leu     L
# Lysine           Lys     K
# Methionine       Met     M
# Phenylalanine    Phe     F
# Proline          Pro     P
# Serine           Ser     S
# Threonine        Thr     T
# Tryptophan       Trp     W
# Tyrosine         Tyr     Y
# Valine           Val     V

NAMES = {
    'A': 'Alanine',
    'R': 'Arginine',
    'N': 'Asparagine',
    'D': 'Aspartic acid',
    'C': 'Cysteine',
    'E': 'Glutamic acid',
    'Q': 'Glutamine',
    'G': 'Glycine',
    'H': 'Histidine',
    'I': 'Isoleucine',
    'L': 'Leucine',
    'K': 'Lysine',
    'M': 'Methionine',
    'F': 'Phenylalanine',
    'P': 'Proline',
    'S': 'Serine',
    'T': 'Threonine',
    'V': 'Valine',
    'W': 'Tryptophan',
    'Y': 'Tyrosine',
}

AA_LETTERS = sorted(NAMES.keys())

NAMES_TO_ABBREV1 = dict((name, abbrev1) for abbrev1, name in NAMES.items())

ABBREV3 = {
    'A': 'Ala',
    'R': 'Arg',
    'N': 'Asn',
    'D': 'Asp',
    'C': 'Cys',
    'E': 'Glu',
    'Q': 'Gln',
    'G': 'Gly',
    'H': 'His',
    'I': 'Ile',
    'L': 'Leu',
    'K': 'Lys',
    'M': 'Met',
    'F': 'Phe',
    'P': 'Pro',
    'S': 'Ser',
    'T': 'Thr',
    'V': 'Val',
    'W': 'Trp',
    'Y': 'Tyr',
}

ABBREV3_TO_ABBREV1 = dict((abbrev3, abbrev1)
                          for abbrev1, abbrev3 in ABBREV3.items())

HYDROPHOBIC = 0x0001
HYDROPHILIC = 0x0002
AROMATIC = 0x0004
SULPHUR = 0x0008
ALIPHATIC = 0x0010
HYDROXYLIC = 0x0020
TINY = 0x0040
SMALL = 0x0080
ACIDIC = 0x0100
BASIC_POSITIVE = 0x0200
NEGATIVE = 0x0400
POLAR = 0x0800
NONE = 0x1000


ALL_PROPERTIES = (
    ACIDIC, ALIPHATIC, AROMATIC, BASIC_POSITIVE, HYDROPHILIC,
    HYDROPHOBIC, HYDROXYLIC, NEGATIVE, NONE, POLAR, SMALL, SULPHUR, TINY)

PROPERTY_NAMES = {
    ACIDIC: 'Acidic',
    ALIPHATIC: 'Aliphatic',
    AROMATIC: 'Aromatic',
    BASIC_POSITIVE: 'Basic positive',
    HYDROPHILIC: 'Hydrophilic',
    HYDROPHOBIC: 'Hydrophobic',
    HYDROXYLIC: 'Hydroxylic',
    NEGATIVE: 'Negative',
    NONE: '<NONE>',
    POLAR: 'Polar',
    SMALL: 'Small',
    SULPHUR: 'Sulphur',
    TINY: 'Tiny',
}

PROPERTIES = {
    'A': HYDROPHOBIC | SMALL | TINY,
    'C': HYDROPHOBIC | SMALL | TINY | SULPHUR,
    'D': HYDROPHILIC | SMALL | POLAR | NEGATIVE,
    'E': HYDROPHILIC | NEGATIVE | ACIDIC,
    'F': HYDROPHOBIC | AROMATIC,
    'G': HYDROPHILIC | SMALL | TINY,
    'H': HYDROPHOBIC | AROMATIC | POLAR | BASIC_POSITIVE,
    'I': ALIPHATIC | HYDROPHOBIC,
    'K': HYDROPHOBIC | BASIC_POSITIVE | POLAR,
    'L': ALIPHATIC | HYDROPHOBIC,
    'M': HYDROPHOBIC | SULPHUR,
    'N': HYDROPHILIC | SMALL | POLAR | ACIDIC,
    'P': HYDROPHILIC | SMALL,
    'Q': HYDROPHILIC | POLAR | ACIDIC,
    'R': HYDROPHILIC | POLAR | BASIC_POSITIVE,
    'S': HYDROPHILIC | SMALL | POLAR | HYDROXYLIC,
    'T': HYDROPHOBIC | SMALL | HYDROXYLIC,
    'V': ALIPHATIC | HYDROPHOBIC | SMALL,
    'W': HYDROPHOBIC | AROMATIC | POLAR,
    'Y': HYDROPHOBIC | AROMATIC | POLAR,
}


# A table with which codons translate to which amino acids.
# Based on information from: http://wang.salk.edu/research.php

CODONS = {
    'A': ['GCC', 'GCA'],
    'C': ['TGT', 'TGC'],
    'D': ['GAT', 'GAC'],
    'E': ['GAA', 'GAG'],
    'F': ['TTT', 'TTC'],
    'G': ['GGC', 'GGA'],
    'H': ['CAT', 'CAC'],
    'I': ['ATC', 'ATA'],
    'K': ['AAA', 'AAG'],
    'L': ['TTA', 'TTG', 'CTC', 'CTA'],
    'M': ['ATG'],
    'N': ['AAT', 'AAC'],
    'P': ['CCC', 'CCA'],
    'Q': ['CAA', 'CAG'],
    'R': ['CGC', 'CGA', 'AGA', 'AGG'],
    'S': ['TCC', 'TCA', 'AGT', 'AGC'],
    'T': ['ACC', 'ACA'],
    'V': ['GTC', 'GTA'],
    'W': ['TGG'],
    'Y': ['TAT', 'TAC'],
}


"""
The dictionary below contains for each amino acid the value for
each property scaled from -1 to 1.
For documentation, check https://notebooks.antigenic-cartography.org/barbara/
pages/features/aa-properties.html
"""

PROPERTY_DETAILS = {
    'A': {
        'aliphaticity': 0.305785123967,
        'aromaticity': -0.550128534704,
        'composition': -1.0,
        'hydrogenation': 0.8973042362,
        'hydropathy': 0.4,
        'hydroxythiolation': -0.265160523187,
        'iep': -0.191489361702,
        'polar requirement': -0.463414634146,
        'polarity': -0.20987654321,
        'volume': -0.664670658683,
    },
    'C': {
        'aliphaticity': -0.00826446280992,
        'aromaticity': -0.740359897172,
        'composition': 1.0,
        'hydrogenation': 0.240051347882,
        'hydropathy': 0.555555555556,
        'hydroxythiolation': 0.785969084423,
        'iep': -0.424280350438,
        'polar requirement': -1.0,
        'polarity': -0.851851851852,
        'volume': -0.377245508982,
    },
    'D': {
        'aliphaticity': -0.818181818182,
        'aromaticity': -1.0,
        'composition': 0.00363636363636,
        'hydrogenation': -0.90243902439,
        'hydropathy': -0.777777777778,
        'hydroxythiolation': -0.348394768133,
        'iep': -1.0,
        'polar requirement': 1.0,
        'polarity': 1.0,
        'volume': -0.389221556886,
    },
    'E': {
        'aliphaticity': -0.553719008264,
        'aromaticity': -0.899742930591,
        'composition': -0.330909090909,
        'hydrogenation': -1.0,
        'hydropathy': -0.777777777778,
        'hydroxythiolation': -0.555291319857,
        'iep': -0.887359198999,
        'polar requirement': 0.878048780488,
        'polarity': 0.827160493827,
        'volume': -0.0419161676647,
    },
    'F': {
        'aliphaticity': 0.223140495868,
        'aromaticity': 0.858611825193,
        'composition': -1.0,
        'hydrogenation': 0.0218228498074,
        'hydropathy': 0.622222222222,
        'hydroxythiolation': 0.0582639714625,
        'iep': -0.321652065081,
        'polar requirement': -0.951219512195,
        'polarity': -0.925925925926,
        'volume': 0.544910179641,
    },
    'G': {
        'aliphaticity': -1.0,
        'aromaticity': -0.45501285347,
        'composition': -0.461818181818,
        'hydrogenation': 1.0,
        'hydropathy': -0.0888888888889,
        'hydroxythiolation': -0.158145065398,
        'iep': -0.198998748436,
        'polar requirement': -0.243902439024,
        'polarity': 0.0123456790123,
        'volume': -1.0,
    },
    'H': {
        'aliphaticity': -0.256198347107,
        'aromaticity': 0.555269922879,
        'composition': -0.578181818182,
        'hydrogenation': -0.150192554557,
        'hydropathy': -0.711111111111,
        'hydroxythiolation': 0.0154577883472,
        'iep': 0.206508135169,
        'polar requirement': -0.121951219512,
        'polarity': 0.358024691358,
        'volume': 0.11377245509,
    },
    'I': {
        'aliphaticity': 0.867768595041,
        'aromaticity': -0.264781491003,
        'composition': -1.0,
        'hydrogenation': 0.432605905006,
        'hydropathy': 1.0,
        'hydroxythiolation': -0.85255648038,
        'iep': -0.18648310388,
        'polar requirement': -0.975609756098,
        'polarity': -0.925925925926,
        'volume': 0.293413173653,
    },
    'K': {
        'aliphaticity': 0.123966942149,
        'aromaticity': -0.141388174807,
        'composition': -0.76,
        'hydrogenation': -0.142490372272,
        'hydropathy': -0.866666666667,
        'hydroxythiolation': -1.0,
        'iep': 0.744680851064,
        'polar requirement': 0.292682926829,
        'polarity': 0.58024691358,
        'volume': 0.389221556886,
    },
    'L': {
        'aliphaticity': 1.0,
        'aromaticity': -0.287917737789,
        'composition': -1.0,
        'hydrogenation': 0.381258023107,
        'hydropathy': 0.844444444444,
        'hydroxythiolation': -0.745541022592,
        'iep': -0.196495619524,
        'polar requirement': -0.975609756098,
        'polarity': -1.0,
        'volume': 0.293413173653,
    },
    'M': {
        'aliphaticity': 0.537190082645,
        'aromaticity': -0.372750642674,
        'composition': -1.0,
        'hydrogenation': -0.186136071887,
        'hydropathy': 0.422222222222,
        'hydroxythiolation': 0.0653983353151,
        'iep': -0.256570713392,
        'polar requirement': -0.878048780488,
        'polarity': -0.802469135802,
        'volume': 0.221556886228,
    },
    'N': {
        'aliphaticity': 0.471074380165,
        'aromaticity': -0.616966580977,
        'composition': -0.0327272727273,
        'hydrogenation': -0.548138639281,
        'hydropathy': -0.777777777778,
        'hydroxythiolation': 0.277051129608,
        'iep': -0.339173967459,
        'polar requirement': 0.268292682927,
        'polarity': 0.654320987654,
        'volume': -0.365269461078,
    },
    'P': {
        'aliphaticity': -0.917355371901,
        'aromaticity': -0.308483290488,
        'composition': -0.716363636364,
        'hydrogenation': 1.0,
        'hydropathy': -0.355555555556,
        'hydroxythiolation': -0.203329369798,
        'iep': -0.116395494368,
        'polar requirement': -0.560975609756,
        'polarity': -0.234567901235,
        'volume': -0.646706586826,
    },
    'Q': {
        'aliphaticity': 0.652892561983,
        'aromaticity': -0.439588688946,
        'composition': -0.352727272727,
        'hydrogenation': -0.602053915276,
        'hydropathy': -0.777777777778,
        'hydroxythiolation': -0.177170035672,
        'iep': -0.279098873592,
        'polar requirement': -0.0731707317073,
        'polarity': 0.382716049383,
        'volume': -0.0179640718563,
    },
    'R': {
        'aliphaticity': -0.157024793388,
        'aromaticity': -0.0642673521851,
        'composition': -0.527272727273,
        'hydrogenation': -0.401797175866,
        'hydropathy': -1.0,
        'hydroxythiolation': -0.51486325802,
        'iep': 1.0,
        'polar requirement': 0.0487804878049,
        'polarity': 0.382716049383,
        'volume': 0.449101796407,
    },
    'S': {
        'aliphaticity': 0.256198347107,
        'aromaticity': -0.660668380463,
        'composition': 0.0327272727273,
        'hydrogenation': 0.106546854942,
        'hydropathy': -0.177777777778,
        'hydroxythiolation': 1.0,
        'iep': -0.271589486859,
        'polar requirement': -0.341463414634,
        'polarity': 0.0617283950617,
        'volume': -0.652694610778,
    },
    'T': {
        'aliphaticity': -0.123966942149,
        'aromaticity': -0.80205655527,
        'composition': -0.483636363636,
        'hydrogenation': 0.399229781772,
        'hydropathy': -0.155555555556,
        'hydroxythiolation': 0.709869203329,
        'iep': -0.151439299124,
        'polar requirement': -0.560975609756,
        'polarity': -0.0864197530864,
        'volume': -0.305389221557,
    },
    'V': {
        'aliphaticity': 0.570247933884,
        'aromaticity': -0.665809768638,
        'composition': -1.0,
        'hydrogenation': 0.679075738126,
        'hydropathy': 0.933333333333,
        'hydroxythiolation': -0.621878715815,
        'iep': -0.201501877347,
        'polar requirement': -0.80487804878,
        'polarity': -0.753086419753,
        'volume': -0.0299401197605,
    },
    'W': {
        'aliphaticity': -0.619834710744,
        'aromaticity': 1.0,
        'composition': -0.905454545455,
        'hydrogenation': 0.0218228498074,
        'hydropathy': -0.2,
        'hydroxythiolation': 0.00118906064209,
        'iep': -0.219023779725,
        'polar requirement': -0.90243902439,
        'polarity': -0.876543209877,
        'volume': 1.0,
    },
    'Y': {
        'aliphaticity': -0.454545454545,
        'aromaticity': 0.712082262211,
        'composition': -0.854545454545,
        'hydrogenation': -0.304236200257,
        'hydropathy': 0.288888888889,
        'hydroxythiolation': 0.405469678954,
        'iep': -0.276595744681,
        'polar requirement': -0.853658536585,
        'polarity': -0.679012345679,
        'volume': 0.592814371257,
    },
}


"""
Clusters based on raw amino acid property values. See
https://notebooks.antigenic-cartography.org/barbara/pages/features/
aa-properties.html and https://notebooks.antigenic-cartography.org/barbara/
pages/features/new-tps.html
"""

PROPERTY_CLUSTERS = {
    'A': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 3,
        'hydroxythiolation': 2,
        'iep': 2,
        'polar requirement': 2,
        'polarity': 2,
        'volume': 2,
    },
    'C': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 3,
        'hydrogenation': 1,
        'hydropathy': 3,
        'hydroxythiolation': 5,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 3,
    },
    'D': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 2,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 2,
        'iep': 1,
        'polar requirement': 4,
        'polarity': 4,
        'volume': 3,
    },
    'E': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 1,
        'iep': 1,
        'polar requirement': 4,
        'polarity': 4,
        'volume': 4,
    },
    'F': {
        'aliphaticity': 1,
        'aromaticity': 2,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 3,
        'hydroxythiolation': 3,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 4,
    },
    'G': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 2,
        'hydroxythiolation': 2,
        'iep': 2,
        'polar requirement': 2,
        'polarity': 2,
        'volume': 1,
    },
    'H': {
        'aliphaticity': 1,
        'aromaticity': 2,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 3,
        'iep': 3,
        'polar requirement': 2,
        'polarity': 3,
        'volume': 4,
    },
    'I': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 4,
        'hydroxythiolation': 1,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 4,
    },
    'K': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 1,
        'iep': 3,
        'polar requirement': 3,
        'polarity': 4,
        'volume': 4,
    },
    'L': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 4,
        'hydroxythiolation': 1,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 4,
    },
    'M': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 3,
        'hydroxythiolation': 3,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 4,
    },
    'N': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 2,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 4,
        'iep': 2,
        'polar requirement': 3,
        'polarity': 4,
        'volume': 3,
    },
    'P': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 2,
        'hydroxythiolation': 2,
        'iep': 2,
        'polar requirement': 2,
        'polarity': 2,
        'volume': 2,
    },
    'Q': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 2,
        'iep': 2,
        'polar requirement': 2,
        'polarity': 3,
        'volume': 4,
    },
    'R': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 1,
        'hydroxythiolation': 1,
        'iep': 3,
        'polar requirement': 2,
        'polarity': 3,
        'volume': 4,
    },
    'S': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 2,
        'hydrogenation': 1,
        'hydropathy': 2,
        'hydroxythiolation': 5,
        'iep': 2,
        'polar requirement': 2,
        'polarity': 2,
        'volume': 2,
    },
    'T': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 2,
        'hydroxythiolation': 5,
        'iep': 2,
        'polar requirement': 2,
        'polarity': 2,
        'volume': 3,
    },
    'V': {
        'aliphaticity': 1,
        'aromaticity': 1,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 4,
        'hydroxythiolation': 1,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 4,
    },
    'W': {
        'aliphaticity': 1,
        'aromaticity': 2,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 2,
        'hydroxythiolation': 3,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 5,
    },
    'Y': {
        'aliphaticity': 1,
        'aromaticity': 2,
        'composition': 1,
        'hydrogenation': 1,
        'hydropathy': 2,
        'hydroxythiolation': 4,
        'iep': 2,
        'polar requirement': 1,
        'polarity': 1,
        'volume': 4,
    },
}


class AminoAcid(object):
    """
    Hold information about an amino acid.

    @param name: The full C{str} name of the amino acid.
    @param abbrev3: The 3-letter C{str} abbreviation of the amino acid,
        e.g., 'Arg'.
    @param abbrev1: The 1-letter C{str} abbreviation of the amino acid,
        e.g., 'A'.
    @param codons: A C{list} of 3-letter codons for the amino acid.
    @param properties: An C{int} logical-AND of the various properties
        (see PROPERTIES, above) of this amino acid.
    @param propertyDetails: A C{dict} containing property names and values
        for this amino acid. E.g.:
        {
            'aliphaticity': -0.157024793388,
            'aromaticity': -0.0642673521851,
            'composition': -0.527272727273,
            'hydrogenation': -0.401797175866,
            'hydropathy': -1.0,
            'hydroxythiolation': -0.51486325802,
            'iep': 1.0,
            'polar requirement': 0.0487804878049,
            'polarity': 0.382716049383,
            'volume': 0.449101796407,
        }
    @param propertyClusters: A C{dict} containing the property names and
        clusters for this amino acid. E.g.:
        {
            'aliphaticity': 1,
            'aromaticity': 2,
            'composition': 1,
            'hydrogenation': 1,
            'hydropathy': 2,
            'hydroxythiolation': 4,
            'iep': 2,
            'polar requirement': 1,
            'polarity': 1,
            'volume': 4,
        }
    """
    def __init__(self, name, abbrev3, abbrev1, codons, properties,
                 propertyDetails, propertyClusters):
        self.name = name
        self.abbrev3 = abbrev3
        self.abbrev1 = abbrev1
        self.codons = codons
        self.properties = properties
        self.propertyDetails = propertyDetails
        self.propertyClusters = propertyClusters


def find(s):
    """
    Find an amino acid whose name or abbreviation is s.

    @param s: A C{str} amino acid specifier. This may be a full name,
        a 3-letter abbreviation or a 1-letter abbreviation. Case is ignored.
    return: An L{AminoAcid} instance or C{None} if no matching amino acid can
        be located.
    """

    abbrev1 = None
    origS = s

    if ' ' in s:
        # Convert first word to title case, others to lower.
        first, rest = s.split(' ', 1)
        s = first.title() + ' ' + rest.lower()
    else:
        s = s.title()

    if s in NAMES:
        abbrev1 = s
    elif s in ABBREV3_TO_ABBREV1:
        abbrev1 = ABBREV3_TO_ABBREV1[s]
    elif s in NAMES_TO_ABBREV1:
        abbrev1 = NAMES_TO_ABBREV1[s]
    else:
        # Look for a 3-letter codon.
        def findCodon(target):
            for abbrev1, codons in CODONS.items():
                for codon in codons:
                    if codon == target:
                        return abbrev1

        abbrev1 = findCodon(origS.upper())

    if abbrev1:
        return AminoAcid(
            NAMES[abbrev1], ABBREV3[abbrev1], abbrev1, CODONS[abbrev1],
            PROPERTIES[abbrev1], PROPERTY_DETAILS[abbrev1],
            PROPERTY_CLUSTERS[abbrev1])


def propertiesForSequence(sequence, propertyNames, missingAAValue=-1.1):
    """
    Extract amino acid property values for a sequence.

    @param sequence: An C{AARead} (or a subclass) instance.
    @param propertyNames: An iterable of C{str} property names (each of which
        must be a key of a key in the dark.aa.PROPERTY_DETAILS dict).
    @param missingAAValue: A C{float} value to use for properties when an AA
        (e.g., 'X') is not known.
    @raise ValueError: If an unknown property is given in C{propertyNames}.
    @return: A C{dict} keyed by (lowercase) property name, with values that are
        C{list}s of the corresponding property value according to sequence
        position.
    """
    propertyNames = sorted(map(str.lower, set(propertyNames)))

    # Make sure all mentioned property names exist for at least one AA.
    knownProperties = set()
    for properties in PROPERTY_DETAILS.values():
        knownProperties.update(properties)
    unknown = set(propertyNames) - knownProperties
    if unknown:
        raise ValueError(
            'Unknown propert%s: %s.' %
            ('y' if len(unknown) == 1 else 'ies', ', '.join(unknown)))

    aas = sequence.sequence.upper()
    result = {}

    for propertyName in propertyNames:
        result[propertyName] = values = []
        for aa in aas:
            try:
                properties = PROPERTY_DETAILS[aa]
            except KeyError:
                # No such AA.
                values.append(missingAAValue)
            else:
                values.append(properties[propertyName])

    return result
