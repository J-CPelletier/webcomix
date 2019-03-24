from webcomix.scrapy.download.comic_spider import ComicSpider


def test_parse_yields_good_page(mocker):
    mock_response = mocker.patch("scrapy.http.Response")
    mock_response.urljoin.return_value = "http://xkcd.com/3/"
    mock_response.url = "http://xkcd.com/2/"
    mock_selector = mocker.patch("scrapy.selector.SelectorList")
    mock_response.xpath.return_value = mock_selector
    mock_selector.getall.return_value = ["//imgs.xkcd.com/comics/tree_cropped_(1).jpg"]
    mock_selector.get.return_value = "xkcd.com/3/"

    spider = ComicSpider()
    result = spider.parse(mock_response)
    results = list(result)
    assert len(results) == 2
    assert results[0].get("url") == "http://imgs.xkcd.com/comics/tree_cropped_(1).jpg"
    assert results[1].url == "http://xkcd.com/3/"


def test_parse_yields_multiple_subpages(mocker):
    mock_response = mocker.patch("scrapy.http.Response")
    mock_response.urljoin.return_value = "http://xkcd.com/3/"
    mock_response.url = "http://xkcd.com/2/"
    mock_selector = mocker.patch("scrapy.selector.SelectorList")
    mock_response.xpath.return_value = mock_selector
    mock_selector.getall.return_value = [
        "//imgs.xkcd.com/comics/tree_cropped_(1).jpg",
        "//imgs.xkcd.com/comics/tree_cropped_(2).jpg",
    ]
    mock_selector.get.return_value = "xkcd.com/3/"

    spider = ComicSpider()
    result = spider.parse(mock_response)
    results = list(result)
    assert len(results) == 3
    assert results[0].get("url") == "http://imgs.xkcd.com/comics/tree_cropped_(1).jpg"
    assert results[1].get("url") == "http://imgs.xkcd.com/comics/tree_cropped_(2).jpg"
    assert results[2].url == "http://xkcd.com/3/"


def test_parse_strips_additionnal_spaces(mocker):
    mock_response = mocker.patch("scrapy.http.Response")
    mock_response.urljoin.return_value = " http://xkcd.com/3/ "
    mock_response.url = "http://xkcd.com/2/"
    mock_selector = mocker.patch("scrapy.selector.SelectorList")
    mock_response.xpath.return_value = mock_selector
    mock_selector.getall.return_value = [
        " //imgs.xkcd.com/comics/tree_cropped_(1).jpg ",
        " //imgs.xkcd.com/comics/tree_cropped_(2).jpg ",
    ]
    mock_selector.get.return_value = " xkcd.com/3/ "

    spider = ComicSpider()
    result = spider.parse(mock_response)
    results = list(result)
    assert len(results) == 3
    assert results[0].get("url") == "http://imgs.xkcd.com/comics/tree_cropped_(1).jpg"
    assert results[1].get("url") == "http://imgs.xkcd.com/comics/tree_cropped_(2).jpg"
    assert results[2].url == "http://xkcd.com/3/"


def test_parse_yields_no_pages(mocker):
    mock_response = mocker.patch("scrapy.http.Response")
    mock_response.urljoin.return_value = "http://xkcd.com/3/"
    mock_response.url = "http://xkcd.com/2/"
    mock_selector = mocker.patch("scrapy.selector.SelectorList")
    mock_response.xpath.return_value = mock_selector
    mock_selector.getall.return_value = []
    mock_selector.get.return_value = "xkcd.com/3/"

    spider = ComicSpider()
    result = spider.parse(mock_response)
    results = list(result)
    assert len(results) == 1
    assert results[0].url == "http://xkcd.com/3/"
