from Driver import DRIVER
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException



class WUZZUF(DRIVER):
    def __init__(self):
        self.wuzzuf_link = 'https://wuzzuf.net/jobs/egypt'
        self.date_validation = True
        self.search_bar_xpath = "//input[@class='search-bar-input']"
        self.job_link_xpath = ".//div/div/h2/a"
        self.title_xpath = "//div[@class='css-bjn8wh']/h1"
        self.date_xpath = ".//div[@class='css-4c4ojb']"
        self.type_xpath = "//div[@class='css-11rcwxl']/a/span"
        self.company_and_location_xpath = "//div[@class='css-bjn8wh']/strong[@class='css-9geu3q']"
        self.skills_xpath = "//section[@class='css-3kx5e2']/div[@class='css-s2o0yh']/a"
        self.experience_eduction_career_salary_xpath= "//section[@class='css-3kx5e2']/div[@class='css-rcl8e5']"
        self._scraped_data = []
    
    
    
    def _searchUsingJobName(self,job_name):
        search_bar = self.waitElementLoad(xpath=self.search_bar_xpath, timeout=10)
        search_bar.send_keys(job_name)
        
    
    def _clickSearchJobs(self):
        self.driver.find_element(By.CLASS_NAME, 'search-btn').click()
    
    def _getJobsDivs(self):
        jobs_divs = self.driver.find_elements(By.XPATH,"//div[@class='css-1gatmva e1v1l3u10']")
        return jobs_divs
    
    def _getJobTitle(self, div = None):
        try:
            if div:
                title = div.find_element(By.XPATH,self.title_xpath).text
            else:
                title = self.waitElementLoad(xpath=self.title_xpath,timeout=10).text
            return title
        except NoSuchElementException:
            print('getJobTitle // element not found')
            return None
        except Exception as e:
            print(f"getJobTitle // An error occurred: {str(e)}")
            return None

    def _getSkills(self, div = None):
        skills = []
        try:
            if div:
                skills_elements = div.find_elements(By.XPATH,self.skills_xpath)
            else:
                self.waitElementLoad(xpath=self.skills_xpath,timeout=10)
                skills_elements = self.driver.find_elements(By.XPATH, self.skills_xpath)
            
            for skill_element in skills_elements:
                skills.append(skill_element.text)
            return skills
        except NoSuchElementException:
            print('getSkills // element not found')
            return None
        except Exception as e:
            print(f"getSkills // An error occurred: {str(e)}")
            return None
    


    def _scrapData(self,dbg=False):
        time.sleep(5)
        self.waitElementLoad(xpath="//body",timeout=30)
        divs = self._getJobsDivs()
        original_tab_handle = self.driver.window_handles[0] 
        
        for div in divs:
            self.waitElementLoad(xpath=self.job_link_xpath,timeout=10)
            job_link = div.find_element(By.XPATH,self.job_link_xpath)

            self.clickLink(element=job_link)
            
            title = self._getJobTitle()
            
            
            skills = self._getSkills()
            self._scraped_data.append((title,skills))
            
            
            self.driver.close()  # Close the new tab
            self.driver.switch_to.window(original_tab_handle)
            

    def _scrapAllTabs(self,n_scraping_pages,dbg=False):
        c = 1
        while c <= n_scraping_pages:
            self.waitElementLoad(xpath="//body",timeout=30)
            if dbg == True:
                print(f'Scraping Page {c} ...')
            self._scrapData(print)
            try:
                self.driver.find_elements(By.XPATH,"//ul[@class='css-e5a93e']/li[@class='css-1q4vxyr']/button[@class='css-zye1os ezfki8j0']")[-1].click()
            except:
                break
            c+=1
        if dbg == True:
            print('ended....')
    
    
    
    
    
    
    def wuzzufRunner(self, job_name,n_scraping_pages,dbg=False):
        
        time.sleep(1)
        self.landFirstPage(self.wuzzuf_link)
        
        if job_name:
            time.sleep(1)
            self._searchUsingJobName(job_name)
        
        self._clickSearchJobs()
        
        time.sleep(2)
        self._scrapAllTabs(n_scraping_pages,dbg)
    
    
    def get_skills(self):
        skills = []
        if self._scraped_data:
            for _,skill in self._scraped_data:
                skills.append(skill)
        return skills
    def get_scraped_data(self):
        return self._scraped_data