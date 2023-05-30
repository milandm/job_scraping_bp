from typing import Optional
from load.models.company_internal_item_prediction import CompanyInternalItemPrediction
from utils.utils import get_bucket_path_list_from_string


class CompanyInternalItem:
    full_web_address: Optional[str]
    base_web_address: Optional[str]
    bucket_name: Optional[str]
    bucket_path_list: list
    company_name: Optional[str]
    language: Optional[str]
    company_internal_item_predictions_dict: Optional[dict]

    def __init__(
            self,
            full_web_address: Optional[str] = '',
            base_web_address: Optional[str] = '',
            bucket_name: Optional[str] = '',
            bucket_path_list: list = None,
            company_name: Optional[str] = '',
            language: Optional[str] = '',
            company_internal_item_predictions_dict: dict = None
    ):
        self.full_web_address = full_web_address
        self.base_web_address = base_web_address
        self.bucket_name = bucket_name
        self.bucket_path_list = bucket_path_list if bucket_path_list else []
        self.company_name = company_name
        self.language = language
        self.company_internal_item_predictions_dict = company_internal_item_predictions_dict if company_internal_item_predictions_dict else {}

    @classmethod
    def from_dict(cls, company_internal_item_dict, my_logger=None):
        bucket_path_list_str = company_internal_item_dict.get('bucket_path_list', [])
        bucket_path_list = get_bucket_path_list_from_string(my_logger, bucket_path_list_str)
        company_internal_item_predictions_dict = company_internal_item_dict.get(
            'company_internal_item_predictions_dict', None)
        object_company_internal_item_predictions_dict = dict()
        if company_internal_item_predictions_dict:
            object_company_internal_item_predictions_dict = {
                criterion_name: CompanyInternalItemPrediction.from_dict(jsonObjectCompany) for
                criterion_name, jsonObjectCompany in company_internal_item_predictions_dict.items()}
        return cls(
            full_web_address=company_internal_item_dict.get('full_web_address', ""),
            base_web_address=company_internal_item_dict.get('base_web_address', ""),
            bucket_name=company_internal_item_dict.get('bucket_name', ""),
            bucket_path_list=bucket_path_list,
            company_name=company_internal_item_dict.get('company_name', ""),
            language=company_internal_item_dict.get('language', ""),
            company_internal_item_predictions_dict=object_company_internal_item_predictions_dict)

    def to_dict(self):
        dict_value = {'full_web_address': self.full_web_address,
                      'base_web_address': self.base_web_address,
                      'bucket_name': self.bucket_name,
                      'bucket_path_list': self.bucket_path_list.__str__(),
                      'company_name': self.company_name,
                      'language': self.language,
                      'company_internal_item_predictions_dict': {
                          criterion: company_internal_item_prediction.to_dict()
                          for criterion, company_internal_item_prediction in (
                                  self.company_internal_item_predictions_dict or dict()).items()}
                      }
        return dict(dict_value)

    def __str__(self):
        string = f'\tfull_web_address: {self.full_web_address if self.full_web_address else ""}' \
                 + f'\tbase_web_address: {self.base_web_address if self.base_web_address else ""}' \
                 + f'\tbucket_name: {self.bucket_name if self.bucket_name else ""}' \
                 + f'\tbucket_path_list: {self.bucket_path_list if self.bucket_path_list else ""}' \
                 + f'\tcompany_name: {self.company_name if self.company_name else ""}' \
                 + f'\tlanguage: {self.language if self.language else ""}' \
                 + f'\tcompany_internal_item_predictions_dict: {(self.company_internal_item_predictions_dict if self.company_internal_item_predictions_dict else "")}'
        return string

    def __repr__(self):
        return self.__str__()
