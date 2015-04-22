"""
Provides summaries about broad reltype performance and
deep semantic performance.
"""
import pandas as pd

from filter_data import filter_data
from true_relation_type import get_euadr_relation_type

from aggregate_results import aggregate_results
from aggregate_results import create_match

def broad_reltype_summary(settings):
    raw_data = filter_data(settings)

    true_relation_type = get_euadr_relation_type(settings)

    match_obj = create_match(true_relation_type)

    results = aggregate_results("sentence_claim", raw_data, match_obj)

#--------------------------------------------------------------------
    ans = pd.Series([0] * 5)
    for unit_id, group in results.groupby("unit_id"):
        temp = list(group["match"])
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

