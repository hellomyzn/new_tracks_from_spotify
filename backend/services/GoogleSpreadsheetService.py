import gspread

from repositories.GoogleSpreadsheetRepository import GoogleSpreadsheetRepository

class GoogleSpreadsheetService(object):

    @classmethod
    def create_columns(cls, worksheet, columns):
        print('Create header on GSS')
        for i, column in enumerate(columns, start=1):
            worksheet.update_cell(1, i, column)

        return None


    @classmethod
    def is_not_columns(cls, worksheet):
        if worksheet.row_values(1) == []:
            return True
        else:
            return False


    @staticmethod
    def add_tracks(tracks: list, google_spreadsheet) -> None:
        # If the spreadsheet is empty, Add column on header(from (1,1))
        if GoogleSpreadsheetService.is_not_columns(google_spreadsheet.worksheet):
            GoogleSpreadsheetService.create_columns(google_spreadsheet.worksheet, google_spreadsheet.columns)
            google_spreadsheet.next_row += 1

        for track in tracks:
            for i, column in enumerate(google_spreadsheet.columns, start=1):
                try:
                    GoogleSpreadsheetRepository.add(google_spreadsheet, i, column, track)
                except gspread.exceptions.APIError:
                    print("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
                    break

            google_spreadsheet.next_row += 1
        