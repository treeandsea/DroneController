# Contributing to Drone Controller

First off all, thank you very much for taking interest in contributing to our project. We value your time and effort.

The following guideline shall help to create a save and efficient environment to develop open source software.

## Questions

We try to document as much as possible but sometimes things are missed. 
If you have any question which is not answered with our resources, please contact us on [slack](https://app.slack.com/client/TSFE416AW/C0101ADT90D).
Don't use the issue. The are reserved for bugs and/or feature discussion.

## What should I know before I get started?

Although Drone Controller is simple project for now, we decided to define an [architecture and an interface](https://treeandsea.github.io/DroneController/) right from the beginning.
Both will be updated during development. So please read them.

## How can I contribute?

### Reporting Bugs

Before reporting a bug, please check our [bug board](https://github.com/treeandsea/DroneController/projects/2).

We track our bugs with [Github Issues](https://guides.github.com/features/issues/).
Also please use our [template](https://github.com/treeandsea/DroneController/blob/community/.github/ISSUE_TEMPLATE/bug_report.md).

Be as descriptive as you can and use a precise title. In addition to that, label it at least with `bug` but also with other matching tags.
This helps enormously on finding bugs for other users.

### Suggesting Enhancements

If you have an idea to improve `DroneController` you should read this section carefully. First of we are open minded to add feature to our project.

First check the [issues](https://github.com/treeandsea/DroneController/issues) if someone made a similar suggestion.
Then it would be best to comment on that one.

If this is not related to an existing suggestion then please use our [feature suggestion template](https://github.com/treeandsea/DroneController/blob/community/.github/ISSUE_TEMPLATE/feature_request.md).

### First Timers

If you are new or do not have that much experience with our technologies used, we still want you to contribute. Therefor we label easy tasks with [good first issue](https://github.com/treeandsea/DroneController/labels/good%20first%20issue). 
On the other hand if you are experienced please leave this issues for those not that experience but tackle one of our [help wanted](https://github.com/treeandsea/DroneController/labels/help%20wanted).

### Workflow

We use the following git workflow.

- **Fork** First fork the project to your own namespace.
- **Local development** Work on an issue in your namespace until you think it is done.
    - **Code Style** Use [PEP8](https://www.python.org/dev/peps/pep-0008/) so the project is easier to read.
    - **Doc String** Write documentation for all you do. This is very important to understand code. Here is a [tutorial](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).
    - **Test** Write tests. This should at least include unit test and if necessary integration tests.
- **Checks** Run our checks to reduce frustration. This include running all tests to prevent regression. We use `pylint` for checks. You can find the configuration file `.pylintrc` in the root directory.
The github actions will check on `src` and `test` with:
```console
pylint --rcfile=.pylintrc -j 2 src test 
```

- **Pull Request** 
    - **Base** Create a pull request to the [develop](https://github.com/treeandsea/DroneController/tree/develop) branches unless it is a `hotfix` or documentation then choose [master](https://github.com/treeandsea/DroneController/tree/master) as base.
        - **Feature** Our project has feature branches for new features. If you want to make an addition to a specific feature, then choose this branch as base, but make sure to contact the author before start coding so two people won't work one same stuff.
    - **Description** Be as descriptive as you can. This should include what you may have fixed or what your feature is. Also describe what you might
    not have done, because it would be too much or a PR own it's own. It that case open another issue.
    - **Labels** Use labels to tag your PR so it is easier to find. Use [bug](https://github.com/treeandsea/DroneController/labels/bug) for bug fixes, [enhancement](https://github.com/treeandsea/DroneController/labels/enhancement) for features and [documentation](https://github.com/treeandsea/DroneController/labels/documentation) for documentation :wink:.
