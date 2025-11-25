# Clu Airflow DAGs

Collection of Airflow DAGs used in the cludus infrastructure to fetch and save data. This repository holds DAG definitions and small helper modules that implement scheduled workflows executed by an Airflow deployment.

## Purpose

This repository's primary goal is to store and version the DAGs (Directed Acyclic Graphs) that define scheduled tasks and data pipelines for the clu ecosystem. The DAGs reference task code and operators that run inside containers (for example, images produced by the `clu-airflow-img` repo) or on the Airflow worker environment.

Use cases:
- Source-controlled Airflow DAGs for production or staging deployments.
- Lightweight examples and templates for new tasks.
- A place to run and validate DAGs locally before deploying to a cluster-based Airflow.

## Repository layout

- `first_dag.py` - example DAG (inspect for task definitions and schedule).
- `second_dag.py` - a second example DAG.
- `__pycache__/` - Python bytecode cache (ignored by VCS normally).
- `README.md` - this document.

If you add more DAG files, keep them at the repository root or in a `dags/` subfolder (Airflow will pick them up if your `airflow.cfg` or deployment mounts that path as the DAGs folder).

## How the DAGs work

- Each DAG file defines a DAG object and one or more tasks using Airflow operators (PythonOperator, BashOperator, KubernetesPodOperator, etc.).
- Tasks can run Python callables, shell commands, or external containers.
- Task code should remain idempotent, small, and easily testable.
- Dependencies required at runtime (third-party Python packages) should be provided by the execution environment image (for example, the `clu-airflow-img` image) or listed in your deployment's requirements manifest.

## Running and testing locally

Option A — Quick local run with `airflow standalone` (Airflow 2.4+):

```bash
# create a venv and install airflow if you don't have it
python -m venv .venv
source .venv/bin/activate
pip install "apache-airflow==2.6.*" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.*/constraints-3.11.txt"

# start a quick, single-node Airflow instance
airflow db init
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
airflow standalone
```

Place this repo's DAG files inside the `AIRFLOW_HOME/dags` folder or update your `airflow.cfg` `dags_folder` to point at this repository path. The Airflow webserver UI will show DAGs and you can trigger runs manually for testing.

Option B — Run tasks using the project image (recommended for parity):

1. Build the image from `clu-airflow-img`:

```bash
docker build -t clu-airflow-img:latest ../clu-airflow-img
```

2. Run an individual task using the image (for example, with `docker run` or a small Kubernetes Pod). Use the image to ensure runtime dependencies are consistent with production.

Note: The repo intentionally does not pin or install dependencies inside each DAG file — runtime packages should be supplied by the container or the Airflow worker environment.

## Testing DAG code

- Keep operator callables small and unit-testable. Put testable logic in separate modules and import them from the DAG file.
- This repository contains simple example DAGs; consider adding `tests/` with pytest tests to validate your callables and small integration behaviors.

Example unit test flow:

```bash
# from the repo root
python -m venv .venv
source .venv/bin/activate
pip install -r ../clu-airflow-img/src/requirements.txt pytest
pytest tests
```

(adapt the paths and requirements to your layout)

## Adding or modifying DAGs

- Add new DAG files (`my_pipeline.py`) to the repo root or `dags/` folder.
- Follow Airflow best practices: small tasks, retries, clear task ids, sensible schedules, and good logging.
- If new Python packages are required, add them to the execution image's `requirements.txt` (for example `clu-airflow-img/src/requirements.txt`) and rebuild that image, or document the dependency for your deployment.

## CI and deployment

This repository is intended to be deployed by copying the DAG files into the DAGs folder used by your Airflow instance, or by mounting this repository as a volume in a Kubernetes deployment. Common deployment strategies:
- Bake DAGs into a custom worker image.
- Mount a Git-backed volume (GitSync) to the Airflow DAGs folder.
- Use CI to sync DAG files to a bucket or directly to the Airflow instance.

If you'd like, I can add a GitHub Actions workflow that lints DAGs and optionally packages them for deployment.

## Contributing

- Open a PR describing the change. Small improvements and bug fixes welcome.
- Follow the repository's coding conventions and keep DAGs readable.
- Include tests for any non-trivial logic.

## Troubleshooting

- If DAGs don't appear in the Airflow UI: ensure the `dags_folder` configured in Airflow points to this repo path and that files have the `.py` extension.
- If tasks fail due to missing imports: verify the execution environment has the required Python packages installed (check the image or worker virtualenv).

## License

Follow the license used across the clu repositories. Add a LICENSE file to this repo if you want a specific license.

