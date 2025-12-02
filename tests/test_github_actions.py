import subprocess
import pytest
from functools import wraps
from utils import (
    databricks_cli,
    generated_project_dir,
    parametrize_by_cloud,
    parameterize_by_cicd_params,
)


@parameterize_by_cicd_params(["github_actions", "github_actions_for_github_enterprise_servers"])
@parametrize_by_cloud
def test_generated_yaml_format(
    project_type, cloud, include_models_in_unity_catalog, generated_project_dir
):
    # Note: actionlint only works when the directory is a git project. Thus we begin by initiatilizing
    # the generated project with git.
    if cloud == "gcp" and include_models_in_unity_catalog == "yes":
        # Skip test for GCP with Unity Catalog
        return
    project_dir = f"my-{project_type}-project"
    subprocess.run(
        """
        git init
        bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
        ./actionlint -color
        """,
        shell=True,
        check=True,
        executable="/bin/bash",
        cwd=(generated_project_dir / project_dir),
    )


@pytest.mark.large
@parameterize_by_cicd_params(["github_actions", "github_actions_for_github_enterprise_servers"])
@parametrize_by_cloud
def test_run_unit_tests_workflow(
    project_type, cloud, include_models_in_unity_catalog, generated_project_dir
):
    """Test that the GitHub workflow for running unit tests in the materialized project passes"""
    if cloud == "gcp" and include_models_in_unity_catalog == "yes":
        # Skip test for GCP with Unity Catalog
        return
    # We only test the unit test workflow, as it's the only one that doesn't require
    # Databricks REST API
    project_dir = f"my-{project_type}-project"
    subprocess.run(
        f"""
        git init
        act -s GITHUB_TOKEN workflow_dispatch --workflows .github/workflows/{project_dir}-run-tests.yml -j "unit_tests"
        """,
        shell=True,
        check=True,
        executable="/bin/bash",
        cwd=(generated_project_dir / project_dir),
    )
