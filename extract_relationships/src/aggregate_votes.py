# last updated 2015-03-30 toby
import pandas as pd

def aggregate_votes(data):
    """
    Given all of the human responses for the broad relationship between
    two concepts for one work unit, aggregates the results for the four
    possible answers (PA, NA, SA, FA). For each choice, calcuates the
    total number of votes, the confidence score, and the percentage
    agreement. Sorts results in decreasing order of confidence score.

    Confidence score is the sum of the accuracy scores of the individuals.
    """
    temp = []
    for correlation_type, group in data.groupby("correlation_type"):
        conf_score = sum(group["_trust"])
        num_votes = len(group)
        temp.append([correlation_type, conf_score, num_votes])

    return pd.DataFrame(temp, columns = ["relation_type", "conf_score", "num_votes"])
