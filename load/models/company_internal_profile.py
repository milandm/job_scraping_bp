from load.models.company_internal_item import CompanyInternalItem
from load.models.company_internal_item_prediction import CompanyInternalItemPrediction
from typing import List, Dict, Optional
from datetime import datetime
from utils.utils import get_date_now_timestamp, get_date_from_string, get_date_str_now, get_date_str_from_timestamp


class CompanyInternalProfileConstants:
    id = "_id"
    company_name = "company_name"
    full_web_address = "full_web_address"
    base_web_address = "base_web_address"
    company_internal_items = "company_internal_items"
    company_external_items_dict = "company_external_items_dict"
    language = "language"
    company_internal_item_labels_dict = "company_internal_item_labels_dict"
    company_internal_item_predictions_dict = "company_internal_item_predictions_dict"
    date = "date"
    latest_date_published = "latest_date_published"
    source_data_created_date = "source_data_created_date"
    scraping_error_list = "scraping_error_list"


class CompanyInternalProfile:
    id: str
    company_name: str
    full_web_address: str
    base_web_address: str
    company_internal_items: List[CompanyInternalItem]
    company_external_items_dict: dict
    language: Optional[str]
    company_internal_item_labels_dict: Dict[str, CompanyInternalItemPrediction]
    company_internal_item_predictions_dict: Dict[str, CompanyInternalItemPrediction]
    date: datetime
    latest_date_published: datetime
    source_data_created_date: datetime
    scraping_error_list: List[str]

    def __init__(
            self,
            id: str = None,
            company_name: str = '',
            full_web_address: str = '',
            base_web_address: str = '',
            company_internal_items: List[CompanyInternalItem] = None,
            company_external_items_dict: dict = None,
            language: str = '',
            company_internal_item_labels_dict: Dict[str, CompanyInternalItemPrediction] = None,
            company_internal_item_predictions_dict: Dict[str, CompanyInternalItemPrediction] = None,
            date=get_date_str_now(),
            latest_date_published=None,
            source_data_created_date=None,
            scraping_error_list=None
    ):
        if id:
            self.id = id
        self.company_name: str = company_name
        self.full_web_address: str = full_web_address
        self.base_web_address: str = base_web_address
        self.company_internal_items: list = company_internal_items if company_internal_items else []
        self.company_external_items_dict: dict = company_external_items_dict if company_external_items_dict else {}
        self.language: str = language
        self.company_internal_item_labels_dict = company_internal_item_labels_dict if company_internal_item_labels_dict else {}
        self.company_internal_item_predictions_dict = company_internal_item_predictions_dict if company_internal_item_predictions_dict else {}
        self.date = date
        self.latest_date_published = latest_date_published
        self.source_data_created_date = source_data_created_date
        self.scraping_error_list = scraping_error_list if scraping_error_list else []

    @classmethod
    def from_dict(cls, company_internal_profile_dict):

        company_internal_item_labels_dict = company_internal_profile_dict.get(
            CompanyInternalProfileConstants.company_internal_item_labels_dict, None)
        object_company_internal_item_labels_dict = dict()
        if company_internal_item_labels_dict:
            object_company_internal_item_labels_dict = {
                criterion_name: CompanyInternalItemPrediction.from_dict(jsonObjectCompany) for
                criterion_name, jsonObjectCompany in company_internal_item_labels_dict.items()}

        company_internal_item_predictions_dict = company_internal_profile_dict.get(
            CompanyInternalProfileConstants.company_internal_item_predictions_dict, None)
        object_company_internal_item_predictions_dict = dict()
        if company_internal_item_predictions_dict:
            object_company_internal_item_predictions_dict = {
                criterion_name: CompanyInternalItemPrediction.from_dict(jsonObjectCompany) for
                criterion_name, jsonObjectCompany in company_internal_item_predictions_dict.items()}

        default_date_timestamp = get_date_now_timestamp()
        date_timestamp = company_internal_profile_dict.get(CompanyInternalProfileConstants.date, default_date_timestamp)
        date_str = get_date_str_from_timestamp(date_timestamp)

        default_latest_date_published_timestamp = None
        latest_date_published_timestamp = company_internal_profile_dict.get(
            CompanyInternalProfileConstants.latest_date_published, default_latest_date_published_timestamp)
        latest_date_published_str = get_date_str_from_timestamp(latest_date_published_timestamp)

        default_source_data_created_date_timestamp = None
        source_data_created_date_timestamp = company_internal_profile_dict.get(
            CompanyInternalProfileConstants.source_data_created_date, default_source_data_created_date_timestamp)
        source_data_created_date_str = get_date_str_from_timestamp(source_data_created_date_timestamp)

        if company_internal_profile_dict:
            return cls(id=company_internal_profile_dict.get(CompanyInternalProfileConstants.id),
                       company_name=company_internal_profile_dict.get(CompanyInternalProfileConstants.company_name),
                       full_web_address=company_internal_profile_dict.get(
                           CompanyInternalProfileConstants.full_web_address),
                       base_web_address=company_internal_profile_dict.get(
                           CompanyInternalProfileConstants.base_web_address),
                       company_internal_items=list(
                           map(lambda json_object_company: CompanyInternalItem.from_dict(json_object_company),
                               company_internal_profile_dict.get(
                                   CompanyInternalProfileConstants.company_internal_items)))
                       if company_internal_profile_dict.get(
                           CompanyInternalProfileConstants.company_internal_items) else list(),
                       language=company_internal_profile_dict.get(CompanyInternalProfileConstants.language, ""),
                       company_internal_item_labels_dict=object_company_internal_item_labels_dict,
                       company_internal_item_predictions_dict=object_company_internal_item_predictions_dict,
                       company_external_items_dict=company_internal_profile_dict.get(
                           CompanyInternalProfileConstants.company_external_items_dict, dict()),
                       date=date_str,
                       latest_date_published=latest_date_published_str,
                       source_data_created_date=source_data_created_date_str,
                       scraping_error_list=company_internal_profile_dict.get(
                           CompanyInternalProfileConstants.scraping_error_list, None))
        else:
            return None

    def to_dict(self):
        date_timestamp = get_date_from_string(self.date)
        latest_date_published_timestamp = get_date_from_string(self.latest_date_published)
        source_data_created_date_timestamp = get_date_from_string(self.source_data_created_date)
        dict_value = {
            CompanyInternalProfileConstants.company_name: self.company_name,
            CompanyInternalProfileConstants.full_web_address: self.full_web_address,
            CompanyInternalProfileConstants.base_web_address: self.base_web_address,
            CompanyInternalProfileConstants.company_internal_items: list(
                map(lambda company_internal_item: company_internal_item.to_dict(),
                    (self.company_internal_items or []))),
            CompanyInternalProfileConstants.language: self.language,
            CompanyInternalProfileConstants.company_external_items_dict: self.company_external_items_dict,
            CompanyInternalProfileConstants.company_internal_item_labels_dict: {
                criterion: company_internal_item_label.to_dict() for criterion, company_internal_item_label in
                (self.company_internal_item_labels_dict or dict()).items()},
            CompanyInternalProfileConstants.company_internal_item_predictions_dict: {
                criterion: company_internal_item_prediction.to_dict() for
                criterion, company_internal_item_prediction in
                (self.company_internal_item_predictions_dict or dict()).items()},
            CompanyInternalProfileConstants.date: date_timestamp,
            CompanyInternalProfileConstants.latest_date_published: latest_date_published_timestamp,
            CompanyInternalProfileConstants.source_data_created_date: source_data_created_date_timestamp,
            CompanyInternalProfileConstants.scraping_error_list: self.scraping_error_list}
        return dict(dict_value)

    def __str__(self):
        string = f'\tcompany_name: {(self.company_name if self.company_name else "")}' \
                 + f'\tfull_web_address: {(self.full_web_address if self.full_web_address else "")}' \
                 + f'\tbase_web_address: {(self.base_web_address if self.base_web_address else "")}' \
                 + f'\tcompany_internal_items: {self.company_internal_items}' \
                 + f'\tlanguage: {(self.language if self.language else "")}' \
                 + f'\tcompany_external_items_dict: {self.company_external_items_dict if self.company_external_items_dict else ""}' \
                 + f'\tcompany_internal_item_labels_dict: {self.company_internal_item_labels_dict if self.company_internal_item_labels_dict else ""}' \
                 + f'\tcompany_internal_item_predictions_dict: {self.company_internal_item_predictions_dict if self.company_internal_item_predictions_dict else ""}' \
                 + f'\tdate: {self.date if self.date else ""}' \
                 + f'\tlatest_date_published: {self.latest_date_published if self.latest_date_published else ""}' \
                 + f'\tsource_data_created_date: {self.source_data_created_date if self.source_data_created_date else ""}' \
                 + f'\tdomain_list: {self.domain_list}' \
                 + f'\tscraping_error_list: {self.scraping_error_list}'
        return string

    def __repr__(self):
        return self.__str__()
