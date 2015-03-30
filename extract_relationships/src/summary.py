# last updated 2015-03-26 toby
import pandas as pd
from filter_data import filter_data
from true_relation_type import get_true_relation_type
from broad_relationships import determine_broad_relationship_matches
import pprint

def data_summary(settings):
    data = filter_data(settings)
    true_relation_type = get_true_relation_type(settings["combine_pos_and_spec"])
    results = determine_broad_relationship_matches(true_relation_type, data)

    if "show_raw" in settings and settings["show_raw"]:
        print results

    ans = pd.Series([0] * (4 - settings["combine_pos_and_spec"]))
    for unit_id, group in results.groupby("unit_id"):
        temp = list(group["match"]) # reset the indicies
        ans = ans.add(pd.Series(temp), fill_value = 0)

    num_work_units = len(results["unit_id"].unique())

    print "Distribution of matches with gold standard based on response rank:\n{0}".format(ans)
    print
    print ("Total number of work units for this subset of data: {0}".
        format(num_work_units))
    print
    print "Number of correct responses with respect to the rank of confidence score:"
    print ("{0}/{1} ({2}%) work units had the correct answer in the top ranked position".
           format(ans[0], num_work_units, ans[0]/num_work_units * 100))

    graph = ans.plot(kind = "bar")
    graph.set_xlabel("Rank of the correct choice according to the crowd")
    graph.set_ylabel("Number of work units where the crowd chosen top answer\n"\
        "matched that of the gold standard")
