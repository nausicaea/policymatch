# -*- coding: utf-8 -*-

import regex as re


class PolicyMatcher(object):
    """
    Define a password policy and perform validation of masks.
    """
    _lower_re = re.compile(r"\?[al]|[^?]\p{Ll}")
    _upper_re = re.compile(r"\?[au]|[^?]\p{Lu}")
    _digit_re = re.compile(r"\?[ad]|[^?]\p{N}")
    _special_re = re.compile(r"\?[as?]|[^?][!\"#$%&'()*+,-./:;<=>@[\]^_`{|}~]")

    def __init__(self, min_lower, max_lower, min_upper, max_upper, min_digit, max_digit,
                 min_special, max_special, min_length, max_length):
        self.min_lower = min_lower
        self.max_lower = max_lower
        self.min_upper = min_upper
        self.max_upper = max_upper
        self.min_digit = min_digit
        self.max_digit = max_digit
        self.min_special = min_special
        self.max_special = max_special
        self.min_length = min_length
        self.max_length = max_length

    def _is_compliant(self, mask):
        """
        Returns True if the supplied mask is compliant with the specified policy.

        :param mask:
        :return:
        """
        reduced_mask = mask.replace("?", "")

        length_match = len(reduced_mask)
        lower_match = len(self._lower_re.findall(mask))
        upper_match = len(self._upper_re.findall(mask))
        digit_match = len(self._digit_re.findall(mask))
        special_match = len(self._special_re.findall(mask))

        if self.max_length < 0:
            length = self.min_length <= length_match
        else:
            length = self.min_length <= length_match <= self.max_length

        if self.max_lower < 0:
            lower = self.min_lower <= lower_match
        else:
            lower = self.min_lower <= lower_match <= self.max_lower

        if self.max_upper < 0:
            upper = self.min_upper <= upper_match
        else:
            upper = self.min_upper <= upper_match <= self.max_upper

        if self.max_digit < 0:
            digit = self.min_digit <= digit_match
        else:
            digit = self.min_digit <= digit_match <= self.max_digit

        if self.max_special < 0:
            special = self.min_special <= special_match
        else:
            special = self.min_special <= special_match <= self.max_special

        return length and lower and upper and digit and special

    def get_compliant(self, masks):
        """
        Yield all compliant masks from the original set of masks.

        :param masks:
        :return:
        """
        for m in masks:
            if self._is_compliant(m):
                yield m