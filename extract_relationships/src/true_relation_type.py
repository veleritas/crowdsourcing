# last updated 2015-03-30 toby
from filter_data import filter_data

def get_true_relation_type(combine_pos_and_spec):
    """
    Returns the EU-ADR gold standard answer for the semantic
    relationship type for all work units in the original raw
    CrowdFlower data.
    """
    settings = {
        "data_subset": "all",
        "min_accuracy": 0.0,
        "max_accuracy": 1.0,
        "link_type": "all",
        "loc": "/home/toby/crowdsourcing/extract_relationships/results/analysis",
        "fname": "705001_full_with_untrusted_and_unfinished.csv",
        "combine_pos_and_spec": combine_pos_and_spec
    }

    all_data = filter_data(settings)

    true_relation_type = dict()
    for unit_id, group in all_data.groupby("_unit_id"):
        assert len(group["true_relation_type"].unique()) == 1
        true_relation_type[unit_id] = group["true_relation_type"].iloc[0]

    return true_relation_type
