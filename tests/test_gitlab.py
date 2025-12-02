import subprocess
import pytest
from functools import wraps
from utils import (
    databricks_cli,
    generated_project_dir,
    parametrize_by_cloud,
    parameterize_by_cicd_params,
)


@parameterize_by_cicd_params(["gitlab"])
@parametrize_by_cloud
def test_generated_gitlab_folder(
    project_type, cloud, include_models_in_unity_catalog, generated_project_dir
):
    if cloud == "gcp" and include_models_in_unity_catalog == "yes":
        # Skip test for GCP with Unity Catalog
        return

    # TEST: Check if gitlab folder has been created.
    project_dir = f"my-{project_type}-project"
    subprocess.run(
        """
        ls ./.gitlab/pipelines
        """,
        shell=True,
        check=True,
        executable="/bin/bash",
        cwd=(generated_project_dir / project_dir),
    )
    # TODO Check syntax with: gitlab-ci-local --file ./.gitlab/cicd.yml
    # (NOTE: syntax check requires gitlab-ci-local installed on VM)
