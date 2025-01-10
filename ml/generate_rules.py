import os
import pandas as pd
import pickle

from fpgrowth_py import fpgrowth

def main():
    dataset_path = os.environ.get("DATASET_PATH", "../local_data/2023_spotify_ds1.csv")
    output_path = os.environ.get("MODEL_PATH", "../local_data/model.pkl")

    print(f"[INFO] Reading dataset from: {dataset_path}")
    print(f"[INFO] Will save patterns/rules to: {output_path}")

    df = pd.read_csv(dataset_path, usecols=["pid", "track_name"])
    df["track_name"] = df["track_name"].str.strip().str.lower()

    transactions = df.groupby("pid")["track_name"].apply(list).tolist()

    print("[INFO] Running fpgrowth...")
    minSupRatio = 0.05
    minConf = 0.5

    patterns, rules = fpgrowth(transactions, minSupRatio, minConf)

    print(f"[INFO] Found {len(patterns)} frequent patterns.")
    print(f"[INFO] Found {len(rules)} rules.")

    print("[INFO] Saving results to pickle...")
    with open(output_path, 'wb') as f:
        pickle.dump({
            "patterns": patterns,
            "rules": rules
        }, f)

    print(f"[INFO] FP-Growth results saved at: {output_path}")

if __name__ == "__main__":
    main()
