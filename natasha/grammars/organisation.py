# coding: utf-8
from __future__ import unicode_literals

from enum import Enum
from yargy.labels import (
    gram,
    gram_not,
    gram_any,
    gram_not_in,
    gnc_match,
    in_,
    is_lower,
    dictionary,
    eq,
    is_capitalized,
    and_,
    or_,
    label,
    string_required
)
from yargy.normalization import NormalizationType
from natasha.grammars import Person


@label
@string_required
def is_abbr(case, token, value):
    '''
    Returns true if token contains only uppercased letters
    '''
    return token.value.isupper() == case


class Organisation(Enum):

    OfficialQuoted = [
        {
            'labels': [
                or_((
                    gram('Orgn/Commercial'),
                    gram('Orgn/Abbr'),
                )),
            ],
        },
        {
            'labels': [
                is_abbr(True),
            ],
            'optional': True,
            'repeatable': True,
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
        {
            'labels': [
                gram_not('QUOTE'),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
    ]

    PrefixAndNoun = [
        {
            'labels': [
                and_((
                    gram('Orgn/Commercial'),
                    or_((
                        gram('sing'),
                        gram('Sgtm'),
                    ))
                )),
            ],
        },
        {
            'labels': [
                gram('NOUN'),
                gram_not('Orgn/Abbr'),
                is_capitalized(True),
                gnc_match(-1, solve_disambiguation=True)
            ],
            'repeatable': True,
        },
    ]

    Abbr = [
        {
            'labels': [
                gram('Abbr'),
                gram('Orgn'),
                gram_not('Orgn/Abbr'),
            ]
        },
    ]

    IndividualEntrepreneur = [
        {
            'labels': [
                eq('ИП'),
            ],
        },
        Person.Full.value[0],
        Person.Full.value[1],
        Person.Full.value[2],
    ]

    SimpleLatin = [
        {
            'labels': [
                gram('Orgn/Commercial'),
            ],
        },
        {
            'labels': [
                gram_any({
                    'LATN',
                    'NUMBER',
                }),
            ],
            'repeatable': True,
        },
    ]

    # Санкт-Петербургский Государственный университет
    Educational = [
        {
            'labels': [
                gram('ADJF'),
                is_capitalized(True),
            ],
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
        },
        {
            'labels': [
                gram('Orgn/Educational'),
                gnc_match(-1, solve_disambiguation=True),
            ],
        }
    ]

    # Общества андрологии и сексуальной медицины
    Social = [
        {
            'labels': [
                gram('Orgn/Social'),
            ],
            'normalization': NormalizationType.Inflected,
        },
        {
            'labels': [
                gram_not_in({
                    'PREP',
                    'CONJ',
                }),
                gram_any({
                    'datv',
                    'gent',
                    'Orgn',
                }),
                gram_not_in({
                    'Name',
                    'Patr',
                    'Surn',
                }),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'normalization': NormalizationType.Original,
        },
        {
            'labels': [
                or_((
                    gram_any({
                        'datv',
                        'gent',
                        'ablt',
                        'Orgn',
                    }),
                    gram_any({
                        'PREP',
                        'CONJ',
                    }),
                )),
                gram_not_in({
                    'Name',
                    'Patr',
                    'Surn',
                }),
            ],
            'optional': True,
            'repeatable': True,
            'normalization': NormalizationType.Original,
        },
    ]

    AdjSocial = [
        {
            'labels': [
                gram('ADJF'),
                is_capitalized(True),
            ],
        },
        {
            'labels': [
                gram('ADJF'),
                gnc_match(-1, solve_disambiguation=True),
            ],
            'optional': True,
            'repeatable': True,
        },
        {
            'labels': [
                gram('Orgn/Social'),
                is_lower(True),
                gnc_match(-1, solve_disambiguation=True),
            ]
        },
        Social[-1],
    ]

class ProbabilisticOrganisation(Enum):

    # "Коммерсантъ" сообщил ...
    NounQuoted = [
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
        {
            'labels': [
                is_capitalized(True),
            ],
            'repeatable': True,
        },
        {
            'labels': [
                gram('QUOTE'),
            ],
        },
    ]
