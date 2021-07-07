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
        "https://karlkerschl.com/comic/episode-one/",
        "//div[@id='comic']//img/@src",
        "//a[contains(@class, 'comic-nav-next')]/@href",
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
        "//img[@class='comicnormal' and contains(@src, 'comicpages')]/@src",
        "//a[img[contains(@src, 'next')]]/@href",
    ),
    "SchlockMercenary": (
        "https://www.schlockmercenary.com/2000-06-12",
        "//div[@class='strip-images']//img/@src",
        "//a[@class='next-strip']/@href",
    ),
    "Nerfnow": (
        "https://www.nerfnow.com/comic/4",
        "//div[@id='comic']//img/@src",
        "//li[@id='nav_next']//a/@href",
    ),
    "EdisonRex": (
        "https://www.edisonrex.net/comic/issue-1-cover",
        "//div[@id='cc-comicbody']//img/@src",
        "//a[@class='cc-next']/@href",
    ),
    "Spinnerette": (
        "https://www.spinnyverse.com/comic/02-09-2010",
        "//div[@id='cc-comicbody']//img/@src",
        "//a[@class='cc-next']/@href",
    ),
    "RyanMadeMistakes": (
        "http://mistakes.ryanestrada.com/comic/0001",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "MissingMonday": (
        "https://www.missingmondaycomic.com/comic/chapter-01-page-01",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "StarTrip": (
        "https://www.startripcomic.com/comic/chapter-1-cover",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "StupidFox": (
        "http://stupidfox.net/hello",
        "//img[contains(@src, 'stupidfox.net/art/')]/@src",
        "//span[@class='spriteNext']/parent::a/@href",
    ),
    "GunnerkriggCourt": (
        "https://www.gunnerkrigg.com/?p=1",
        "//img[@class='comic_image']/@src",
        "//a[img[contains(@src, 'next')]]/@href",
    ),
    "Housepets": (
        "https://www.housepetscomic.com/comic/2008/06/02/when-boredom-strikes/",
        "//div[@id='comic']//img/@src",
        "//div[@id='comic']//@href",
    ),
}
