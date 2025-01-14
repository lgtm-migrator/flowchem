import nox

nox.options.stop_on_first_error = True


@nox.session(python=["3.9"])
def black(session):
    session.install("black")
    session.run("black", "flowchem", "--check")


@nox.session(python=["3.9", "3.10"])
def lint(session):
    session.install("flake8")
    session.run(
        "flake8",
        "flowchem",
        "--count",
        "--select=E9,F63,F7,F82",
        "--show-source",
        "--statistics",
    )


@nox.session(python=["3.9", "3.10"])
def type_check(session):
    session.install("mypy")
    session.run("mypy", "--install-types", "--non-interactive", "flowchem")


@nox.session(python=["3.9", "3.10"])
def tests(session):
    session.install(".[test]")
    session.run("pytest")
