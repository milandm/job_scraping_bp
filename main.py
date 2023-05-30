import asyncio
import fire
from log.log_config import get_logger
from utils.constants import SourceDirectoryConstants
from tasks import scrape_companies_data_from_csv, async_scrape_companies_data_from_csv
from tasks import read_export_csv_file, async_read_export_csv_file
from utils.constants import RunAppConstants

logger = get_logger('main')


def main(
    data_source=RunAppConstants.DEFAULT_DATA_SOURCE,
    db_config=RunAppConstants.DB_CONFIG,
    delimiter=RunAppConstants.DELIMITER,
    bucket_name=RunAppConstants.EXPORT_BUCKET_NAME
):
    csv_files_dir_path = RunAppConstants.BASE_CSV_FILES_DIR + SourceDirectoryConstants.sources_dir_dict.get(data_source)
    # async_scrape_companies_data_from_csv.delay(
    #     data_source,
    #     csv_files_dir_path,
    #     RunAppConstants.BASE_COLLECTION_NAME,
    #     db_config,
    #     delimiter,
    #     bucket_name
    # )
    async_read_export_csv_file.delay(
        data_source=data_source,
        base_collection_name=RunAppConstants.BASE_COLLECTION_NAME,
        db_config=db_config,
        delimiter=delimiter,
        csv_files_dir=csv_files_dir_path,
        bucket_name=bucket_name,
        export_file_name='linkedin_sales_nav'
    )


if __name__ == '__main__':
    fire.Fire(main)
