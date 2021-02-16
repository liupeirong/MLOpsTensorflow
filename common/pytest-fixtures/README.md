# Overview

This folder contains pytest-fixture templates for reuse in new MLOps projects.

* [Fixture for mocking AML SDK](##Fixture-for-mocking-AML-SDK)
* [Fixture for mocking AML SDK with Env util](##Fixture-for-mocking-AML-SDK-with-Env-util)

## Fixture for mocking AML SDK

> [This fixture](./test_aml_mock_fixtures_default.py) is **independent** from other utils and tools used in
[samples](/samples) of this repo.

If you are referencing environment variables directly instead of using util, please import this [test_aml_mock_fixtures_default.py](./test_aml_mock_fixtures_default.py) file under your test directory.

Sets mocks for AML SDK related to AML Pipeline build scripts:

* Workspace.Get
* PythonScriptStep
* Pipeline
* Pipeline.publish
* ComputeTarget (AmlCompute only)
* Environment

### How to use
1. Import predefined fixture to your test method
    ```
    from test_aml_mock_fixtures_env import environment_vars, aml_pipeline_mocks
    ```
    > Note: Depending on the location you are referencing 'test_aml_mock_fixtures_env', the path may need to be different.

2. Pass 'aml_pipeline_mocks' as parameter to your unit test method
    ```
    [Example]
    def test_build_data_processing_os_cmd_pipeline(aml_pipeline_mocks):
    ```

3. Load mocks from fixture using tuple 
    ```
    (workspace, aml_compute, mock_workspace_get, mock_pipeline_publish) =\
    aml_pipeline_mocks
    ```
    
4. [Optional] Use "spy" to write tests in more detail

    ```
    [Example]
    # Create a spy
    spy_pythonscriptstep_create =\
        mocker.patch('azureml.pipeline.steps.PythonScriptStep',wraps=PythonScriptStep)

    # Check if PythonScriptStep instantiation was called correctly
    spy_pythonscriptstep_create.\
        assert_called_once_with(allow_reuse=False,
                                runconfig=ANY,
                                arguments=ANY,
                                source_directory=e.sources_directory_train,
                                script_name="preprocess/"
                                            "preprocess_os_cmd_aml.py",
                                name="Preprocess Data with OS cmd",
                                compute_target=ANY)
    ```

The full unit test code can be found at [test_build_data_processing_os_cmd_pipeline.py](/samples/non-python-preprocess/ml_service/tests/pipelines/test_build_data_processing_os_cmd_pipeline.py).

## Fixture for mocking AML SDK with Env util

> [This fixture](./test_aml_mock_fixtures_env.py) is **dependent on the ml_service.util.env_variables.Env class**
used in [non-python-preprocess sample](/samples/non-python-preprocess/ml_service/util/env_variables.py).

If you are referencing your environment variables through dotenv module, please import this [test_aml_mock_fixtures_env.py](./test_aml_mock_fixtures_env.py) file under your test directory.

Sets mocks for AML SDK related to AML Pipeline build scripts:

* Workspace.Get
* PythonScriptStep
* Pipeline
* Pipeline.publish
* ComputeTarget (AmlCompute only)
* Environment

### How to use

TODO