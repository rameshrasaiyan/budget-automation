from amazon_bot import AmazonBot
from email_alert import EmailAlert
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class PriceUpdater(object):

    def __init__(self, spreadsheet_name):

        self.item_col = 1
        self.price_col = 2
        self.frequency_col = 3
        self.url_col = 4
        self.product_name_col = 5

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name('clients-secret.json', scope)

        client = gspread.authorize(creds)

        self.sheet = client.open(spreadsheet_name).sheet1

    def process_item_list(self):
        items = self.sheet.col_values(self.item_col)[1:]

        amazon_bot = AmazonBot(items)
        prices, urls, names = amazon_bot.search_items()

        print("Updating Spreadsheet")
        for i in range(len(prices)):
            self.sheet.update_cell(i+2, self.price_col, prices[i])
            self.sheet.update_cell(i+2, self.url_col, urls[i])
            self.sheet.update_cell(i+2, self.product_name_col, names[i])


price_updater = PriceUpdater("ProductPrice")
price_updater.process_item_list()

email = EmailAlert("Google Sheets Updated", "This is a message to let you know that the spreadsheet has been updated")
email.send_email()
