# Seaplane
Seaplane was created as a minimal tool to get a local kubernetes development environment off the ground. It is 
purposefully simple and limited to local development.

Under the hood, seaplane is just calling Docker, Helm, and Minikube. You're not bound to any proprietary file formats 
or tools.

## Installation
Seaplane requires Python 3. To install simply run:

```bash
pip install --user seaplane
```

## Commands
### `seaplane init`
Check for all required packages. If any packages need to be installed, it will direct you
towards an installation link. It will then generate the basic directory structure seaplane expects. 

The `--recommended` flag will also search for any recommended, but non-essential packages.

The `--example` flag will copy the example files to your current project. This can be useful if you want to get an idea
of what a very basic deployment looks like.

### `seaplane start`
Starts minikube and helm then install the nginx ingress controller and the development deployment in the minikube 
cluster. 

### `seaplane stop`
Stops the development cluster. The `--all` flag will stop the nginx ingress controller and the minikube cluster.

### `seaplane shell LABEL`
Opens a shell in the first pod in your deployment with label `seaplane-label=LABEL`. 

The default shell executable, `/bin/bash`, can be overridden with the `--executable` argument.

The namespace can be overridden with the `--namespace` argument. Defaults to the configuration value.

### `seaplane logs LABEL`
Shows streaming logs for the first pod in your deployment with label `seaplane-label=LABEL`. 

The namespace can be overridden with the `--namespace` argument. Defaults to the configuration value.

**NOTE**: If stern is installed, it will show logs for all pods in your deployment with label `seaplane-label=LABEL`.

## Configuration
Default configuration values can be overridden with a `seaplane.json` file in your projects root directory. Here's the 
the defaults in `seaplane.json` form.

```json
{
  "development_directory": "development",
  "docker_directory": "docker",
  "charts_directory": "charts",
  "development_chart": "development",
  "namespace": "example-ns",
  "project_name": "example",
  "project_hostname": "example.test",
  "port_range": "80-8080"
}

```

Changes may require you manually update your directory structure to match for seaplane to work.
