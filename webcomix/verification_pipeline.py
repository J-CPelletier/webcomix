class VerificationPipeline:
    def open_spider(self, spider):
        self.pages = []

    def close_spider(self, spider):
        for page in self.pages:
            click.echo(page)

    def process_item(self, item, info):
        image_path = Comic.save_image_location(
            item.get("url"), item.get("page"), info.spider.directory
        )
        yield scrapy.Request(
            item.get("url"),
            meta={
                "image_file_name": Comic.save_image_location(
                    item.get("url"), item.get("page")
                )
            },
        )
