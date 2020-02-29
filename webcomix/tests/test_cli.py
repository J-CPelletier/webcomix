from click.testing import CliRunner
import pytest

from webcomix import cli
from webcomix.comic import Comic
from webcomix.exceptions import CrawlerBlocked, NextLinkNotFound
from webcomix.supported_comics import supported_comics
from webcomix.tests.fake_websites.fixture import (
    three_webpages_uri,
    three_webpages_alt_text_uri,
)

first_comic = list(sorted(supported_comics.keys()))[0]


def test_print_verification(capfd, three_webpages_uri):
    comic = Comic("test", three_webpages_uri, "//img/@src", "//a/@href")
    verification = comic.verify_xpath()
    cli.print_verification(verification)
    out, err = capfd.readouterr()

    three_webpages_folder = three_webpages_uri.strip("1.html")

    assert out == (
        "Page 1:\n"
        "Page URL: " + three_webpages_uri + "\n"
        "Image URLs:\n"
        "" + three_webpages_folder + "1.jpeg"
        "\n"
        "\n"
        "Page 2:\n"
        "Page URL: " + three_webpages_folder + "2.html"
        "\n"
        "Image URLs:\n"
        "" + three_webpages_folder + "2.jpeg"
        "\n"
        "\n"
        "Page 3:\n"
        "Page URL: " + three_webpages_folder + "3.html"
        "\n"
        "Image URLs:\n"
        "\n"
        "\n"
    )


def test_print_verification_with_alt_text(capfd, three_webpages_alt_text_uri):
    comic = Comic(
        "test_alt",
        three_webpages_alt_text_uri,
        "//img/@src",
        "//a/@href",
        "//img/@title",
    )
    verification = comic.verify_xpath()
    cli.print_verification(verification)
    out, err = capfd.readouterr()

    three_webpages_alt_text_folder = three_webpages_alt_text_uri.strip("1.html")

    assert out == (
        "Page 1:\n"
        "Page URL: " + three_webpages_alt_text_uri + "\n"
        "Image URLs:\n"
        "" + three_webpages_alt_text_folder + "1.jpeg"
        "\n"
        "Alt text: First page\n"
        "\n"
        "Page 2:\n"
        "Page URL: " + three_webpages_alt_text_folder + "2.html"
        "\n"
        "Image URLs:\n"
        "" + three_webpages_alt_text_folder + "2.jpeg"
        "\n"
        "Alt text: Second page\n"
        "\n"
        "Page 3:\n"
        "Page URL: " + three_webpages_alt_text_folder + "3.html"
        "\n"
        "Image URLs:\n"
        "\n"
        "\n"
    )


def test_print_verification_with_no_validation_throws_crawler_blocked():
    with pytest.raises(CrawlerBlocked):
        cli.print_verification(None)


def test_comics():
    runner = CliRunner()
    result = runner.invoke(cli.comics)
    assert result.exit_code == 0
    assert len(result.output) > 0


