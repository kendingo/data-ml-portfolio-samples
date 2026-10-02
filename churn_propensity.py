"""Churn propensity model on synthetic subscription data.

Portfolio sample: generates a synthetic customer table, engineers features,
trains a baseline logistic regression and reports AUC and top-decile lift.
No real customer data is used.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def make_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "tenure_months": rng.integers(1, 60, n),
        "sessions_30d": rng.poisson(8, n),
        "support_tickets_90d": rng.poisson(1.2, n),
        "monthly_spend": rng.gamma(4, 8, n).round(2),
    })
    logit = (-0.04 * df.tenure_months - 0.12 * df.sessions_30d
             + 0.45 * df.support_tickets_90d - 0.01 * df.monthly_spend + 1.2)
    df["churned"] = rng.random(n) < 1 / (1 + np.exp(-logit))
    return df


def top_decile_lift(y_true: np.ndarray, scores: np.ndarray) -> float:
    k = max(1, len(scores) // 10)
    top = np.argsort(scores)[::-1][:k]
    return float(y_true[top].mean() / y_true.mean())


def main() -> None:
    df = make_data()
    X, y = df.drop(columns="churned"), df["churned"].astype(int).to_numpy()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
    model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    p = model.predict_proba(X_te)[:, 1]
    print(f"AUC: {roc_auc_score(y_te, p):.3f}")
    print(f"Top-decile lift: {top_decile_lift(y_te, p):.2f}x")
    for name, coef in zip(X.columns, model.coef_[0]):
        print(f"  {name}: {coef:+.3f}")


if __name__ == "__main__":
    main()
