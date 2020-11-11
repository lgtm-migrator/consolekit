# 3rd party
import click
from click import echo
from domdf_python_tools.stringlist import StringList
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from consolekit.input import choice, confirm, prompt


def test_choice_letters(capsys, monkeypatch, data_regression: DataRegressionFixture):

	inputs = iter(["F", "G", "D"])

	def fake_input(prompt):
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	echo("Configuration file '/etc/sudoers'")
	echo("==> Modified (by you or by a script) since installation.")
	echo("==> Package distributor has shipped an updated version.")
	echo("What would you like to do about it ?  Your options are:")
	options = {
			"Y": "install the package maintainer's version",
			"N": "keep your currently-installed version",
			"D": "show the differences between the versions",
			"Z": "start a shell to examine the situation"
			}
	assert choice(text="*** sudoers", options=options, default="N") == "D"

	data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


def test_choice_numbers(capsys, monkeypatch, data_regression: DataRegressionFixture):

	inputs = iter(["20", "0", "5"])

	def fake_input(prompt):
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	echo("What is the Development Status of this project?")
	options = [
			"Planning",
			"Pre-Alpha",
			"Alpha",
			"Beta",
			"Production/Stable",
			"Mature",
			"Inactive",
			]
	assert choice(text="", options=options, start_index=1) == 4

	data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


def test_confirm(capsys, monkeypatch, data_regression: DataRegressionFixture):

	inputs = iter(["Y", "N", "", ""])

	def fake_input(prompt):
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is True
	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is False
	assert confirm(text="Do you wish to delete all files in '/' ?", default=False) is False
	assert confirm(text="Do you wish to delete all files in '/' ?", default=True) is True

	data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))


def test_prompt(capsys, monkeypatch, data_regression: DataRegressionFixture):

	inputs = iter(["", "", "", "", "24", "Bond007", "badpassword", "baspassword", "badpassword", "badpassword"])

	def fake_input(prompt):
		value = next(inputs)
		print(f"{prompt}{value}".rstrip())
		return value

	monkeypatch.setattr(click.termui, "visible_prompt_func", fake_input)

	assert prompt(text="What is your age", prompt_suffix="? ", type=click.INT) == 24

	assert prompt(text="Username", type=click.STRING) == "Bond007"
	assert prompt(text="Password", type=click.STRING, confirmation_prompt=True) == "badpassword"

	data_regression.check(list(StringList(capsys.readouterr().out.splitlines())))
