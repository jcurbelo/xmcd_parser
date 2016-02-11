id_define_dict1 = {
    "@disable-calc": "false",
    "@optimize": "true",
    "ml:define": {
        "@xmlns:ml": "http://schemas.mathsoft.com/math30",
        "ml:id": {
            "#text": "F",
            "@subscript": "tu",
            "@xml:space": "preserve"
        },
        "ml:real": "38.00"
    }
}
id_define_dict2 = {
    "@disable-calc": "false",
    "@optimize": "true",
    "ml:define": {
        "@xmlns:ml": "http://schemas.mathsoft.com/math30",
        "ml:id": {
            "#text": "F",
            "@subscript": "su",
            "@xml:space": "preserve"
        },
        "ml:real": "24.00"
    }
}
div_with_two_literals = {"ml:apply": {
    "ml:div": None,
    "ml:real": [
        "1",
        "2"
    ]
}}
div_with_two_access = {
    "ml:apply": {
        "ml:div": None,
        "ml:id": [
            {
                "#text": "B",
                "@subscript": "p",
                "@xml:space": "preserve"
            },
            {
                "#text": "E",
                "@xml:space": "preserve"
            }
        ]
    }
}
div_with_one_literal_one_access = {"ml:apply": {
    "ml:div": None,
    "ml:id": {
        "#text": "n",
        "@subscript": "y",
        "@xml:space": "preserve"
    },
    "ml:real": "1"
}}

pow_with_two_literals = {"ml:apply": {
    "ml:pow": None,
    "ml:real": [
        "3.1416",
        "2"
    ]
}}
