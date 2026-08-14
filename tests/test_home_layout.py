import os
from typing import cast

import pytest
from PySide6.QtWidgets import QApplication, QSizePolicy, QVBoxLayout, QWidget
from sqlmodel import SQLModel, create_engine

from navfitx.db import add_fitrep_to_db
from navfitx.examples import build_validated_example_fitrep
from navfitx.gui.home import Home

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

HOME_PAGE_WINDOW_WIDTH = 1300
HOME_PAGE_WINDOW_HEIGHT = 800
NARROW_WINDOW_WIDTH = 500
NARROW_WINDOW_HEIGHT = 700
LAYOUT_TEST_WIDTH = 1000
LAYOUT_TEST_HEIGHT = 700
WIDE_TEST_WIDTH = 1100
WIDER_TEST_WIDTH = 1200
REPORT_LIST_MANUAL_NAME_COLUMN_WIDTH = 420
REPORT_LIST_FILL_TOLERANCE_PX = 5


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return cast(QApplication, app)


def test_report_list_has_layout_stretch_on_home_page(qapp: QApplication) -> None:
    home = Home()

    home_page = home.stack.widget(0)
    assert isinstance(home_page, QWidget)
    layout = home_page.layout()
    assert isinstance(layout, QVBoxLayout)
    report_list_index = layout.indexOf(home.reports_table)

    assert report_list_index >= 0
    assert layout.stretch(report_list_index) == 1


def test_report_list_fill_behavior_tracks_resize_with_no_database(qapp: QApplication) -> None:
    home = Home()
    home.db = None
    home.refresh_reports_table()

    home.resize(LAYOUT_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    home.show()
    qapp.processEvents()

    assert home.reports_table.rowCount() == 0

    initial_name_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)
    home.resize(WIDER_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    qapp.processEvents()
    resized_name_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)

    home_page = home.stack.widget(0)
    assert isinstance(home_page, QWidget)
    layout = home_page.layout()
    assert isinstance(layout, QVBoxLayout)
    report_list_index = layout.indexOf(home.reports_table)

    assert report_list_index >= 0
    assert layout.stretch(report_list_index) == 1
    assert resized_name_width != initial_name_width


def test_report_list_columns_fill_available_width_on_home_page(qapp: QApplication) -> None:
    home = Home()
    home.resize(HOME_PAGE_WINDOW_WIDTH, HOME_PAGE_WINDOW_HEIGHT)
    home.show()
    qapp.processEvents()

    total_column_width = sum(home.reports_table.columnWidth(i) for i in range(home.reports_table.columnCount()))
    viewport_width = home.reports_table.viewport().width()

    assert total_column_width >= viewport_width - REPORT_LIST_FILL_TOLERANCE_PX


def test_report_list_keeps_name_readable_with_horizontal_scroll_when_narrow(qapp: QApplication) -> None:
    home = Home()
    home.resize(NARROW_WINDOW_WIDTH, NARROW_WINDOW_HEIGHT)
    home.show()
    qapp.processEvents()

    assert home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN) >= Home.REPORT_LIST_MIN_NAME_COLUMN_WIDTH
    assert home.reports_table.horizontalScrollBar().maximum() > 0
    assert home.reports_table.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Expanding
    assert home.reports_table.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Expanding


def test_report_list_reflows_name_column_after_window_resize(qapp: QApplication) -> None:
    home = Home()
    home.resize(WIDE_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    home.show()
    qapp.processEvents()

    home.reports_table.setColumnWidth(Home.REPORT_LIST_NAME_COLUMN, REPORT_LIST_MANUAL_NAME_COLUMN_WIDTH)
    qapp.processEvents()

    manual_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)

    home.resize(WIDER_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    qapp.processEvents()

    reflowed_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)

    assert reflowed_width >= Home.REPORT_LIST_MIN_NAME_COLUMN_WIDTH
    assert reflowed_width != manual_width


def test_report_list_fill_behavior_tracks_resize_with_empty_database(qapp: QApplication, tmp_path) -> None:
    home = Home()
    db_path = tmp_path / "empty.db"
    engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(engine)
    home.db = db_path
    home.refresh_reports_table()

    home.resize(LAYOUT_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    home.show()
    qapp.processEvents()

    assert home.reports_table.rowCount() == 0

    initial_name_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)
    home.resize(WIDER_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    qapp.processEvents()
    resized_name_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)

    home_page = home.stack.widget(0)
    assert isinstance(home_page, QWidget)
    layout = home_page.layout()
    assert isinstance(layout, QVBoxLayout)
    report_list_index = layout.indexOf(home.reports_table)

    assert report_list_index >= 0
    assert layout.stretch(report_list_index) == 1
    assert resized_name_width != initial_name_width


def test_report_list_fill_behavior_tracks_resize_with_populated_database(qapp: QApplication, tmp_path) -> None:
    home = Home()
    db_path = tmp_path / "populated.db"
    engine = create_engine(f"sqlite:///{db_path}")
    SQLModel.metadata.create_all(engine)

    fitrep = build_validated_example_fitrep()
    add_fitrep_to_db(db_path, fitrep)

    home.db = db_path
    home.refresh_reports_table()

    home.resize(LAYOUT_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    home.show()
    qapp.processEvents()

    assert home.reports_table.rowCount() >= 1

    initial_name_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)
    home.resize(WIDER_TEST_WIDTH, LAYOUT_TEST_HEIGHT)
    qapp.processEvents()
    resized_name_width = home.reports_table.columnWidth(Home.REPORT_LIST_NAME_COLUMN)

    home_page = home.stack.widget(0)
    assert isinstance(home_page, QWidget)
    layout = home_page.layout()
    assert isinstance(layout, QVBoxLayout)
    report_list_index = layout.indexOf(home.reports_table)

    assert report_list_index >= 0
    assert layout.stretch(report_list_index) == 1
    assert resized_name_width != initial_name_width
