# last updated 2015-04-16 Tong Shu Li
"""
Takes raw CrowdFlower data and groups data together by
individual work units. Aggregates the votes based on
a specific column and creates a summary data frame.
"""
import pandas as pd
from aggregate_votes import aggregate_votes

def create_match(gold_std_answer):
    mapping = {
        "definite_relation": "positive",
        "uncertain_relation": "speculative",
        "inferred_relation": "false",
        "no_relation": "negative",
        "is_cooccurrence": "false"
    }
    def match(unit_id, crowd_choice):
        """
        Determines if the crowd's response matches the EU-ADR answer.
        """
        if crowd_choice in ["positive", "speculative", "false", "negative"]:
            return int(crowd_choice == gold_std_answer[unit_id])

        return int(mapping[crowd_choice] == gold_std_answer[unit_id])

    return match

def aggregate_results(id_column, agg_column, data, match = None):
    result = []
    for identifier, group in data.groupby(id_column):
        ans = aggregate_votes(agg_column, group)

        total_vote_score = sum(ans["conf_score"])
        percent_agree = ans["conf_score"] / total_vote_score

        ans["percent_agree"] = percent_agree
        ans.insert(0, id_column, identifier)

        if match is not None:
            matches = [match(identifier, crowd_choice) for crowd_choice in ans[agg_column]]
            ans["match"] = matches

        ans = ans.sort(["conf_score"], ascending = False)

        result.append(ans)

    return pd.concat(result)
