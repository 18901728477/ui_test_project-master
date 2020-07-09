from pathlib import Path

p = Path()
current = p.resolve()
mobile_root = current.parent

ITEM_ROOT = mobile_root / "mitem_ui_test" / "mitem_ui_test"
TRADE_ROOT =  mobile_root / "mtrade_ui_test" / "mtrade_ui_test"
# test_file = ITEM_ROOT / "README.md"
# with test_file.open('r') as r:
#     print(r.read())
mobile_report = mobile_root / "reports"
ITEM_REPORT = mobile_report / "item"
TRADE_REPORT = mobile_report / "trade"
CONFIG = mobile_root / "config"


if __name__ == '__main__':
    print(TRADE_REPORT)