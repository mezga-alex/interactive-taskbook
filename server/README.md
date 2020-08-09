# yogi-backend

![build state](https://github.com/meetyogi/yogi-backend/workflows/api-dev-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/api-staging-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/api-prod-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/clustering-service-dev-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/clustering-service-staging-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/clustering-service-prod-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/ingestion-service-dev-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/ingestion-service-staging-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/ingestion-service-prod-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/network-service-dev-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/network-service-staging-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/network-service-prod-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/nlp-service-prod-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/nlp-service-dev-build/badge.svg)

![build state](https://github.com/meetyogi/yogi-backend/workflows/code-quality/badge.svg)

## Prerequisite CLI Tools:
1. [pyenv](https://github.com/pyenv/pyenv) (manage multiple versions of python and types of python)
2. [pipenv](https://github.com/pypa/pipenv) (like package.json and package-lock.json for python)

## Local Repo Setup
1. `pyenv install 3.7.0` (decided to go with 3.7 so we can one day use pypy3.7 which should come out soon - pypy is much faster then cpython)
2. From the top of the repo where the global Pipfile resides, run `pipenv --python /Users/yourusername/.pyenv/versions/3.7.0/bin/python3.7`. Manually set the correct python version under `[requires]` in the Pipfile (i.e. "3.7").
3. For services that don't have a Pipfile, navigate to each where their Pipfile should reside, and run `export PIPENV_NO_INHERIT=true`, and repeat #2 command for each.
4. To use a service's virtual environment in a shell, run `pipenv shell` at the level of its Pipfile.
5. `pipenv install --dev` only at the root Pipfile to install packages to the virtual environment needed for running code quality checks (`tox`) and tests.
6. `FURY_AUTH=your-auth-token-from-gemfury pipenv install` at each service's Pipfile. The services only have prod packages (hence no `--dev` install flag), and the `FURY_AUTH` token is used to pull private packages hosted on Gemfury (e.g. `common-lib`).

## Running Services Locally
Due to multiple services, libs, and multi-staged Docker builds, it's best to build a Docker image of a service and run the container.

### Environment Variables
There are a few environment variables that need to be set first. Create a `localtesting.sh` file that contains the following:

```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export FURY_AUTH=
# export GEMFURY_PUSH_TOKEN=
export DB_NAME=
export DB_USER=
export DB_PASSWORD=
export DB_HOST=# "host.docker.internal" (when running docker containers on macOS) OR "localhost" (when running from the python interpreter)
export DB_PORT=5432
```
```
chmod +x localtesting.sh
source localtesting.sh
./localtesting.sh
then test by running:
echo $FURY_AUTH
```
The AWS credentials come from a dev tester user account (ask admin) that allows locally running services to have the same permissions as the cloud dev environment. Enter the connection information for your local PostgreSQL database.

You can also just set these variables in your zsh or bash startup and then change them per shell when needed. [Here is how.](https://apple.stackexchange.com/questions/356441/how-to-add-permanent-environment-variable-in-zsh)

NOTE: on our deployed environments, the only environment varibale that is needed is: ENV=dev,staging, or prod. This should NOT be used locally as it will attempt to set the incorrect things in settings.py of common_lib. The tox environment when running locally will actually have use the dev database. However no actual calls will be made to the database. See tox.ini for details.

### Database Setup
1. Create a local database server in your database management tool (e.g. pgAdmin)
2. In the python interpreter, run `common_lib.crud._create_tables()` to create database tables based on the models found in common-lib.
3. Import seed data into the database (ask admin)

Alternatively you could take a pgdump and restore the file. This is the fastest way to get started. Ask admin or check google drive for these files. We will have a dump per common-lib/models schema version.

### Image Building
Use the `build.sh` script in each service's scripts directory to build a local image. They take one parameter--the image tag (e.g. `v1.0.0`). Below are the basic commands the script runs.
1. `pipenv lock -r > requirements.txt`
2. `docker build --build-arg FURY_AUTH=${FURY_AUTH} -t <service_name>:v<version_number> .`

### Running a Container
The template command to run any service is as follows.
1. `docker run -t -p 80:80 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -e DB_NAME=$DB_NAME -e DB_HOST=$DB_HOST -e DB_PORT=$DB_PORT -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -e MAX_WORKERS=1 -e GRACEFUL_TIMEOUT=3 <service_name>:v<version_number>`
The choice of host port doesn't matter when running a single service locally, but some services expect others to listen on ports other than port 80 when running locally (services may make requests to others). Refer to the services' `settings.py` files for the expected ports.


### Example
1. `source /path/to/localtesting.sh`
2. `cd api`
3. (optional) `pipenv install`
4. `sh scripts/build.sh`
5. `docker run -t -p 80:80 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -e DB_NAME=$DB_NAME -e DB_HOST=$DB_HOST -e DB_PORT=$DB_PORT -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -e MAX_WORKERS=1 -e GRACEFUL_TIMEOUT=3 api:v1.0.0`

### Running a service (without container)
For reference, this is how you would run the api service locally if the docker build wasn't needed.
#### Running the API 
You would want to do this if you are making changes to common-lib and want to see them immediately without publishing a test lib to the package repoistroy (currently gemfurry).
Make sure you are in the root dir (/backend/). The same can be done for any fastapi services.
1. `pipenv shell`
2. `uvicorn api.main:app --reload`

#### Making changes to common-lib and observing them locally without publishing a package
Simply take a Pipfile where perviouly `common-lib = {version = "==1.0.1",index = "fury"}` to `common-lib = { editable = true, path = "/Users/yourname/yogi/common_lib" }` (basically point to your local common-lib folder). You might need to pipenv uninstall and reinstall in order for it to work. Then run the uvicorn server and you should see the changes locally. If you make a change to the app (backend) then those changes you should see automatically. If you make a change to common-lib you will need to restart the server manually to see the changes. Test if it is working by adding a print() to any endpoint you are testing.

## Git Commits and PRs
1. Switch to `dev` branch.
2. Branch off of `dev` with the naming convention `dev-<ticket identifier>-<name of feature>` and switch to the branch. Example: `dev-yp-001-migrating`. The "yp" references the Yogi Product backlog, and "eng" references the Engineering backlog.
3. Before you commit: `pipenv tox` or just `tox` if you are in the virtual env shell. Code quality and tests will run.
4. Then commit, and you should see the pre-commit run if you have followed the instructions and installed pre-commit hooks.
5. On GitHub, open a PR for `dev-<ticket identifier>-<name of feature>` to `dev`
6. View GitHub Actions fire off. Should be success or fail. Add reviewer. Get feedback. Push again to fix failing CI (look at the "Actions" tab and find your commit/branch) or any PR changes. Then merge and close branch.

## Unit tests
UNIT TESTING is a level of software testing where individual units/ components of a software are tested. Therefore when new code is rewritten tests should be written with it: happy path, alernative paths, and any exceptions. No network or db calls should actually occur rather they should be mocked:
[https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)
[https://docs.python.org/3/library/unittest.mock.html?highlight=mock#module-unittest.mock](https://docs.python.org/3/library/unittest.mock.html?highlight=mock#module-unittest.mock)
[https://docs.python.org/3/library/unittest.mock.html?highlight=magicmock#unittest.mock.MagicMock](https://docs.python.org/3/library/unittest.mock.html?highlight=magicmock#unittest.mock.MagicMock)
[https://docs.python-guide.org/writing/tests/](https://docs.python-guide.org/writing/tests/)

See ingestion service unit tests for good examples.

## Repo tooling
The following tools have been installed:
1. [flake8](https://medium.com/python-pandemonium/what-is-flake8-and-why-we-should-use-it-b89bd78073f2) - linting tool for writing clean code
2. [flake8-docstrings](https://gitlab.com/pycqa/flake8-docstrings) - enforces doc strings
3. [flake8-import-order](https://github.com/PyCQA/flake8-import-order) - enforces import order
4. [black](https://black.readthedocs.io/en/stable/) - auto code formatter
5. [mypy](http://mypy-lang.org/) - enforces static type checking/ type hinting for Python
4. [pre-commit](https://pre-commit.com/) - runs scripts/tools before commiting anything
6. [tox](https://tox.readthedocs.io/en/latest/) -  used to automate running the liniting, type checking, and running pytest. Will be used in CI.
8. [pytest](https://docs.pytest.org/en/latest/) - testing framework

## TODO:

Tests:
- Fixutures, unit, intergration,
- Add security tool bandit
- Add codecoverage
- common-lib versions syncd on all projects tooling
