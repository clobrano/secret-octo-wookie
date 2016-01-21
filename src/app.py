from flask import Flask
from flask import render_template
from src.models.reports.report import Report
from src.models.reports.errors import EmptyReportException
from src.common.utils import get_entries


datafile = 'data.json'

app = Flask(__name__)
app.secret_key = '123'
entries = get_entries(datafile)

years = set()
dates = set()
for e in entries:
    tmp_date = "%04d/%02d" % (e.date.tm_year, e.date.tm_mon)
    years.add(e.date.tm_year)
    dates.add(tmp_date)

years = sorted(list(years), reverse=True)
dates = sorted(list(dates), reverse=True)

year_reports = [Report(year=year, entries=entries).json() for year in years]


@app.route("/report")
def index():
    return render_template('index.html', years=list(years),
                           reports=year_reports)


@app.route("/report/<string:year>/<string:month>", methods=['GET'])
def monthly_report(year, month):
    year = int(year)
    month = int(month)
    try:
        report = Report(year=year, month=month, entries=entries)
        if month > 1:
            ref = Report(year=year, month=month-1, entries=entries)
        else:
            ref = Report(year=int(year)-1, month=12, entries=entries)
        report.compare_categories(ref)
        data = report.json()
        data['dates'] = [date for date in dates if '%s' % year in date]
        return render_template('report.html', **data)
    except EmptyReportException:
        return render_template('report.html',
                               year=year,
                               month=month,
                               error=True,
                               error_message="No data for %02d/%04d" %
                               (month, year))
