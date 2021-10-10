import pytest
import sys
import coverage
import shutil
from pathlib import Path

shutil.rmtree(Path(__file__).parents[0] / "htmlcov", ignore_errors=True)
cov = coverage.Coverage(concurrency=["greenlet"])
cov.start()
return_code = pytest.main([str(Path(__file__).parents[0] / "tests")])
cov.stop()
cov.report()
cov.html_report()

sys.exit(return_code)
