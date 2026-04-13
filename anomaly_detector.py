"""
anomaly_detector.py
Uses scikit-learn Isolation Forest to detect anomalies in network interface stats.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def prepare_data(interface_stats):
      """Convert raw interface stats into a DataFrame."""
      df = pd.DataFrame(interface_stats)
      return df


def detect_anomalies(interface_stats, contamination=0.1):
      """
          Run Isolation Forest anomaly detection on interface statistics.

              Args:
                      interface_stats: List of interface stat dictionaries.
                              contamination: Expected proportion of anomalies (default 0.1).

                                  Returns:
                                          DataFrame with anomaly column (-1 = anomaly, 1 = normal).
                                              """
      if not interface_stats:
                print("No data to analyze.")
                return pd.DataFrame()

      df = prepare_data(interface_stats)

    feature_columns = [
              "crc_errors", "input_errors", "output_errors",
              "input_packets", "output_packets"
    ]
    features = df[feature_columns].copy()

    model = IsolationForest(
              n_estimators=100,
              contamination=contamination,
              random_state=42,
              verbose=0
    )

    df["anomaly"] = model.fit_predict(features)
    df["anomaly_score"] = model.decision_function(features)
    df["status_label"] = df["anomaly"].map({1: "Normal", -1: "Anomaly"})

    return df


def print_results(results_df):
      """Print anomaly detection results in a readable format."""
      if results_df.empty:
                print("No results to display.")
                return 0

      print("\nResults:")
      print("-" * 90)
      header = f"{'Device':<18} {'Interface':<22} {'CRC':<8} {'In Err':<10} {'Out Err':<10} {'Status':<12}"
      print(header)
      print("-" * 90)

    anomaly_count = 0
    for _, row in results_df.iterrows():
              status = "ANOMALY" if row["status_label"] == "Anomaly" else "Normal"
              line = f"{row['device']:<18} {row['interface']:<22} {row['crc_errors']:<8} "
              line += f"{row['input_errors']:<10} {row['output_errors']:<10} {status:<12}"
              print(line)
              if row["status_label"] == "Anomaly":
                            anomaly_count += 1

          print("-" * 90)

    if anomaly_count > 0:
              print(f"\n{anomaly_count} anomaly(ies) detected! Review flagged interfaces.")
else:
          print("\nNo anomalies detected. All interfaces look healthy.")

    return anomaly_count
