import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('GoogleSheet-a6cf88e67d67.json', scope)
gss_client = gspread.authorize(credentials)
feed = gss_client.open_by_url('https://docs.google.com/spreadsheets/d/1M6VrPwpK2vcpnKYDFiLAaofkdBdhq8yF5SPp6_7AgfQ/edit#gid=619620803')
print dir(feed)
print feed.title

wk = feed.get_worksheet(0)
print wk.get_all_records()