# last updated 2015-03-26 toby
import os

def has_proper_settings(settings):
    """
    Settings:
        1. data_subset: ["gold", "normal", "all"]
            differentiates between test questions and regular work
        2. min_accurarcy and max_accuracy: reals from 0 to 1. Workers
            with trust (accuracy) scores outside this range are disregarded.
        3. link_type: a string that specifies which semantic relationship subset
        4. loc: the directory of the file we want to read
        5. fname: the name of the file we are trying to read
        6. combine_pos_and_spec: a boolean stating whether we want to treat
            positive associations and speculative associations as the same thing
    """
    assert "loc" in settings, "No directory specified"
    assert "fname" in settings, "No file name specified"

    assert os.path.exists(os.path.join(settings["loc"], settings["fname"])), "File does not exist"

    assert "data_subset" in settings, "No data subset specified"
    assert settings["data_subset"] in ["all", "gold", "normal"], "Data subset is not a valid choice"

    assert "min_accuracy" in settings, "No minimum accuracy specified"
    assert 0 <= settings["min_accuracy"] <= 1, "Minimum accuracy is out of bounds"

    assert "max_accuracy" in settings, "No maximum accuracy specified"
    assert 0 <= settings["max_accuracy"] <= 1, "Maximum accuracy is out of bounds"

    assert settings["min_accuracy"] <= settings["max_accuracy"], \
        "Minimum accuracy is not less than maximum accuracy"

    all_link_types = set([
        "all", "disease/drug", "gene or protein/disease",
        "gene variant/disease", "gene or protein/drug",
        "gene variant/drug"
    ])

    assert "link_type" in settings, "No link type specified"
    assert settings["link_type"] in all_link_types, "Invalid choice of link type"

    assert "combine_pos_and_spec" in settings, "Whether to combine is not specified"
    assert isinstance(settings["combine_pos_and_spec"], bool), "Combine is not a boolean"

    return True
