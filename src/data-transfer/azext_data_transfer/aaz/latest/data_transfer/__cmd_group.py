# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command_group(
    "data-transfer",
    is_preview=True,
)
class __CMDGroup(AAZCommandGroup):
    """Commands for cross domain Service that enables customers to transfer data across security domains.
    """
    pass


__all__ = ["__CMDGroup"]
