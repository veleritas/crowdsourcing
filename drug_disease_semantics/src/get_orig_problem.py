# last updated 2015-04-15 toby
"""
Grabs the original sentence for each work unit.
"""
import re

def get_orig_problem(column_name, data):
    result = dict()
    for identifier, group in data.groupby(column_name):
        assert len(group["original_sentence"].unique()) == 1
        assert len(group["subject_text"].unique()) == 1
        assert len(group["object_text"].unique()) == 1

        sentence = group["original_sentence"].iloc[0]
        sub_text = group["subject_text"].iloc[0]
        obj_text = group["object_text"].iloc[0]

        form_sent = group["formatted_sentence"].iloc[0]

        temp = re.sub(r'</?div.*?>', '', form_sent)
        temp = re.sub(r'<span.*?>', '[[', temp)
        temp = re.sub(r'</span>', ']]', temp)

        result[identifier] = (sub_text, obj_text, sentence, temp)

    return result
