import sys
sys.path.append('./scraping')
sys.path.append('./database')
sys.path.append('./assets')
from Wuzzuf import WUZZUF
import pickle
import os
import pdfplumber
import re
from DB import PostgreSQLConnection





class CVMATCHER:
    def __init__(self):
        current_path = os.getcwd()
        self.file_path = os.path.abspath(os.path.join(current_path,'assets', 'skills.pkl'))
        print('how'*100)
        print(self.file_path)
        print('how'*100)
        # self.file_path = r'/assets/skills.pkl'
        self.skills = self.get_skills()
        self.skills_pattern = self.skills_pattern_creator(self.skills)
        
    
    def skills_file_creator(self): ## creat skills file if not exists by scraping skills from wuzzuf jobs
        wuzzuf = WUZZUF()
        wuzzuf.wuzzufRunner(job_name='data analysis',n_scraping_pages=1,dbg=False)
        skills = wuzzuf.get_skills()
        unique_skills = set()
        for i in skills:
            for skill in i:
                unique_skills.add(skill)
        unique_skills = list(unique_skills)
        
        
        with open(self.file_path,'wb') as file:
            pickle.dump(unique_skills,file)
    
    def get_skills(self): ## update skills variable using skills got from scraped file
        
        if not os.path.exists(self.file_path):
            print('wait creating skills file ....')
            self.skills_file_creator()
            
        
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as file:
                loaded_skills = pickle.load(file)
            print('loaded....')
        else:
            print(f'file not exiists {self.file_path}')
        
        return loaded_skills
            
    
    def skills_pattern_creator(self,skills):
        strat_string = '(?i)[^\w]('
        end_string = ')(?![\w])'
        delimiter = '|'
        result_string = delimiter.join(skills)
        skills_to_match = strat_string + result_string + end_string
        return skills_to_match
    
    
    
    def skills_extractor_from_pdf(self,pdf_path):
        matched_skills = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                skills = re.findall(pattern=self.skills_pattern,string=text)
                for i in skills:
                    matched_skills.append(i[0].lower())
                    
        return list(set(matched_skills))
    
    
    def get_matched_jobs(self,user_skills):

        query = """
        WITH SkillMatches AS (
        SELECT j.id, j.job_title, j.job_description, s.skill
        FROM job j
        LEFT JOIN (
            SELECT id, unnest(REGEXP_MATCHES(job_description, %s, 'g')) AS skill
            FROM job
        ) s
        ON j.id = s.id
        )
        SELECT j.id, j.job_title, j.job_description, COUNT(DISTINCT LOWER(s.skill)) AS unique_skill_count
        FROM job j
        LEFT JOIN SkillMatches s ON j.id = s.id
        GROUP BY j.id, j.job_title, j.job_description
        HAVING COUNT(DISTINCT s.skill) > 0
        ORDER BY unique_skill_count DESC;
        """

        user_skills_pattern = self.skills_pattern_creator(user_skills)



        with PostgreSQLConnection() as con:            
            jobs = con.execute_query(query, (user_skills_pattern,))
        return jobs
    