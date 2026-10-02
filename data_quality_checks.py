"""Lightweight data quality checks for an events table (pandas).

Portfolio sample: checks for nulls, duplicates, late-arriving rows and
unexpected event names, and returns a structured report.
"""
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Report:
    passed: bool = True
    issues: list = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.passed = False
        self.issues.append(msg)


def check_events(df: pd.DataFrame, allowed_events: set, max_lag_hours: int = 24) -> Report:
    r = Report()
    for col in ("event_id", "user_id", "event_name", "event_ts", "received_ts"):
        if col not in df.columns:
            r.fail(f"missing column: {col}")
            return r
    nulls = df[["event_id", "user_id", "event_name", "event_ts"]].isna().sum()
    for col, n in nulls[nulls > 0].items():
        r.fail(f"{n} null values in {col}")
    dupes = int(df.duplicated("event_id").sum())
    if dupes:
        r.fail(f"{dupes} duplicate event_id values")
    lag = (pd.to_datetime(df.received_ts) - pd.to_datetime(df.event_ts)).dt.total_seconds() / 3600
    late = int((lag > max_lag_hours).sum())
    if late:
        r.fail(f"{late} events arrived more than {max_lag_hours}h late")
    unknown = set(df.event_name.dropna()) - allowed_events
    if unknown:
        r.fail(f"unexpected event names: {sorted(unknown)}")
    return r


if __name__ == "__main__":
    demo = pd.DataFrame({
        "event_id": [1, 2, 2, 4],
        "user_id": ["a", "b", "b", None],
        "event_name": ["page_view", "purchase", "purchase", "refund_x"],
        "event_ts": pd.to_datetime(["2026-01-01 10:00"] * 4),
        "received_ts": pd.to_datetime(["2026-01-01 10:05", "2026-01-01 10:06",
                                       "2026-01-01 10:06", "2026-01-03 12:00"]),
    })
    rep = check_events(demo, {"page_view", "purchase", "signup"})
    print("PASSED" if rep.passed else "FAILED")
    for i in rep.issues:
        print(" -", i)
