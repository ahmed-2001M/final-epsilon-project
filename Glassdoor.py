from Driver import DRIVER
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from DB import PostgreSQLConnection
import re



class GLASSDOOR(DRIVER):
    def __init__(self):
        self.glassdoor_link = 'https://www.glassdoor.sg/Job/index.htm'
        self.company_block_xpath = "//div[@class='JobDetails_jobDetailsContainer__sS1W1']/section/section"
        self.google_popup_xpath = "//body[@class='qJTHM']/div/div/div/div[@id='picker-header']/div[@id='close']"
        self.most_recent_jobs_button_xpath = "//div[@class='SearchFiltersBar_filterLabel__jFhCl SearchFiltersBar_pill__sShgh SearchFiltersBar_pillNoBackground__SLUgI SearchFiltersBar_active__w87nv']\
                                        /button[@class='SearchFiltersBar_labelButton__yhx4z SearchFiltersBar_pillLeft__KLiVw']"
        self.login_popup_xpath = "//div[@class='actionBarMt0   css-gss116 e1jtvglp0']/button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']"
        self.jobs_number_xpath = "//div[@class='SearchResultsHeader_searchResultsHeader__jEUWz']/h1[@class='SearchResultsHeader_jobCount__12dWB']"
        self.jobs_cards_xpath = "//div[@class='d-flex justify-content-between p-std jobCard ']"
        self.company_name_xpath = ".//div/div[@class='css-gx72iw']/div[@class='css-8wag7x']"
        self.company_name_if_no_logo_xpath = ".//div/div[@class='css-gx72iw']"
        self.job_title_xpath = ".//div/a"
        self.salary_xpath = ".//div/div[@class='salary-estimate']"
        self.location_xpath = ".//div/div[@class='location mt-xxsm']"
        self.company_block_info_xpath = ".//div/div/div"
        self.job_description_xpath = ".//div[@class='JobDetails_jobDescriptionWrapper__BTDTA']"
        self.show_more_job_descritpion_button_xpath = "//div[@class='JobDetails_showMoreWrapper__I6uBt']/button"
        self.show_more_button_xpath = "//div[@class='JobsList_buttonWrapper__haBp5']/button"
        self.connection = PostgreSQLConnection(host='172.17.0.2',database='work',user='postgres',password='123')
        self.connection.connect()
    
    def searchByJobTitle(self, title,location):
        search_bar = self.driver.find_element(By.ID,'searchBar-jobTitle')
        location_bar = self.driver.find_element(By.ID,'searchBar-location')
        search_bar.send_keys(title)
        if location:
            location_bar.send_keys(location)
        search_bar.send_keys(Keys.ENTER)
    
    def closePopup(self):
        self.waitElementLoad(xpath=self.google_popup_xpath,timeout=5).click()
    
    def clickOnMostResentJobs(self):
        self.waitElementLoad(xpath=self.most_recent_jobs_button_xpath,timeout=5).click()
    
    def CloseLoginPopup(self):
        self.waitElementLoad(xpath=self.login_popup_xpath,timeout=5).click()
    
    
    def getJobTitle(self,job_card=None):
        try:
            if job_card:
                job_titile = self.waitElementLoad(card=job_card, xpath=self.job_title_xpath, timeout=5).text
            else:
                job_titile = self.waitElementLoad(xpath=self.job_title_xpath, timeout=5).text
            return job_titile
        except:
            print('not found')
    
    
    def companyNameTransformer(self,company_name:str):
        if company_name[-1] == '★':
            if company_name[-5].isdigit():
                name = company_name[:-5]
                stars_number = float(company_name[-5:-1].strip())
            elif company_name[-4].isdigit():
                name = company_name[:-4]
                stars_number = float(company_name[-4:-1].strip())
            else:
                name = company_name[:-3]
                stars_number = float(company_name[-3:-1].strip())
                
                
            return (name, stars_number)
        else:
            return (company_name, 0)
    
    def getCompanyName(self, job_card=None):
        try:
            if job_card:
                company_name = self.waitElementLoad(card=job_card, xpath=self.company_name_xpath, timeout=5).text
            else:
                company_name = self.waitElementLoad(xpath=self.company_name_xpath, timeout=5).text
            return self.companyNameTransformer(company_name)
        except:
            try:
                if job_card:
                        company_name = self.waitElementLoad(card=job_card, xpath=self.company_name_if_no_logo_xpath, timeout=5).text
                else:
                    company_name = self.waitElementLoad(xpath=self.company_name_if_no_logo_xpath, timeout=5).text
                return self.companyNameTransformer(company_name)
            except:
                print('not found')
    
    def clickShowMoreJobs(self):
        try:
            self.waitElementLoad(xpath=self.show_more_button_xpath,timeout=5).click()
        except:

            try:
                element = self.driver.find_element(By.XPATH, self.login_popup_xpath)
                if not element:
                    element = self.waitElementLoad(By.XPATH,"//span[@alt='Close']",timeout=5)
                    element.click()
                elif not element:
                    element = self.waitElementLoad(".//button[@class='CloseButton']")
                    element.click()
                
                print('popup closed')
            except Exception as e:
                print(f"clickShowMoreJobs // An error occurred: {str(e)}")
                return None
            

    def getJobsNumber(self):
        jobs_number = int(self.waitElementLoad(xpath=self.jobs_number_xpath,timeout=5).text.split(' ')[0].replace(',',''))
        return jobs_number

    def calculateNumberOfPages(self):
        jobs_number = self.getJobsNumber()
        jobs_displayed_in_one_page = 20
        number_of_pages = ((jobs_number+1)//jobs_displayed_in_one_page)
        return number_of_pages
        





    def extract_salary_range(self, salary):
        # Extract numeric values and units using regular expressions
        try:
            matches = re.findall(r'\$?(\d+(?:\.\d+)?)([KkMmBb]{0,1})', salary)
            
            min_salary = None
            max_salary = None

            for match in matches:
                value = float(match[0])
                unit = match[1].lower()

                if unit == 'k':
                    value *= 1000
                elif unit == 'm':
                    value *= 1000000

                if min_salary is None:
                    min_salary = value
                elif max_salary is None:
                    max_salary = value
                    break

            return min_salary, max_salary
        except:
            return salary



    def getSalary(self,job_card):
        try:
            if job_card:
                salary = job_card.find_element(By.XPATH,self.salary_xpath).text
            else:
                salary = self.waitElementLoad(xpath=self.salary_xpath,timeout=5).text
            return self.extract_salary_range(salary)
        except NoSuchElementException:
            print('getSalary // element not found')
            return (None,None)
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getSalary // An error occurred: {str(e)}")
            return (None,None)
    
    def getLocation(self,job_card):
        try:
            if job_card:
                location = job_card.find_element(By.XPATH,self.location_xpath).text
            else:
                location = self.waitElementLoad(xpath=self.location_xpath,timeout=5).text
            return location
        except NoSuchElementException:
            print('getLocation // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getLocation // An error occurred: {str(e)}")
            return None
    
    
    
    def getCompanyBlock(self,idx):
        self.waitElementLoad(xpath=self.company_block_xpath,timeout=20)
        try:
            elements = self.driver.find_elements(By.XPATH,self.company_block_xpath)
            return elements[idx]
        except NoSuchElementException:
            print('getCompanyBlock // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanyBlock // An error occurred: {str(e)}")
            return None
    
    
    
    
    def CompanySizeTransformer(self,company_size):
        size_parts = company_size.split()[0]
        if '+' in size_parts:
            size_parts = size_parts.replace('+', '')
        
        if 'to' in size_parts:
            first = int(size_parts.split('to')[0])
            second = int(size_parts.split('to')[1])
            size_parts = (first+second) / 2
        
        return int(size_parts)
    
    
    def getCompanySize(self, company_block):
        try:
            if company_block:
                size = company_block.find_elements(By.XPATH,self.company_block_info_xpath)[0].text
            else:
                size = self.driver.find_elements(By.XPATH,self.company_block_info_xpath)[0].text
            return self.CompanySizeTransformer(size)
        except NoSuchElementException:
            print('getCompanySize // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanySize // An error occurred: {str(e)}")
            return None

    def getCompanyFound(self , company_block):
        try:
            if company_block:
                found = company_block.find_elements(By.XPATH,self.company_block_info_xpath)[1].text
            else:
                found = self.driver.find_elements(By.XPATH,self.company_block_info_xpath)[1].text
            return found
        except NoSuchElementException:
            print('getCompanyFound // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanyFound // An error occurred: {str(e)}")
            return None

    def getCompanyType(self , company_block):
        try:
            if company_block:
                type = company_block.find_elements(By.XPATH,self.company_block_info_xpath)[2].text
            else:
                type = self.driver.find_elements(By.XPATH,self.company_block_info_xpath)[2].text
            return type
        except NoSuchElementException:
            print('getCompanyType // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanyType // An error occurred: {str(e)}")
            return None




    def getCompanyIndustry(self , company_block):
        try:
            if company_block:
                industry = company_block.find_elements(By.XPATH,self.company_block_info_xpath)[3].text
            else:
                industry = self.driver.find_elements(By.XPATH,self.company_block_info_xpath)[3].text
            return industry
        except NoSuchElementException:
            print('getCompanyIndustry // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanyIndustry // An error occurred: {str(e)}")
            return None


    def getCompanySector(self , company_block):
        try:
            if company_block:
                sector = company_block.find_elements(By.XPATH,self.company_block_info_xpath)[4].text
            else:
                sector = self.driver.find_elements(By.XPATH,self.company_block_info_xpath)[4].text
            return sector
        except NoSuchElementException:
            print('getCompanySector // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanySector // An error occurred: {str(e)}")
            return None





    def companyRevenueTransformer(self,revenue_str):
        match = re.search(r'\$([\d,.]+)\s*(?:\+\s*)?(billion|million)', revenue_str, re.IGNORECASE)

        if match:
            # Get the matched numeric parts for the range
            largest_match = match.group(1)

            # Remove commas and convert to integers
            largest_revenue = int(''.join(largest_match.split(',')))

            # Adjust for billion or million
            if 'billion' in revenue_str.lower():
                largest_revenue *= 1000000000
            elif 'million' in revenue_str.lower():
                largest_revenue *= 1000000

            return largest_revenue
                
        return 0 
        
        



    def getCompanyRevenue(self, company_block):
        try:
            if company_block:
                revenue = company_block.find_elements(By.XPATH,self.company_block_info_xpath)[5].text
            else:
                revenue = self.driver.find_elements(By.XPATH,self.company_block_info_xpath)[5].text
            return self.companyRevenueTransformer(revenue)
        except NoSuchElementException:
            print('getCompanyRevenue // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getCompanyRevenue // An error occurred: {str(e)}")
            return None
    
    
    def getJobDescription(self):
        try:
            res = self.driver.find_element(By.XPATH, self.job_description_xpath).text
            return res
        except NoSuchElementException:
            print('getJobDescription // element not found')
            return None
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"getJobDescription // An error occurred: {str(e)}")
            return None
    
    def clickOnShowMoreJobDescription(self):
        try:
            self.waitElementLoad(xpath=self.show_more_job_descritpion_button_xpath,timeout=5).click()
        except:
            try:
                self.driver.find_element(By.XPATH, self.login_popup_xpath).click()
                print('popup closed')
            except Exception as e:
                print(f"clickOnShowMoreJobDescription // An error occurred: {str(e)}")
                return None



    def scrapData(self):
        # Create empty lists to store data
        company_names = []
        stars_numbers = []
        job_titles = []
        salaries = []
        locations = []
        jobs_descriptions = []
        companys_sizes = []
        companys_found = []
        companys_types = []
        companys_industrys = []
        companys_sectors = []
        companys_revenues = []
        
        
        
        self.waitElementLoad(xpath=self.jobs_cards_xpath, timeout=5)
        jobs_cards = self.driver.find_elements(By.XPATH, self.jobs_cards_xpath)
        c=1
        for job_card in jobs_cards:
            
            try:
                job_card.click()
                print('Clicked')
            except Exception as e:
                try:
                    self.CloseLoginPopup()
                    print('popup closed')
                except:
                    print('not found after check popup')

            company_name, stars_number = self.getCompanyName(job_card=job_card)
            job_title = self.getJobTitle(job_card=job_card)
            min_salary, max_salary = self.getSalary(job_card=job_card)
            location = self.getLocation(job_card=job_card)
            self.clickOnShowMoreJobDescription()
            job_description = self.getJobDescription()
            

            
            #Company section
            company_block_idx = 0
            # if min_salary:
            #     company_block_idx = 1
            
            try:
                company_block_element = self.getCompanyBlock(company_block_idx)
            except:
                try:
                    self.CloseLoginPopup()
                    print('popup closed')
                except:
                    print('not found after check popup')
            
            
            company_size = self.getCompanySize(company_block=company_block_element)
            company_founded = self.getCompanyFound(company_block=company_block_element)
            company_type = self.getCompanyType(company_block=company_block_element)
            company_industry = self.getCompanyIndustry(company_block=company_block_element)
            company_sector = self.getCompanySector(company_block=company_block_element)
            company_revenue = self.getCompanyRevenue(company_block=company_block_element)
            #---------------
            
            
            
            print(50*'%')
            print(c)
            print('____')
            print(f'company_name   ===> {company_name}')
            print(f'stars_number   ===> {stars_number}')
            print(f'job_title     ====>{job_title}')
            print(f'location   ====>{location}')
            print(f'salary   ====> {min_salary} - {max_salary}')
            print('____________________')
            print(f'company_size    ====>{company_size}')
            print(f'company_founded    ====>{company_founded}')
            print(f'company_type   ====> {company_type}')
            print(f'company_industry   ====>{company_industry}')
            print(f'company_sector   ====> {company_sector}')
            print(f'company_revenue ====> {company_revenue}')
            print('____________________')
            print(50*'%')

            
            
            # Append data to lists
            company_names.append(company_name)
            stars_numbers.append(stars_number)
            job_titles.append(job_title)
            # salaries.append(salary)
            locations.append(location)
            jobs_descriptions.append(job_description)
            companys_sizes.append(company_size)
            companys_found.append(str(company_founded))
            companys_types.append(company_type)
            companys_industrys.append(company_industry)
            companys_sectors.append(company_sector)
            companys_revenues.append(company_revenue)
            
            if job_description:
                id = self.hashing(job_description)
                insert_query = """
                                INSERT INTO job
                                (id, job_titile, job_location, job_description, company_name, stars, company_size, company_founde, company_type, company_industry, company_sector, company_revenue, min_salary, max_salary) 
                                SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s
                                WHERE NOT EXISTS (
                                    SELECT 1 FROM job WHERE id = %s
                                );
                            """
                self.connection.execute_insert(insert_query, [(id, job_title, location, job_description, company_name, stars_number, company_size, company_founded, company_type, company_industry, company_sector, company_revenue, min_salary, max_salary, id)])
                
            
            c+=1


    def scrapAllTabs(self):
        
        number_of_pages = self.calculateNumberOfPages()
        print(f'Number of pages =============> {number_of_pages}')
        for i in range(40):
            print(f'page {i} opened......')
            self.clickShowMoreJobs()
            time.sleep(3)

        self.scrapData()
