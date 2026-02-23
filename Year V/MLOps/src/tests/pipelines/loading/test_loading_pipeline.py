from kedro.runner import SequentialRunner
import pandas as pd

from purchase_predict.pipelines.loading.pipeline import create_pipeline


def test_pipeline(catalog_test):
    runner = SequentialRunner()
    pipeline = create_pipeline()
    pipeline_output = runner.run(pipeline, catalog_test)
    df = pipeline_output["primary"]
    assert type(df) == pd.DataFrame
    assert df.shape[1] == 16
    assert "purchased" in df
