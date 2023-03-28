"""Generator constants"""

IGNORE_PREFIXES = {
    'parenleft question': [
        'colon',
        'equal'
        'exclaim'
    ],
    'less question': ['equal'],
    'parenleft question less': [
        'equal',
        'exclaim'
    ],
}

# Replacement ignore templates map
# ignore sub
IGNORE_TEMPLATES = {
    2: [
        "1  1' 2",
        "1' 2  2"
    ],
    3: [
        "1  1' 2  3",
        "1' 2  3  3"
    ],
    4: [
        "1  1' 2  3  4",
        "1' 2  3  4  4"
    ]
}

# Replacement templates map
# sub
REPLACE_TEMPLATES = {
    2: [
        "LIG 2' by 1_2.liga",
        "1'  2  by LIG"
    ],
    3: [
        "LIG LIG 3' by 1_2_3.liga",
        "LIG 2'  3  by LIG",
        "1'  2   3  by LIG"
    ],
    4: [
        "LIG LIG LIG 4' by 1_2_3_4.liga",
        "LIG LIG 3'  4  by LIG",
        "LIG 2'  3   4  by LIG",
        "1'  2   3   4  by LIG"
    ]
}
