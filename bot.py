import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup
import urllib

class SemRush:
    def __init__(self, filter_links: list):
        self.filter_list = filter_links
        self.item_list = []
        
    def get_agency_link(self):
        session = cloudscraper.create_scraper()
        for link in self.filter_list:
            print(f'Filter link: {link}')
            page = 0
            while True:
                page += 1
                resp = session.get(f'{link}&page={page}')
                print(f'Page {page}')
                soup = BeautifulSoup(resp.text, 'lxml')
                link_htmls = soup.select('._2_C2MX2f')
                agency_links = [urllib.parse.urljoin('https://www.semrush.com', l['href']) for l in link_htmls]
                if len(agency_links) < 1:
                    print('No more new pages')
                    break
                else:
                    self.get_data(agency_links)
                
    def get_data(self, agency_links):
        session = cloudscraper.create_scraper()
        for link in agency_links:
            print(f'Agency: {link}')
            resp = session.get(link)
            soup = BeautifulSoup(resp.text, 'lxml')
            try:
                agency_link = soup.select_one('.GaPlz6OV a')['href']
            except:
                agency_link = None
            try:
                agency_name = soup.select_one('h1').get_text(strip=True)
            except:
                agency_name = None
            try:
                agency_budget = soup.select_one('.RrpCHeFe').get_text(strip=True)
            except:
                agency_budget = None
            try:
                agency_details = soup.select('._2dIJTecQ')
                agency_address = agency_details[0].get_text(strip=True)
                agency_employee = agency_details[1].get_text(strip=True)
                agency_founded = agency_details[2].get_text(strip=True)
            except:
                agency_address = None
                agency_employee = None
                agency_founded = None
            item = {
                'Company name': agency_name,
                'Domain': agency_link,
                'Revenue range': agency_budget,
                'HQ Address': agency_address,
                'Phone number': None,
                '# of Employees': agency_employee,
                'Year founded': agency_founded
            }
            self.item_list.append(item)
            
    def save_data(self):
        df = pd.DataFrame(self.item_list)
        df.drop_duplicates(subset=['Company name'], inplace=True)
        df.to_csv('semrush_agency_data.csv', index=False)
        print(f'Length of data: {len(df)}')
      
    def main(self):
        self.get_agency_link()
        self.save_data()
   
if __name__ == '__main__':
    semrush = SemRush([
        'https://www.semrush.com/agencies/list/?services=42%2C30%2C28%2C23%2C24&industries=36%2C14%2C16%2C24%2C26%2C31%2C35%2C21%2C2%2C6%2C8%2C10%2C19%2C13%2C1%2C5%2C17%2C3%2C29%2C32%2C33%2C34%2C4%2C25%2C12%2C15%2C22%2C27%2C11%2C20%2C23&businessSizes=2',
        'https://www.semrush.com/agencies/list/?services=42%2C30%2C28%2C23%2C24&industries=36%2C14%2C16%2C24%2C26%2C31%2C35%2C21%2C2%2C6%2C8%2C10%2C19%2C13%2C1%2C5%2C17%2C3%2C29%2C32%2C33%2C34%2C4%2C25%2C12%2C15%2C22%2C27%2C11%2C20%2C23&businessSizes=3'
    ])
    semrush.main()  
            