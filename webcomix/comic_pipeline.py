import os

import click
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from webcomix.comic import Comic


class ComicPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        click.echo("Saving image {}".format(item.get('image_element')))
        image_path = Comic.save_image_location(
            item.get("image_element"), item.get("page"), info.spider.directory)
        if os.path.isfile(image_path):
            click.echo("The image was already downloaded. Skipping...")
            raise DropItem("The image was already downloaded. Skipping...")
        yield scrapy.Request(
            item.get("image_element"),
            meta={
                'page': item.get('page'),
                'image_element': item.get('image_element')
            })

    def item_completed(self, results, item, info):
        file_paths = [data['path'] for ok, data in results if ok]
        if not file_paths:
            click.echo("Could not find comic image.")
            raise DropItem("Could not find comic image.")

        return item

    def file_path(self, request, response=None, info=None):
        path = Comic.save_image_location(
            request.meta.get("image_element"), request.meta.get("page"))
        return path
