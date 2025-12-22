# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from textwrap import dedent
from unittest.mock import call, mock_open

import pytest

from . import load_from_sbin

CONFIG_FILE_PATH = '/etc/odbcinst.ini'


@pytest.fixture
def update_odbcinst_config():
    yield load_from_sbin('xivo-update-odbcinst-config')


def test_unmodified(update_odbcinst_config):
    config = """
        [xivo]
        Description = Connection to the database used by Wazo
    """
    update_odbcinst_config.open = mock_open(read_data=dedent(config))
    update_odbcinst_config.main()
    update_odbcinst_config.open.assert_called_once_with(CONFIG_FILE_PATH)


def test_modified_comm_log(update_odbcinst_config):
    config = """
        [PostgreSQL ANSI]
        CommLog = 1
    """
    update_odbcinst_config.open = mock_open(read_data=dedent(config))
    update_odbcinst_config.main()
    update_odbcinst_config.open.assert_has_calls(
        [
            call(CONFIG_FILE_PATH),
            call().__enter__(),
            call().__getattr__('__iter__')(),
            call().__exit__(None, None, None),
            call(CONFIG_FILE_PATH, 'w'),
            call().__enter__(),
            call().write('[PostgreSQL ANSI]\n'),
            call().write('CommLog = 0\n'),
            call().write('\n'),
            call().__exit__(None, None, None),
        ]
    )
