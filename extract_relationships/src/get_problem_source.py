# last updated 2015-03-30 toby
import re
import pandas as pd

def remove_tags(text):
    text = text.replace("&quot;", "")
    text = text.replace("<div class=\"formatted_sentence\" id=\"\" style=\"display: \">", "")
    text = text.replace("</span>", "")
    text = text.replace("<span class=\"subject_text\" id=\"\" style=\"display: \">", "")
    text = text.replace("<span class=\"object_text\" id=\"\" style=\"display: \">", "")
    text = text.replace("</div>", "")
    return text

def get_original_problem(unit_id):
    """
    Returns the subject text, object text, and sentence for this work unit id.
    """
    loc = "/home/toby/crowdsourcing/extract_relationships/results/analysis/"
    fname = "705001_full_with_untrusted_and_unfinished.csv"

    raw_data = pd.read_csv(loc + fname, sep = "\t")

    subset = raw_data[raw_data["_unit_id"] == unit_id]

    sentence = subset["formatted_sentence"].iloc[0]
    sub_text = subset["subject_text"].iloc[0]
    obj_text = subset["object_text"].iloc[0]

    sentence = remove_tags(sentence)
    sub_text = remove_tags(sub_text)
    obj_text = remove_tags(obj_text)

    sentence = sentence.replace(sub_text, "[[{0}]]".format(sub_text))
    sentence = sentence.replace(obj_text, "[[{0}]]".format(obj_text))

    return (sub_text, obj_text, sentence)
