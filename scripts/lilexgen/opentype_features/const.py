"""Generator constants"""

SKIP_IGNORES = [
    # <<*>> <<+>> <<$>>
    ("less", "asterisk", "greater"),
    ("less", "plus", "greater"),
    ("less", "dollar", "greater"),
]

IGNORE_PREFIXES = [
    ("parenleft", "question", "colon"),
    # Regexp lookahead/lookbehind
    ("parenleft", "question", "colon"),
    ("parenleft", "question", "equal"),
    ("parenleft", "question", "less", "equal"),
    ("parenleft", "question", "exclam"),
    # PHP <?=
    ("less", "question", "equal"),
]

IGNORES = {
    ("slash", "asterisk"): [
        "slash' asterisk slash",
        "asterisk slash' asterisk",
    ],
    ("asterisk", "slash"): ["slash asterisk' slash", "asterisk' slash asterisk"],
    ("asterisk", "asterisk"): [
        "slash asterisk' asterisk",
        "asterisk' asterisk slash",
    ],
    ("asterisk", "asterisk", "asterisk"): [
        "slash asterisk' asterisk asterisk",
        "asterisk' asterisk asterisk slash",
    ],
    ("colon", "colon"): [
        "colon' colon [less greater]",
        "[less greater] colon' colon",
    ],
    ("colon", "colon", "colon"): [
        "colon' colon colon [less greater]",
        "[less greater] colon' colon colon",
    ],
    # <||>
    ("less", "bar", "bar"): ["less' bar bar greater"],
    ("bar", "bar", "greater"): ["less bar' bar greater"],
    # {|}
    ("braceleft", "bar"): ["braceleft' bar braceright"],
    ("bar", "braceright"): ["braceleft bar' braceright"],
    # [|]
    ("bracketleft", "bar"): ["bracketleft' bar bracketright"],
    ("bar", "bracketright"): ["bracketleft bar' bracketright"],
    # <*>>> <+>>> <$>>> >>->> >>=>> >>=
    ("greater", "greater"): [
        "[asterisk plus dollar] greater' greater",
        "[hyphen equal] greater' greater",
        "greater' greater hyphen",
        "greater' greater equal [equal less greater bar colon exclam slash]",
    ],
    # <*>>> <+>>> <$>>>
    ("greater", "greater", "greater"): [
        "[asterisk plus dollar] greater' greater greater"
    ],
    # <<*> <<+> <<$> <<-<< <<=<< <<=
    ("less", "less"): [
        "less' less [asterisk plus dollar]",
        "[hyphen equal] less' less",
        "less' less hyphen",
        "less' less equal [equal less greater bar colon exclam slash]",
    ],
    # <<<*> <<<+> <<<$>
    ("less", "less", "less"): ["less' less less [asterisk plus dollar]"],
    # =:=
    ("colon", "equal"): [
        "equal colon' equal",
    ],
    # =!=
    ("exclam", "equal"): [
        "equal exclam' equal",
    ],
    # =!==
    ("exclam", "equal", "equal"): [
        "equal exclam' equal equal",
    ],
    # =<= <=< <=> <=| <=: <=! <=/
    ("less", "equal"): [
        "equal less' equal",
        "less' equal [less greater bar colon exclam slash]",
    ],
    # >=< =>= >=> >=< >=| >=: >=! >=/
    ("greater", "equal"): [
        "equal greater' equal",
        "greater' equal [less greater bar colon exclam slash]",
    ],
    # ||-|| ||=|| ||=
    ("bar", "bar"): [
        "[hyphen equal] bar' bar",
        "bar' bar hyphen",
        "bar' bar equal [equal less greater bar colon exclam slash]",
    ],
    # //=
    ("slash", "slash"): [
        "equal slash' slash",
        "slash' slash equal",
    ],
    # <--> >--< |--|
    ("hyphen", "hyphen"): [
        "[less greater bar] hyphen' hyphen",
        "hyphen' hyphen [less greater bar]",
    ],
    # <==> >==< |==| /==/ =:== =!== ==:= ==!= [==[ ]==] [== ==]
    ("equal", "equal"): [
        "bracketleft equal' equal",
        "equal' equal bracketright",
        "equal [colon exclam] equal' equal",
        "[less greater bar slash] equal' equal",
        "equal' equal [less greater bar slash]",
        "equal' equal [colon exclam] equal",
    ],
    # <===> >===< |===| /===/ =:=== =!=== ===:= ===!= [===[ ]===] [=== ===]
    ("equal", "equal", "equal"): [
        "bracketleft equal' equal equal",
        "equal' equal equal bracketright",
        "equal [colon exclam] equal' equal equal",
        "[less greater bar slash] equal' equal equal",
        "equal' equal equal [less greater bar slash]",
        "equal' equal equal [colon exclam] equal",
    ],
}

# Replacement ignore templates map
# ignore sub
IGNORE_TPL = {
    2: ["1  1' 2", "1' 2  2"],
    3: ["1  1' 2  3", "1' 2  3  3"],
    4: ["1  1' 2  3  4", "1' 2  3  4  4"],
    5: ["1  1' 2  3  4", "1' 2  3  4  4"],
}


PRIORITIES = {
    # <|>
    ("less", "bar", "greater"): 0,
    # |||> ||> |> <| <|| <|||
    ("bar", "bar", "bar", "greater"): 1,
    ("bar", "bar", "greater"): 1,
    ("bar", "greater"): 1,
    ("less", "bar", "bar", "bar"): 1,
    ("less", "bar", "bar"): 1,
    ("less", "bar"): 1,
    # << <<< >> >>> || ||| before -- --- == ===
    ("less", "less"): 2,
    ("less", "less", "less"): 2,
    ("greater", "greater"): 2,
    ("greater", "greater", "greater"): 2,
    ("bar", "bar"): 2,
    ("bar", "bar", "bar"): 2,
}

# Replacement templates map
# sub
REPLACE_TPL = {
    2: ["1.spacer 2' by 1_2.liga", "1'       2  by 1.spacer"],
    3: [
        "1.spacer 2.spacer 3' by 1_2_3.liga",
        "1.spacer 2'       3  by 2.spacer",
        "1'       2        3  by 1.spacer",
    ],
    4: [
        "1.spacer 2.spacer 3.spacer 4' by 1_2_3_4.liga",
        "1.spacer 2.spacer 3'       4  by 3.spacer",
        "1.spacer 2'       3        4  by 2.spacer",
        "1'       2        3        4  by 1.spacer",
    ],
    5: [
        "1.spacer 2.spacer 3.spacer 4.spacer 5' by 1_2_3_4_5.liga",
        "1.spacer 2.spacer 3.spacer 4'       5  by 4.spacer",
        "1.spacer 2.spacer 3'       4        5  by 3.spacer",
        "1.spacer 2'       3        4        5  by 2.spacer",
        "1'       2        3        4        5  by 1.spacer",
    ],
}

NAME_TPL = {
    "ss": ('featureNames {\n  name 3 1 0x0409 "$NAME";\n};\n'),
    "cv": (
        'cvParameters {\n  FeatUILabelNameID{\n    name 3 1 0x0409 "$NAME";\n  };\n};\n'
    ),
}
