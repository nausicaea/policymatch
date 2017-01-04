# -*- coding: utf-8 -*-

import attr
from attr.validators import instance_of
import regex as re


@attr.s
class PolicyMatcher(object):
    """
    Define a password policy and perform validation of masks.
    """
    min_lower = attr.ib(default=0, validator=instance_of(int))
    max_lower = attr.ib(default=-1, validator=instance_of(int))
    min_upper = attr.ib(default=0, validator=instance_of(int))
    max_upper = attr.ib(default=-1, validator=instance_of(int))
    min_digit = attr.ib(default=0, validator=instance_of(int))
    max_digit = attr.ib(default=-1, validator=instance_of(int))
    min_special = attr.ib(default=0, validator=instance_of(int))
    max_special = attr.ib(default=-1, validator=instance_of(int))
    min_length = attr.ib(default=0, validator=instance_of(int))
    max_length = attr.ib(default=-1, validator=instance_of(int))

    # FIXME: The compliance checker currently ignores '?a'
    _lower_re = re.compile(r"\?l|[^?]\p{Ll}")
    _upper_re = re.compile(r"\?u|[^?]\p{Lu}")
    _digit_re = re.compile(r"\?d|[^?]\p{N}")
    _special_re = re.compile(r"\?[s?]|[^?][!\"#$%&'()*+,-./:;<=>@[\]^_`{|}~]")

    def _is_compliant(self, mask):
        """
        Returns True if the supplied mask is compliant with the specified policy.

        :param mask:
        :return:
        """
        length_match = len(mask.replace("?", ""))
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
