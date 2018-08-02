from click.testing import CliRunner

from webcomix import main
from webcomix.comic import Comic
from webcomix.supported_comics import supported_comics

first_comic = list(sorted(supported_comics.keys()))[0]


def test_print_verification(capfd):
    verification = Comic.verify_xpath(*supported_comics["xkcd"])
    main.print_verification(verification)
    out, err = capfd.readouterr()
    assert out == (
        "Page 1: \n"
        "Page URL: http://xkcd.com/1/\n"
        "Image URL: http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg\n"
        "\n"
        "Page 2: \n"
        "Page URL: http://xkcd.com/2/\n"
        "Image URL: http://imgs.xkcd.com/comics/tree_cropped_(1).jpg\n"
        "\n"
        "Page 3: \n"
        "Page URL: http://xkcd.com/3/\n"
        "Image URL: http://imgs.xkcd.com/comics/island_color.jpg\n\n")


def test_comics():
    runner = CliRunner()
    result = runner.invoke(main.comics)
    assert result.exit_code == 0
    assert len(result.output) > 0


def test_good_download_ends_up_downloading(mocker):
    runner = CliRunner()
    mock_download = mocker.patch('webcomix.comic.Comic.download')

    result = runner.invoke(main.download, [first_comic])
    assert result.exit_code == 0
    assert mock_download.call_count == 1


def test_unknown_download_does_nothing(mocker):
    runner = CliRunner()
    mock_download = mocker.patch('webcomix.comic.Comic.download')

    result = runner.invoke(main.download, ["foo"])
    assert result.exit_code == 0
    assert mock_download.call_count == 0


def test_good_download_makes_the_cbz_file(mocker):
    runner = CliRunner()
    mock_download = mocker.patch('webcomix.comic.Comic.download')
    mock_make_cbz = mocker.patch('webcomix.comic.Comic.make_cbz')

    result = runner.invoke(main.download, [first_comic, "--cbz"])
    assert result.exit_code == 0
    assert mock_download.call_count == 1
    assert mock_make_cbz.call_count == 1


def test_bad_download_does_not_make_the_cbz(mocker):
    runner = CliRunner()
    mock_download = mocker.patch('webcomix.comic.Comic.download')
    mock_make_cbz = mocker.patch('webcomix.comic.Comic.make_cbz')

    result = runner.invoke(main.download, ["foo", "--cbz"])
    assert result.exit_code == 0
    assert mock_download.call_count == 0
    assert mock_make_cbz.call_count == 0


def test_custom(mocker):
    runner = CliRunner()
    mock_download = mocker.patch('webcomix.comic.Comic.download')
    mock_verify_xpath = mocker.patch('webcomix.comic.Comic.verify_xpath')
    mock_print_verification = mocker.patch('webcomix.main.print_verification')

    result = runner.invoke(main.custom, [
        "--comic_name=foo", "--start_url=url", "--next_page_xpath=next_page",
        "--image_xpath=image"
    ], "yes")
    assert result.exit_code == 0
    assert mock_download.call_count == 1
    assert mock_verify_xpath.call_count == 1
    assert mock_print_verification.call_count == 1


def test_custom_make_cbz(mocker):
    runner = CliRunner()
    mock_download = mocker.patch('webcomix.comic.Comic.download')
    mock_verify_xpath = mocker.patch('webcomix.comic.Comic.verify_xpath')
    mock_print_verification = mocker.patch('webcomix.main.print_verification')
    mock_make_cbz = mocker.patch('webcomix.comic.Comic.make_cbz')

    result = runner.invoke(main.custom, [
        "--comic_name=foo", "--start_url=url", "--next_page_xpath=next_page",
        "--image_xpath=image", "--cbz"
    ], "y")
    assert result.exit_code == 0
    assert mock_download.call_count == 1
    assert mock_verify_xpath.call_count == 1
    assert mock_print_verification.call_count == 1
    assert mock_make_cbz.call_count == 1


def test_search(mocker):
    runner = CliRunner()
    mock_discovery = mocker.patch(
        'webcomix.main.discovery',
        return_value=Comic("url", "next_page", "comic_image"))
    mock_download = mocker.patch('webcomix.comic.Comic.download')
    mock_verify_xpath = mocker.patch('webcomix.comic.Comic.verify_xpath')
    mock_print_verification = mocker.patch('webcomix.main.print_verification')

    result = runner.invoke(main.search, ["foo", "--start_url=good"], "y")
    assert result.exit_code == 0
    assert mock_discovery.call_count == 1
    assert mock_download.call_count == 1
    assert mock_verify_xpath.call_count == 1
    assert mock_print_verification.call_count == 1
