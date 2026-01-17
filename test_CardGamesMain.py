import pytest
from CardGamesMain import CardGamesRunner


class TestCardGamesRunner:
    """
    Test functionality of CardGamesRunner class
    """

    def test_reset_game_selection(self):
        """
        Test _reset_game_selection method of CardGamesRunner.
        """

        runner = CardGamesRunner()
        runner._game_title = "dummy"
        runner._game_runner = "dummy"

        runner._reset_game_selection()
        assert runner._game_title == None
        assert runner._game_runner == None

    def test_run_game_selection(self, monkeypatch):
        """
        Test _run_game_selection method of CardGamesRunner
        """
        runner = CardGamesRunner()

        # override built-in input function to return test input
        user_inputs = iter(["-1", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

        runner._run_game_selection()
        assert runner._game_title == runner._game_options[0][0]
        assert isinstance(runner._game_runner, runner._game_options[0][1])

    def test_set_game_selection_invalid(self):
        """
        Test _set_game_selection method of CardGamesRunner when invalid game index is inputted
        """
        runner = CardGamesRunner()

        # game index is too small
        runner._set_game_selection(-1)
        assert runner._game_title == None
        assert runner._game_runner == None
        # game index is greater than last game option
        runner._set_game_selection(len(runner._game_options))
        assert runner._game_title == None
        assert runner._game_runner == None

    def test_set_game_selection_valid(self):
        """
        Test _set_game_selection method of CardGamesRunner when valid game index is inputted
        """
        runner = CardGamesRunner()

        # game index is too small
        runner._set_game_selection(0)
        assert runner._game_title == runner._game_options[0][0]
        assert isinstance(runner._game_runner, runner._game_options[0][1])

    def test_run_game_action_no_game_select(self):
        """
        Test _run_game_action method of CardGamesRunner when no game has been selected yet
        """
        runner = CardGamesRunner()
        with pytest.raises(AttributeError):
            runner._run_game_action()

    def test_run_game_action_game_selected(self, monkeypatch):
        """
        Test _run_game_action method of CardGamesRunner when game has been selected
        """
        runner = CardGamesRunner()
        # Select game
        runner._game_title = runner._game_options[0][0]
        runner._game_runner = runner._game_options[0][1]()
        # override built-in input function to return test input
        user_inputs = iter(["-1", "4"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
        # Run method and ensure that quit action is successful (i.e., this test does not get stuck in infinite loop)
        runner._run_game_action()

    def test_run_card_game(self, monkeypatch):
        """
        Provide test coverage of run_card_game method of CardGamesRunner
        """
        runner = CardGamesRunner()

        # override built-in input function to return test input
        user_inputs = iter(["1", "4", str(len(runner._game_options) + 1)])
        monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

        runner.run_card_games()
