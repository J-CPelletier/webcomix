supported_comics = {
    "xkcd": {
        "name": "xkcd",
        "start_url": "https://xkcd.com/1/",
        "comic_image_selector": "//div[@id='comic']//img/@src",
        "next_page_selector": "//a[@rel='next']/@href",
    },
    "xkcd_alt": {
        "name": "xkcd_alt",
        "start_url": "https://xkcd.com/1/",
        "comic_image_selector": "//div[@id='comic']//img/@src",
        "next_page_selector": "//a[@rel='next']/@href",
        "alt_text": "//div[@id='comic']//img/@title",
    },
    "Nedroid": {
        "name": "Nedroid",
        "start_url": "http://nedroid.com/2005/09/2210-whee/",
        "comic_image_selector": "//div[@id='comic']/img/@src",
        "next_page_selector": "//div[@class='nav-next']/a/@href",
    },
    "JL8": {
        "name": "JL8",
        "start_url": "https://limbero.org/jl8/1",
        "comic_image_selector": "//img[@alt='Comic']/@src",
        "next_page_selector": "//a[text()='>']/@href",
    },
    "SMBC": {
        "name": "SMBC",
        "start_url": "https://www.smbc-comics.com/comic/2002-09-05",
        "comic_image_selector": "//img[@id='cc-comic']/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "Blindsprings": {
        "name": "Blindsprings",
        "start_url": "https://www.blindsprings.com/comic/blindsprings-cover-book-one",
        "comic_image_selector": "//img[@id='cc-comic']/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "TheAbominableCharlesChristopher": {
        "name": "TheAbominableCharlesChristopher",
        "start_url": "https://karlkerschl.com/comic/episode-one/",
        "comic_image_selector": "//div[@id='comic']//img/@src",
        "next_page_selector": "//a[contains(@class, 'comic-nav-next')]/@href",
    },
    "GuildedAge": {
        "name": "GuildedAge",
        "start_url": "https://guildedage.net/comic/chapter-1-cover/",
        "comic_image_selector": "//div[@id='comic']//img/@src",
        "next_page_selector": "//a[@class='navi comic-nav-next navi-next']/@href",
    },
    "TalesOfElysium": {
        "name": "TalesOfElysium",
        "start_url": "https://ssp-comics.com/comics/toe/?page=1&mode=10",
        "comic_image_selector": "//div[@id='ImageComicContainer']//img[contains(@src, 'comic')]/@src",
        "next_page_selector": "//a[button/@id='next10Button']/@href",
    },
    "AmazingSuperPowers": {
        "name": "AmazingSuperPowers",
        "start_url": "https://www.amazingsuperpowers.com/2007/09/heredity/",
        "comic_image_selector": "//div[@class='comicpane']/img/@src",
        "next_page_selector": "//a[@class='navi navi-next']/@href",
    },
    "Gunshow": {
        "name": "Gunshow",
        "start_url": "https://gunshowcomic.com/1",
        "comic_image_selector": "//img[@class='strip']/@src",
        "next_page_selector": "//span[@class='snavb'][4]/a/@href",
    },
    "Lackadaisy": {
        "name": "Lackadaisy",
        "start_url": "https://www.lackadaisycats.com/comic.php?comicid=1",
        "comic_image_selector": "//div[@id='content']/img/@src",
        "next_page_selector": "//div[@class='next']/a/@href",
    },
    "WildeLife": {
        "name": "WildeLife",
        "start_url": "https://www.wildelifecomic.com/comic/1",
        "comic_image_selector": "//img[@id='cc-comic']/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "ElGoonishShive": {
        "name": "ElGoonishShive",
        "start_url": "https://www.egscomics.com/comic/2002-01-21",
        "comic_image_selector": "//div[@id='cc-comicbody']//img/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "StandStillStaySilent": {
        "name": "StandStillStaySilent",
        "start_url": "https://www.sssscomic.com/comic.php?page=1",
        "comic_image_selector": "//img[@class='comicnormal' and contains(@src, 'comicpages')]/@src",
        "next_page_selector": "//a[img[contains(@src, 'next')]]/@href",
    },
    "SchlockMercenary": {
        "name": "SchlockMercenary",
        "start_url": "https://www.schlockmercenary.com/2000-06-12",
        "comic_image_selector": "//div[@class='strip-images']//img/@src",
        "next_page_selector": "//a[@class='next-strip']/@href",
    },
    "Nerfnow": {
        "name": "Nerfnow",
        "start_url": "https://www.nerfnow.com/comic/4",
        "comic_image_selector": "//div[@id='comic']//img/@src",
        "next_page_selector": "//li[@id='nav_next']//a/@href",
    },
    "EdisonRex": {
        "name": "EdisonRex",
        "start_url": "https://www.edisonrex.net/comic/issue-1-cover",
        "comic_image_selector": "//div[@id='cc-comicbody']//img/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "Spinnerette": {
        "name": "Spinnerette",
        "start_url": "https://www.spinnyverse.com/comic/02-09-2010",
        "comic_image_selector": "//div[@id='cc-comicbody']//img/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "RyanMadeMistakes": {
        "name": "RyanMadeMistakes",
        "start_url": "http://mistakes.ryanestrada.com/comic/0001",
        "comic_image_selector": "//img[@id='cc-comic']/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "MissingMonday": {
        "name": "MissingMonday",
        "start_url": "https://www.missingmondaycomic.com/comic/chapter-01-page-01",
        "comic_image_selector": "//img[@id='cc-comic']/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "StarTrip": {
        "name": "StarTrip",
        "start_url": "https://www.startripcomic.com/comic/chapter-1-cover",
        "comic_image_selector": "//img[@id='cc-comic']/@src",
        "next_page_selector": "//a[@class='cc-next']/@href",
    },
    "GunnerkriggCourt": {
        "name": "GunnerkriggCourt",
        "start_url": "https://www.gunnerkrigg.com/?p=1",
        "comic_image_selector": "//img[@class='comic_image']/@src",
        "next_page_selector": "//a[img[contains(@src, 'next')]]/@href",
    },
    "Housepets": {
        "name": "Housepets",
        "start_url": "https://www.housepetscomic.com/comic/2008/06/02/when-boredom-strikes/",
        "comic_image_selector": "//div[@id='comic']//img/@src",
        "next_page_selector": "//div[@id='comic']//@href",
    },
}
