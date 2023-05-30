import csv
from typing import List
import aiofiles as aiofiles
from export.data_export import DataExport
from load.models.company_internal_profile import CompanyInternalProfile
import aiocsv
from log.log_config import get_logger
from transform.transform import Transform
from utils.constants import CsvExportProfilePreviewConstants


class AsyncCsvExport(DataExport):

    def __init__(self, csv_path, data_source):
        self.logger = get_logger('AsyncCsvExport')
        super().__init__(file_path=csv_path, data_source=data_source)

    async def export_companies_data(
            self,
            company_internal_profiles: List[CompanyInternalProfile]
    ):
        exported_companies = []
        transform = Transform()
        async with aiofiles.open(file=self.file_path, mode='w+', encoding='utf-8', newline='') as file:
            writer = aiocsv.AsyncDictWriter(
                file, CsvExportProfilePreviewConstants.CSV_EXPORT_HEADER, restval='NULL', quoting=csv.QUOTE_ALL
            )
            await writer.writeheader()
            for company_profile in company_internal_profiles:
                try:
                    csv_export_company = transform.company_internal_profile_to_csv(
                        self.data_source, company_profile
                    )
                    await writer.writerow(csv_export_company)
                    exported_companies.append(company_profile)
                except Exception as e:
                    self.logger.debug(f'Exception writing to file: {e}')
        return exported_companies
