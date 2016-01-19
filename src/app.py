from flask import Flask
from flask import render_template
from src.models.reports.report import Report
from src.models.entries.constants import AMOUNT_COL
from src.models.entries.constants import DESCRIPTION_COL
from src.models.entries.constants import DATE_COL
from src.models.entries.constants import OUTCOME_COL
from src.models.entries.constants import CATEGORY_COL
from src.common.utils import parse_cvs
from src.common.utils import update_json
from src.common.utils import get_entries


datafile = 'data.json'

app = Flask(__name__)
# TODO: set real key
app.secret_key = '123'

entries = get_entries(datafile)


def update_database(cvs_filename, json_datafile):
    entries = parse_cvs(cvs_filename,
                        AMOUNT_COL,
                        DESCRIPTION_COL,
                        DATE_COL,
                        OUTCOME_COL,
                        CATEGORY_COL)

    update_json(datafile, entries)


@app.route("/report/<string:year>/<string:month>")
def monthly_report(year, month):
    year = int(year)
    month = int(month)
    report = Report(year=year, month=month, entries=entries)
    if month > 1:
        ref = Report(year=year, month=month-1, entries=entries)
    else:
        ref = Report(year=int(year)-1, month=12, entries=entries)
    report.compare_categories(ref)
    data = report.json()
    return render_template('report.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
