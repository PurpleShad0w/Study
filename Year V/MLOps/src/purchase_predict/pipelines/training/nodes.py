import numpy as np
import pandas as pd
import os
import mlflow

from mlflow.models import infer_signature

from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
from sklearn.metrics import precision_recall_curve, PrecisionRecallDisplay

from typing import Callable, Tuple, Any, Dict

from sklearn.base import BaseEstimator
from sklearn.metrics import f1_score
from sklearn.model_selection import RepeatedKFold

from lightgbm.sklearn import LGBMClassifier

from hyperopt import hp, tpe, fmin

import warnings

warnings.filterwarnings("ignore")


MODELS = [
    {
        "name": "LightGBM",
        "class": LGBMClassifier,
        "params": {
            "objective": "binary",
            "verbose": -1,
            "learning_rate": hp.uniform("learning_rate", 0.001, 1),
            "num_iterations": hp.quniform("num_iterations", 100, 1000, 20),
            "max_depth": hp.quniform("max_depth", 4, 12, 6),
            "num_leaves": hp.quniform("num_leaves", 8, 128, 10),
            "colsample_bytree": hp.uniform("colsample_bytree", 0.3, 1),
            "subsample": hp.uniform("subsample", 0.5, 1),
            "min_child_samples": hp.quniform("min_child_samples", 1, 20, 10),
            "reg_alpha": hp.choice("reg_alpha", [0, 1e-1, 1, 2, 5, 10]),
            "reg_lambda": hp.choice("reg_lambda", [0, 1e-1, 1, 2, 5, 10]),
        },
        "override_schemas": {
            "num_leaves": int,
            "min_child_samples": int,
            "max_depth": int,
            "num_iterations": int,
        },
    }
]


def train_model(
    instance: BaseEstimator,
    training_set: Tuple[np.ndarray, np.ndarray],
    params: Dict = {},
) -> BaseEstimator:
    """
    Trains a new instance of model with supplied training set and hyper-parameters.
    """
    override_schemas = list(filter(lambda x: x["class"] == instance, MODELS))[0][
        "override_schemas"
    ]
    for p in params:
        if p in override_schemas:
            params[p] = override_schemas[p](params[p])
    model = instance(**params)
    model.fit(*training_set)
    return model


def optimize_hyp(
    instance: BaseEstimator,
    dataset: Tuple[np.ndarray, np.ndarray],
    search_space: Dict,
    metric: Callable[[Any, Any], float],
    max_evals: int = 40,
) -> BaseEstimator:
    """
    Trains model's instances on hyper-parameters search space and returns most accurate
    hyper-parameters based on eval set.
    """
    X, y = dataset

    def objective(params):
        rep_kfold = RepeatedKFold(n_splits=4, n_repeats=1)
        scores_test = []
        for train_I, test_I in rep_kfold.split(X):
            X_fold_train = X.iloc[train_I, :]
            y_fold_train = y.iloc[train_I].values.flatten()
            X_fold_test = X.iloc[test_I, :]
            y_fold_test = y.iloc[test_I].values.flatten()
            # On entraîne une instance du modèle avec les paramètres params
            model = train_model(
                instance=instance,
                training_set=(X_fold_train, y_fold_train),
                params=params,
            )
            # On calcule le score du modèle sur le test
            scores_test.append(metric(y_fold_test, model.predict(X_fold_test)))

        return np.mean(scores_test)

    return fmin(fn=objective, space=search_space, algo=tpe.suggest, max_evals=max_evals)


def save_pr_curve(X, y, model):
    plt.figure(figsize=(16, 11))
    prec, recall, _ = precision_recall_curve(
        y, model.predict_proba(X)[:, 1], pos_label=1
    )
    pr_display = PrecisionRecallDisplay(precision=prec, recall=recall)
    pr_display.plot(ax=plt.gca())
    plt.title("PR Curve", fontsize=16)
    plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(1, 0))
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1, 0))
    plt.savefig(os.path.expanduser("data/08_reporting/pr_curve.png"))
    plt.close()


def auto_ml(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    max_evals: int = 40,
    log_to_mlflow: bool = False,
    experiment_id: int = -1,
) -> BaseEstimator:
    """
    Runs training of multiple model instances and select the most accurated based on objective function.
    """
    X = pd.concat((X_train, X_test))
    y = pd.concat((y_train, y_test))

    run_id = ""

    if log_to_mlflow:
        mlflow.set_tracking_uri(os.getenv("MLFLOW_SERVER"))
        run = mlflow.start_run(experiment_id=experiment_id)
        run_id = run.info.run_id

    opt_models = []
    for model_specs in MODELS:
        # Finding best hyper-parameters with bayesian optimization
        optimum_params = optimize_hyp(
            model_specs["class"],
            dataset=(X, y),
            search_space=model_specs["params"],
            metric=lambda x, y: -f1_score(x, y),
            max_evals=max_evals,
        )
        print("done")
        # Training the supposed best model with found hyper-parameters
        model = train_model(
            model_specs["class"],
            training_set=(X_train, y_train),
            params=optimum_params,
        )
        opt_models.append(
            {
                "model": model,
                "name": model_specs["name"],
                "params": optimum_params,
                "score": f1_score(y_test, model.predict(X_test)),
            }
        )

    # In case we have multiple models
    best_model = max(opt_models, key=lambda x: x["score"])

    if log_to_mlflow:
        model_metrics = {"f1": best_model["score"]}
        signature = infer_signature(X_train, best_model["model"].predict(X_train))
        save_pr_curve(X_test, y_test, best_model["model"])

        mlflow.log_metrics(model_metrics)
        mlflow.log_params(best_model["params"])
        # Only use if validation curves are produced
        mlflow.log_artifacts("data/08_reporting", artifact_path="plots")
        mlflow.sklearn.log_model(best_model["model"], "model", signature=signature)

        mlflow.end_run()

    return dict(model=best_model, mlflow_run_id=run_id)
