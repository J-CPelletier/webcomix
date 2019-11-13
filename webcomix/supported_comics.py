supported_comics = {
    "xkcd": (
        "https://xkcd.com/1/",
        "//div[@id='comic']//img/@src",
        "//a[@rel='next']/@href",
    ),
    "xkcd_alt": (
        "https://xkcd.com/1/",
        "//div[@id='comic']//img/@src",
        "//a[@rel='next']/@href",
        "//div[@id='comic']//img/@title",
    ),
    "Nedroid": (
        "http://nedroid.com/2005/09/2210-whee/",
        "//div[@id='comic']/img/@src",
        "//div[@class='nav-next']/a/@href",
    ),
    "JL8": (
        "https://limbero.org/jl8/1",
        "//img[@alt='Comic']/@src",
        "//a[text()='>']/@href",
    ),
    "SMBC": (
        "https://www.smbc-comics.com/comic/2002-09-05",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "Blindsprings": (
        "https://www.blindsprings.com/comic/blindsprings-cover-book-one",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "TheAbominableCharlesChristopher": (
        "https://abominable.cc/post/44164796353/episode-one",
        "//div[@class='photo']//img/@src",
        "//span[@class='next_post']//@href",
    ),
    "GuildedAge": (
        "https://guildedage.net/comic/chapter-1-cover/",
        "//div[@id='comic']//img/@src",
        "//a[@class='navi comic-nav-next navi-next']/@href",
    ),
    "TalesOfElysium": (
        "https://ssp-comics.com/comics/toe/?page=1&mode=10",
        "//div[@id='ImageComicContainer']//img[contains(@src, 'comic')]/@src",
        "//a[button/@id='next10Button']/@href",
    ),
    "AmazingSuperPowers": (
        "https://www.amazingsuperpowers.com/2007/09/heredity/",
        "//div[@class='comicpane']/img/@src",
        "//a[@class='navi navi-next']/@href",
    ),
    "Gunshow": (
        "https://gunshowcomic.com/1",
        "//img[@class='strip']/@src",
        "//span[@class='snavb'][4]/a/@href",
    ),
    "Lackadaisy": (
        "https://www.lackadaisycats.com/comic.php?comicid=1",
        "//div[@id='content']/img/@src",
        "//div[@class='next']/a/@href",
    ),
    "WildeLife": (
        "https://www.wildelifecomic.com/comic/1",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "ElGoonishShive": (
        "https://www.egscomics.com/comic/2002-01-21",
        "//div[@id='cc-comicbody']//img/@src",
        "//a[@class='cc-next']/@href",
    ),
    "StandStillStaySilent": (
        "https://www.sssscomic.com/comic.php?page=1",
        "//img[@class='comicnormal']/@src",
        "//a[img[contains(@src, 'next')]]/@href",
    ),
    "SchlockMercenary": (
        "https://www.schlockmercenary.com/2000-06-12",
        "//div[@class='strip-images']//img/@src",
        "//a[@class='next-strip']/@href",
    ),
}