def test_good_download_ends_up_downloading(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")

    result = runner.invoke(cli.download, [first_comic])
    assert result.exit_code == 0
    assert mock_download.call_count == 1


def test_predefined_unknown_comic_does_not_download(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")

    result = runner.invoke(cli.download, ["foo"])
    assert result.exit_code == 2
    assert mock_download.call_count == 0


def test_predefined_downloadable_comic_downloads_the_comic(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")

    result = runner.invoke(cli.download, [first_comic])
    assert result.exit_code == 0
    assert mock_download.call_count == 1


def test_predefined_downloadable_comic_makes_the_cbz_file(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_convert_to_cbz = mocker.patch("webcomix.comic.Comic.convert_to_cbz")

    result = runner.invoke(cli.download, [first_comic, "--cbz"])
    assert result.exit_code == 0
    assert mock_convert_to_cbz.call_count == 1


def test_predefined_unknown_comic_does_not_make_the_cbz_file(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_convert_to_cbz = mocker.patch("webcomix.comic.Comic.convert_to_cbz")

    result = runner.invoke(cli.download, ["foo", "--cbz"])
    assert result.exit_code == 2
    assert mock_convert_to_cbz.call_count == 0


def test_custom_comic_asks_for_verification_before_downloading(mocker):
    runner = CliRunner()
    mock_manager = mocker.Mock()
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch("webcomix.comic.Comic.verify_xpath")
    mock_print_verification = mocker.patch("webcomix.cli.print_verification")
    mock_manager.attach_mock(mock_download, "download")
    mock_manager.attach_mock(mock_verify_xpath, "verify_xpath")
    mock_manager.attach_mock(mock_print_verification, "print_verification")

    result = runner.invoke(
        cli.custom,
        [
            "foo",
            "--start_url=url",
            "--next_page_xpath=next_page",
            "--image_xpath=image",
        ],
        "yes",
    )
    assert result.exit_code == 0
    mock_manager.assert_has_calls(
        [
            mocker.call.verify_xpath(),
            mocker.call.print_verification(mocker.ANY),
            mocker.call.download(),
        ]
    )


def test_custom_comic_makes_the_cbz_file(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch("webcomix.comic.Comic.verify_xpath")
    mock_print_verification = mocker.patch("webcomix.cli.print_verification")
    mock_convert_to_cbz = mocker.patch("webcomix.comic.Comic.convert_to_cbz")

    result = runner.invoke(
        cli.custom,
        [
            "foo",
            "--start_url=url",
            "--next_page_xpath=next_page",
            "--image_xpath=image",
            "--cbz",
        ],
        "y",
    )
    assert result.exit_code == 0
    assert mock_convert_to_cbz.call_count == 1


def test_custom_comic_doesnt_ask_for_verification_if_next_link_not_found(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch(
        "webcomix.comic.Comic.verify_xpath",
        side_effect=NextLinkNotFound(mocker.ANY, mocker.ANY),
    )
    mock_print_verification = mocker.patch("webcomix.cli.print_verification")

    result = runner.invoke(
        cli.custom,
        [
            "foo",
            "--start_url=url",
            "--next_page_xpath=next_page",
            "--image_xpath=image",
        ],
        "yes",
    )

    assert result.exit_code == 1
    assert type(result.exception) is SystemExit
    assert mock_verify_xpath.call_count == 1
    assert mock_print_verification.call_count == 0
    assert mock_download.call_count == 0


def test_custom_comic_doesnt_download_comic_if_crawler_blocked(mocker):
    runner = CliRunner()
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch("webcomix.comic.Comic.verify_xpath")
    mock_print_verification = mocker.patch(
        "webcomix.cli.print_verification", side_effect=CrawlerBlocked()
    )

    result = runner.invoke(
        cli.custom,
        [
            "foo",
            "--start_url=url",
            "--next_page_xpath=next_page",
            "--image_xpath=image",
        ],
        "yes",
    )

    assert result.exit_code == 1
    assert type(result.exception) is SystemExit
    assert mock_verify_xpath.call_count == 1
    assert mock_print_verification.call_count == 1
    assert mock_download.call_count == 0


def test_discovered_comic_searches_for_a_comic(mocker):
    runner = CliRunner()
    mock_discovery = mocker.patch(
        "webcomix.cli.discovery",
        return_value=(
            Comic(mocker.ANY, mocker.ANY, mocker.ANY, mocker.ANY, mocker.ANY),
            mocker.ANY,
        ),
    )
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch("webcomix.comic.Comic.verify_xpath")
    mock_print_verification = mocker.patch("webcomix.cli.print_verification")

    result = runner.invoke(cli.search, ["foo", "--start_url=good"], "y")
    assert result.exit_code == 0
    assert mock_discovery.call_count == 1


def test_discovered_comic_asks_for_verification_before_downloading(mocker):
    runner = CliRunner()
    mock_manager = mocker.Mock()
    mock_discovery = mocker.patch(
        "webcomix.cli.discovery",
        return_value=(
            Comic(mocker.ANY, mocker.ANY, mocker.ANY, mocker.ANY, mocker.ANY),
            mocker.ANY,
        ),
    )
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch("webcomix.comic.Comic.verify_xpath")
    mock_print_verification = mocker.patch("webcomix.cli.print_verification")
    mock_manager.attach_mock(mock_download, "download")
    mock_manager.attach_mock(mock_verify_xpath, "verify_xpath")
    mock_manager.attach_mock(mock_print_verification, "print_verification")

    result = runner.invoke(cli.search, ["foo", "--start_url=good"], "y")
    assert result.exit_code == 0
    mock_manager.assert_has_calls(
        [mocker.call.print_verification(mocker.ANY), mocker.call.download()]
    )


def test_discovered_comic_makes_cbz_file(mocker):
    runner = CliRunner()
    mock_discovery = mocker.patch(
        "webcomix.cli.discovery",
        return_value=(
            Comic(mocker.ANY, mocker.ANY, mocker.ANY, mocker.ANY, mocker.ANY),
            mocker.ANY,
        ),
    )
    mock_download = mocker.patch("webcomix.comic.Comic.download")
    mock_verify_xpath = mocker.patch("webcomix.comic.Comic.verify_xpath")
    mock_print_verification = mocker.patch("webcomix.cli.print_verification")
    mock_convert_to_cbz = mocker.patch("webcomix.comic.Comic.convert_to_cbz")

    result = runner.invoke(cli.search, ["foo", "--start_url=good", "--cbz"], "y")
    assert result.exit_code == 0
    assert mock_convert_to_cbz.call_count == 1
