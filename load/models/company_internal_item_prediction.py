from typing import Optional


class CompanyInternalItemPrediction:
    criterion_name: Optional[str]
    labeled_probabilities: Optional[dict]
    criterion_value_label: Optional[str]
    raw_criterion_value_number: Optional[int]
    raw_probability_values: Optional[list]

    def __init__(
            self,
            criterion_name: Optional[str] = '',
            labeled_probabilities: Optional[dict] = None,
            criterion_value_label: Optional[str] = '',
            raw_criterion_value_number: Optional[int] = 0,
            raw_probability_values: Optional[list] = None
    ):
        self.criterion_name = criterion_name
        self.labeled_probabilities = labeled_probabilities if labeled_probabilities else {}
        self.criterion_value_label = criterion_value_label
        self.raw_criterion_value_number = raw_criterion_value_number
        self.raw_probability_values = raw_probability_values if raw_probability_values else []

    @classmethod
    def from_dict(cls, company_internal_item_prediction_dict):
        return cls(
            criterion_name=company_internal_item_prediction_dict.get('criterion_name', ""),
            labeled_probabilities=company_internal_item_prediction_dict.get('label_probabilities', ""),
            criterion_value_label=company_internal_item_prediction_dict.get('criterion_value_label', ""),
            raw_criterion_value_number=company_internal_item_prediction_dict.get('raw_criterion_value_number', ""),
            raw_probability_values=company_internal_item_prediction_dict.get('raw_probability_values', "")
        )

    def to_dict(self):
        print('type criterion ', type(self.criterion_name))
        print('type labeled_probabilities ', type(self.labeled_probabilities))
        print('type current_label ', type(self.criterion_value_label))

        dict_value = {'criterion_name': self.criterion_name,
                      'labeled_probabilities': self.labeled_probabilities,
                      'criterion_value_label': self.criterion_value_label,
                      'raw_criterion_value_number': self.raw_criterion_value_number,
                      'raw_probability_values': self.raw_probability_values}
        return dict(dict_value)

    def __str__(self):
        string = f'\tcriterion: {self.criterion_name if self.criterion_name else ""}' \
                 + f'\tlabeled_probabilities: {self.labeled_probabilities if self.labeled_probabilities else ""}' \
                 + f'\tcurrent_label: {self.criterion_value_label if self.criterion_value_label else ""}' \
                 + f'\traw_criterion_value_number: {self.raw_criterion_value_number if self.raw_criterion_value_number else ""}' \
                 + f'\traw_probability_values: {self.raw_probability_values if self.raw_probability_values else ""}'
        return string

    def __repr__(self):
        return self.__str__()
