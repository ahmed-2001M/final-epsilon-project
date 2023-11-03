# this is job recommender and job salary predictor project

### project demo
https://drive.google.com/file/d/1QFruj7afQMc6RC-DM_Z6H-uLqrlTgi06/view?usp=drive_link


### About Data
- Scraped Featers from glassdoor Site:


|    Column       |          Type           | 
| :---------------| :-----------------------|
|id               | character varying(255)  |
|job_titile       | character varying(50)   |
|job_location     | character varying(50)   |
|job_description  | character varying(9000) |
|company_name     | character varying(50)   |
|company_size     | integer                 |
|company_founde   | character varying(50)   |
|company_type     | character varying(50)   |
|company_industry | character varying(50)   |
|company_sector   | character varying(50)   |
|company_revenue  | character varying(50)   |
|stars            | integer                 |
|min_salary       | integer                 |
|max_salary       | integer                 |

- my aim is use this features for do job recommendtion system and salary predictor




# Project Structure
```
epsilon_project/
├── analysis/
|   ├── data_and_note_book_generator.ipynb          __use my library for generate analysis notebook__
|   ├── fun.ipynb                                   __analyize and visualize scraped data__
|   ├── utility.py                                  __have pipline function for new data__
│   └── ts.ipynb                                    __test pipline function__
├── data/
|   └── data.csv                                    __have scraped data from glassdoor__
├── database/
|   ├── d.sql
|   └──DB.py                                        __have database class for connection__
└── deployment/
|   └── landing_page.ipynb
└── scraping/
    ├── Driver.py
    ├── Glassdoor.py
    ├── Run.ipynb
```













# Analysis Notes

### From Info Function
- __Usless Columns__ : Unnamed: 0, id
- ##### Columns have nulls:
    - Unnamed: 0==> 0.06% 
    - job_titile==> 0.06% 
    - company_size==> 18.89% 
    - company_founde==> 38.09% 
    - company_type==> 9.79% 
    - company_industry==> 24.64% 
    - company_sector==> 14.91% 
    - company_revenue==> 51.17% 
    - stars==> 19.33% 
    - min_salary==> 15.1% 
    - max_salary==> 24.26% 
- __min_slary , max_salary__: have outliers 
- ___company_found___ have min value 3.5 it is not true value
