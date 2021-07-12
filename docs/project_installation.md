# Project Installation

Solution is Python based with combination of standalone software components. Therefore, there are two ways of
installation. Installation for end user and installation for development purposes. Everything is packed inside Docker
images for end user to maximally ease usage. Installation is more complicated for development purposes, but depends on
the development tools too.

## End User Installation

### Docker Compose Installation
[comment]: <> (TODO)

## Development Installation

There are two ways of dev installations, depending on development tools setup:

- Option 1: Using Docker Compose Python interpreter.
- Option 2: Using bare metal.

### Option 1: Docker Compose Python interpreter

This option assumes that developer's Python IDE is capable of using Docker Compose based Python interpreter
(e.g. JetBrains PyCharm Professional IDE supports this option).

1. Install Docker ([how to install](https://docs.docker.com/get-docker/)).
2. Install Docker Compose ([how to install](https://docs.docker.com/compose/install/)).

### Option 2: Using Bare Metal

This approach gives user a freedom to use any Python IDE, but requires to install a bundle of software components.
Follow the general steps to install the solution or even more, go command by command using
> ##### :bulb: Reference Installation Steps :point_down:
section of each step.

1. Download the repository using `git clone https://github.com/OndrejSzekely/metron.git`.

2. To encapsulate solution's installation (Python frameworks and other software components), it recommended to use
   virtual environment. Create Python **3.8** virtual environment using Python dependency management tool you are
   using (e.g. Conda, Pipenv, etc...).

   ##### :bulb: Reference Installation Steps :point_down:
   It is recommended to use Anaconda channel ([how to get Anaconda](https://www.anaconda.com/products/individual)),
   which also provides installation management of non-Python software components, and Python 3.8.8. Run following
   command to create a new virtual environment:
   ```shell
   conda create -n metron python=3.8.8
   ```
   Run following command to attach created virtual environment in which all further steps are executed:
   ```shell
   conda activate metron
   ```

3. Install dev tools for commits validation: *Black*, *Pylint*, *Flake8*, *MyPy* and *Bandit*.
   
   When manual installation is used, use following config files which modifies default setting of the tools:
   - `pyproject.toml`: Customized Black settings and customized Pylint settings.
   - `.flake8`: Customized Flake8 setting.
   
   The alternative option is using *pre-commit* tool. This tools uses Git Hooks to run automatically all 
   the tools before commit making. The configuration of *pre-commit* (including tool configurations) is located in 
   *.pre-commit-config.yaml*. There is no need of tools manual installation using this option. To understand how 
   work with *pre-commit*, take a look into [docs](https://pre-commit.com/#usage).
   
   ##### :bulb: Reference Installation Steps :point_down:
   Go into the project's root folder and run following command attached Conda environment to install *pre-commit*:
   ```shell
   conda install -c conda-forge pre-commit
   ```
   Then install *pre-commit* configuration using:
   ```shell
   pre-commit install
   ```

4. Install Poetry ([how to install](https://python-poetry.org/docs/#installation)), which is a Python dependency
   management tool and Metron uses Poetry to track all Python dependencies.

   ##### :bulb: Reference Installation Steps :point_down:
   Run in attached Conda environment:
   ```shell
   conda install -c conda-forge poetry
   ```

5. Install FFmpeg **4.3.1** ([how to install](https://ffmpeg.org/download.html)).

   ##### :bulb: Reference Installation Steps :point_down:
   Run in attached Conda environment:
   ```shell
   conda install -c conda-forge ffmpeg=4.3.1
   ```

6. Install Poetry Python dependencies, including dev ones.

   ##### :bulb: Reference Installation Steps :point_down:
   Run in attached Conda environment in project's root folder:
   ```shell
   poetry install
   ```

7. Add Metron's root folder path **permanently** into `PYTHONPATH` environmental variable.

   ##### :bulb: Reference Installation Steps :point_down:
   In the attached Conda environment go to the Metron's root folder, **copy all** following commands **at once**, paste
   them into terminal and execute:
   ```shell
   mkdir -p "${CONDA_PREFIX}/etc/conda/activate.d" && \
   mkdir -p "${CONDA_PREFIX}/etc/conda/deactivate.d" && \
   touch "${CONDA_PREFIX}/etc/conda/activate.d/env_vars.sh" && \
   touch "${CONDA_PREFIX}/etc/conda/deactivate.d/env_vars.sh" && \
   echo -e "#"'!'"/bin/sh\n" >> "${CONDA_PREFIX}/etc/conda/activate.d/env_vars.sh" && \
   echo -e "#"'!'"/bin/sh\n" >> "${CONDA_PREFIX}/etc/conda/deactivate.d/env_vars.sh" && \
   echo -e "export PYTHONPATH=$(pwd):\n" >> "${CONDA_PREFIX}/etc/conda/activate.d/env_vars.sh" && \
   echo -e "unset PYTHONPATH\n" >> "${CONDA_PREFIX}/etc/conda/deactivate.d/env_vars.sh"
   ```

8. Spawn Poetry shell. It will create a new Poetry virtual environment, if one does not exist and attach it.

   > ##### :clipboard: Remark :raised_hand:
   > If the virtual environment was created in the first step of the guide, then we have now running virtual
   > environment within virtual environment. This might sound odd, but it has two benefits.
   >
   > In some steps we need to install additional software, not only Python packages. Therefore, it is a good practice
   > to separate these software installations from bare metal. This allows to prevent software conflicts
   > (e.g. compatibility, versions, prerequisites) and solution's easy uninstallation or updates.
   >
   > The second reason is when Poetry uses the hosting virtual environment, which is provided by different Python
   > management tool, it can cause inconsistencies between two Python package management tools and break Metron.
   >
   > In case it is desired to use only hosting virtual environment, Poetry allows disabling creation of its own
   > environment. To make it work within virtual environment, use `poetry config` to disable the creation of virtual
   > env and customize `virtualenvs.path` to point into the directory of the hosting virtual environment.

   ##### :bulb: Reference Installation Steps :point_down:
   In the attached Conda environment execute:
   ```shell
   poetry shell
   ```
   This creates a new virtual environment managed by Poetry. If you want to *force Poetry to use Conda's virtual
   environment*, **which is not recommended**, then you have to run following commands:
   ```shell
   poetry config virtualenvs.path ${CONDA_PREFIX}
   poetry config virtualenvs.create false
   ```

9. Everything is now up and ready to run Metron's components. Be aware that you can run only one component at the time
   in one session. To run all Metron's components, you have to open several terminal sessions, one per Metron's
   component and attach the virtual environment created in the step 1 (if performed) and attach Poetry's virtual
   environment created in the step 6 (if performed).

   GOOD JOB! :raised_hands: :rocket: :dizzy:

   ##### :bulb: Reference Installation Steps :point_down:
   **You have to close the terminal session after the installation.**
   
   To run Metron's component in a new terminal session, run following commands in **Metron's root directory** to 
   activate the environments:
   ```shell
   conda activate metron
   source "$( poetry env list --full-path )/bin/activate"
   ```
   Then run the execution command for given component.
   
   To deactivate Poetry's and Conda's virtual environment run following commands:
   ```shell
   deactivate
   conda deactivate
   ```