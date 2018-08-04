import os

import click
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

from webcomix.comic import Comic


class ComicPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        click.echo("Saving image {}".format(item.get('url')))
        image_path = Comic.save_image_location(
            item.get("url"), item.get("page"), info.spider.directory)
        if os.path.isfile(image_path):
            click.echo("The image was already downloaded. Skipping...")
            raise DropItem("The image was already downloaded. Skipping...")
        yield scrapy.Request(
            item.get("url"),
            meta={
                'image_path':
                Comic.save_image_location(item.get("url"), item.get("page"))
            })

    def item_completed(self, results, item, info):
        file_paths = [data['path'] for ok, data in results if ok]
        if not file_paths:
            click.echo("Could not find comic image.")
            raise DropItem("Could not find comic image.")

        return item

    def file_path(self, request, response=None, info=None):
        return request.meta.get('image_path')
