from celery_app import app
from export.export_data.async_company_profiles_export import AsyncCompanyProfilesExport
from export.export_data.company_profiles_export import CompanyProfilesExport
from export.csv.csv_export import CsvExport
from export.csv.async_csv_export import AsyncCsvExport
from log.log_config import get_logger
from load.utils import get_mongodb, get_async_mongodb
from engines.csv_file_scraper_engine import CsvFilesScraperEngine
from engines.async_csv_file_scraper_engine import AsyncCsvFilesScraperEngine
from engines.read_csv_file_export_engine import ReadCsvFilesExportEngine
from engines.async_read_csv_fiiles_export_engine import AsyncReadCsvFilesExportEngine
from load.store_company_internal_profiles.store_data import StoreData
from load.store_company_internal_profiles.async_store_data import AsyncStoreData
from extract.scraping.scrape_data.companies_crawler import CompaniesCrawler
from load.utils import get_s3_obj
from load.utils import get_async_s3_obj
import asyncio
from utils.utils import get_config
from utils.utils import get_predictions_csv_filename

logger = get_logger('tasks')


@app.task
def async_scrape_companies_data_from_csv(
        data_source: str,
        csv_files_dir: str,
        base_collection_name: str,
        db_config: str,
        delimiter: str,
        bucket_name: str
):
    config = get_config(logger, db_config)
    async_mongo_db = get_async_mongodb(config, base_collection_name)
    mongo_db = get_mongodb(config, base_collection_name)
    s3 = get_s3_obj(config=config, bucket_name=bucket_name)
    store_data = AsyncStoreData(data_source, async_mongo_db)
    companies_crawler = CompaniesCrawler(data_source=data_source, s3=s3, db=mongo_db)
    csv_files_scraper_engine = AsyncCsvFilesScraperEngine(
        data_source=data_source,
        store_data=store_data,
        companies_crawler=companies_crawler,
        csv_files_dir=csv_files_dir,
        delimiter=delimiter
    )
    stored_companies_list = asyncio.run(csv_files_scraper_engine.run())
    logger.debug(f'stored {len(stored_companies_list)} companies')
    csv_files_scraper_engine.run_crawling(stored_companies_list)


@app.task
def scrape_companies_data_from_csv(
        data_source: str,
        csv_files_dir: str,
        base_collection_name: str,
        db_config: str,
        delimiter: str,
        bucket_name: str
):
    config = get_config(logger, db_config)
    mongo_db = get_mongodb(config, base_collection_name)
    s3 = get_s3_obj(config=config, bucket_name=bucket_name)
    store_data = StoreData(data_source, mongo_db)
    companies_crawler = CompaniesCrawler(data_source, s3, mongo_db)
    csv_files_scraper_engine = CsvFilesScraperEngine(
        data_source=data_source,
        store_data=store_data,
        companies_crawler=companies_crawler,
        csv_files_dir=csv_files_dir,
        delimiter=delimiter
    )
    csv_files_scraper_engine.run()


@app.task
def read_export_csv_file(
        data_source: str,
        base_collection_name: str,
        db_config: str,
        delimiter: str,
        csv_files_dir: str,
        bucket_name: str,
        export_file_name
):
    config = get_config(logger, db_config)
    mongo_db = get_mongodb(config, base_collection_name)
    s3 = get_s3_obj(config=config, bucket_name=bucket_name)
    file_path = get_predictions_csv_filename(filename=export_file_name, data_source=data_source)
    data_export = CsvExport(file_path, data_source)
    company_profiles_export = CompanyProfilesExport(data_source, mongo_db, s3, data_export)
    read_export_engine = ReadCsvFilesExportEngine(
        data_source=data_source,
        db=mongo_db,
        company_profiles_export=company_profiles_export,
        csv_files_dir=csv_files_dir,
        delimiter=delimiter
    )
    exported_companies = read_export_engine.run()
    logger.debug(f'Exported {len(exported_companies)} company profiles')


@app.task
def async_read_export_csv_file(
        data_source: str,
        base_collection_name: str,
        db_config: str,
        delimiter: str,
        csv_files_dir: str,
        bucket_name: str,
        export_file_name
):
    config = get_config(logger, db_config)
    mongo_db = get_async_mongodb(config, base_collection_name)
    s3 = get_async_s3_obj(config=config, bucket_name=bucket_name)
    file_path = get_predictions_csv_filename(filename=export_file_name, data_source=data_source)
    data_export = AsyncCsvExport(file_path, data_source)
    company_profiles_export = AsyncCompanyProfilesExport(data_source, mongo_db, s3, data_export)
    read_export_engine = AsyncReadCsvFilesExportEngine(
        data_source=data_source,
        db=mongo_db,
        company_profiles_export=company_profiles_export,
        csv_files_dir=csv_files_dir,
        delimiter=delimiter
    )
    exported_companies = asyncio.run(read_export_engine.run())
    logger.debug(f'Exported {len(exported_companies)} company profiles')
