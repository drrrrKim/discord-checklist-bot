from crawling.royal import crawling_royal
from crawling.wonki_berry import crawling_wonki_berry
from crawling.event import crawling_event

async def kms_migration(path_dir):
    await crawling_wonki_berry(path_dir)
    await crawling_royal(path_dir)
    await crawling_event(path_dir)