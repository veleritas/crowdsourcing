# last updated 2015-03-26 toby
import pandas as pd
import os
from check_settings import has_proper_settings

def filter_data(settings):
    """
    Filters the raw CrowdFlower summary about the job down to the data
    that we care about.
    """
    def converter(text):
        """
        If we are treating positive and speculative assocations as the
        same thing, then this is the step at which the data are converted.
        """
        if text in ["positive", "speculative"]:
            return "are_linked"

        return text

    assert has_proper_settings(settings)

    data = pd.read_csv(os.path.join(settings["loc"], settings["fname"]), sep = "\t")

    if settings["data_subset"] == "gold":
        data = data.query("_golden")
    elif settings["data_subset"] == "normal":
        data = data.query("~_golden")

    data = (data.query("{0} <= _trust <= {1}".
        format(settings["min_accuracy"], settings["max_accuracy"])))

    if settings["link_type"] != "all":
        sub_type, obj_type = settings["link_type"].split('/')
        data = (data.query("subject_type == '{0}' and object_type == '{1}'".
            format(sub_type, obj_type)))

    if settings["combine_pos_and_spec"]:
        data.loc[:, "true_relation_type"] = data["true_relation_type"].map(converter)
        data.loc[:, "correlation_type"] = data["correlation_type"].map(converter)

    return data
