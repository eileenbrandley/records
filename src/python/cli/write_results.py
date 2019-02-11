from python import write_results
import pandas as pd

RESULTS_DB = 'records' # Set as temp table for testing


if __name__ == "__main__":
    df = pd.read_csv("/Users/eileentoomer/Code/records/src/data/csv/all_po10_data.csv")
    not_saved = write_results.set_results_from_dataframe(df, RESULTS_DB)
    if len(not_saved) > 0:
        print("Following results not saved: {0}".format(", ".join(map(str, not_saved))))
    else:
        print("All saved correctly")