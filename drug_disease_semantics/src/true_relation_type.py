# last updated 2015-04-04 toby
from filter_data import filter_data

def get_euadr_relation_type(settings):
    """
    Returns the EU-ADR answer for the semantic relationship
    type for all work units.
    """
    all_data = filter_data(settings)

    euadr_relation_type = dict()
    for identifier, group in all_data.groupby(settings["id_column"]):
        assert len(group["gold_std_association_type"].unique()) == 1
        euadr_relation_type[identifier] = group["gold_std_association_type"].iloc[0]

    return euadr_relation_type
