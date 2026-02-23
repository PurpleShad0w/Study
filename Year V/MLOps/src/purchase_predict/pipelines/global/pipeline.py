from kedro.pipeline import Pipeline
from typing import Dict

from loading import pipeline as loading_pipeline
from loading import pipeline as processing_pipeline
from training import pipeline as training_pipeline


def register_pipelines(self) -> Dict[str, Pipeline]:
    """Register the project's pipeline.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    p_processing = processing_pipeline.create_pipeline()
    p_training = training_pipeline.create_pipeline()
    p_loading = loading_pipeline.create_pipeline()

    return {
        "global": Pipeline([p_loading, p_processing, p_training]),
        "loading": p_loading,
        "processing": p_processing,
        "training": p_training,
    }
