
import sys
sys.path.append('./jobs_recomender')
sys.path.append('./analysis')

import pandas as pd
from utility import process_new
import numpy as np
import joblib
from Cv_matcher import CVMATCHER
import streamlit as st




model = joblib.load('./assets/linear_model.pkl')


def job_matcher(): ## will get top related 3 jobs not all jobs

    st.title("Job Recommender .....")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        cv_matcher = CVMATCHER()
        user_skills = cv_matcher.skills_extractor_from_pdf(
            pdf_path='./assets/Ahmed Abdallah (5).pdf')
        matched_jobs = cv_matcher.get_matched_jobs(user_skills)

        st.subheader("Matching Jobs")
        c = 0
        for job in matched_jobs:
            title = f"""## 👉 {job[1]}"""
            description = f"""#### Job Description:"""
            description_text = f"""{job[2]}"""

            st.markdown(title, unsafe_allow_html=True)
            st.markdown(description, unsafe_allow_html=True)
            st.markdown(description_text, unsafe_allow_html=True)
            st.markdown('------', unsafe_allow_html=True)

            c += 1
            if c == 3:
                break


def salary_prediction():
    st.title('Job Salary Prediction ......')
    st.markdown('<hr>', unsafe_allow_html=True)

    job_title = st.selectbox('job_title', options=[
                              'data analyst', 'data scientist'])
    job_description = st.text_area('description')
    company_size = st.number_input('Company Size')
    if company_size >=0 and company_size <= 500:
        company_size = 1
    elif company_size > 500 and company_size <= 1000:
        company_size = 2
    else:
        company_size = 3


    company_type = st.selectbox('company_type', options=['Company - Private', 'Company - Public',
                                                         'Subsidiary or Business Segment', 'Non-profit Organisation',
                                                         'Hospital', 'Contract', 'Government', 'Self-employed',
                                                         'Private Practice / Firm', 'College / University', 'Franchise',
                                                         'School / School District'])
    company_industry = st.selectbox('company industry', options=['Sporting Goods Stores', 'Other Retail Shops',
                                                                 'Enterprise Software & Network Solutions',
                                                                 'Catering & Food Service Contractors',
                                                                 'Information Technology Support Services', 'Insurance Carriers',
                                                                 'Healthcare Services & Hospitals',
                                                                 'Airlines, Airports & Air Transportation', 'HR Consulting',
                                                                 'Sports & Recreation', 'Advertising & Public Relations',
                                                                 'Civic, Welfare & Social Services', 'Banking & Lending',
                                                                 'Cable, Internet & Telephone Providers', 'Grocery Stores',
                                                                 'Electronics Manufacturing', 'Business Consulting', 'Real Estate',
                                                                 'Biotech & Pharmaceuticals', 'Food & Beverage Manufacturing',
                                                                 'Motor Vehicle Dealers', 'Legal', 'Accounting & Tax',
                                                                 'Food & Beverage Stores', 'Staffing, Recruitment & Subcontracting',
                                                                 'Consumer Product Manufacturing', 'Taxi & Car Services',
                                                                 'Broadcast Media', 'General Repair & Maintenance',
                                                                 'National Services & Agencies', 'Financial Transaction Processing',
                                                                 'Municipal Agencies', 'Colleges & Universities',
                                                                 'Insurance Agencies & Brokerages', 'Investment & Asset Management',
                                                                 'Energy & Utilities', 'Rail Transportation', 'Gambling & Betting',
                                                                 'Wholesale', 'Drug & Health Stores', 'Restaurants & Cafes',
                                                                 'Department, Clothing & Shoe Stores', 'Internet & Web Services',
                                                                 'Video Game Publishing', 'Computer Hardware Development',
                                                                 'Machinery Manufacturing', 'Mining & Metals',
                                                                 'Membership Organisations', 'Regional Agencies',
                                                                 'Education Support & Training Services', 'Construction',
                                                                 'Telecommunications Services', 'Wood & Paper Manufacturing',
                                                                 'Shipping & Trucking', 'Home Furniture & Housewares Stores',
                                                                 'Transportation Equipment Manufacturing', 'Hotels & Resorts',
                                                                 'Software Development', 'Pet & Pet Supplies Stores',
                                                                 'Commercial Equipment Services', 'Preschools & Childcare Services',
                                                                 'Convenience & Corner Stores',
                                                                 'Automotive Parts & Accessories Stores',
                                                                 'Architectural & Engineering Services',
                                                                 'Nursing & Residential Care Facilities', 'Crop Production',
                                                                 'Aerospace & Defence', 'Event Services', 'Pharmaceutical',
                                                                 'Metal & Mineral Manufacturing', 'Primary & Secondary Schools',
                                                                 'Fishery', 'Chemical Manufacturing', 'Culture & Entertainment',
                                                                 'Medical Testing & Clinical Laboratories',
                                                                 'Grantmaking & Charitable Foundations',
                                                                 'General Merchandise & Superstores', 'Dental Clinics',
                                                                 'Research & Development', 'Beauty & Personal Accessories Stores',
                                                                 'Beauty & Wellness', 'Building & Personnel Services',
                                                                 'Religious Institutions', 'Publishing',
                                                                 'Health Care Products Manufacturing',
                                                                 'Consumer Electronics & Appliances Stores', 'Stock Exchanges',
                                                                 'Film Production', 'Ticket Sales', 'Travel Agencies',
                                                                 'Biotechnology'])
    company_sector = st.selectbox('company_sector', options=['Search', 'Retail & Wholesale', 'Information Technology',
                                                             'Restaurants & Food Service', 'Insurance', 'Healthcare',
                                                             'Transportation & Logistics', 'Human Resources & Staffing',
                                                             'Arts, Entertainment & Recreation', 'Media & Communication',
                                                             'Non-profit & NGO', 'Finance', 'Telecommunications',
                                                             'Manufacturing', 'Management & Consulting', 'Real Estate',
                                                             'Pharmaceutical & Biotechnology', 'Legal',
                                                             'Construction, Repair & Maintenance Services',
                                                             'Government & Public Administration', 'Education',
                                                             'Energy, Mining, Utilities', 'Hotel & Travel Accommodation',
                                                             'Agriculture', 'Aerospace & Defence', 'Personal Consumer Services'])

    if st.button('Predict'):
        X_new = [[job_title, job_description, company_size,
                  company_type, company_industry, company_sector]]
        new_data_df = pd.DataFrame(X_new, columns=[
                                   'job_title', 'job_description', 'company_size', 'company_type', 'company_industry', 'company_sector'])

        processed_raw = process_new(new_data_df)

        prediction = model.predict(processed_raw)
        x = st.columns(2)
        x[0].text_area("Min Salary", prediction[0][0])
        x[1].text_area('Max Salary', prediction[0][1])


if __name__ == '__main__':
    tab1, tab2 = st.tabs(['Job Recommender', 'Salary Prediction'])
    with tab1:
        job_matcher()

    with tab2:
        salary_prediction()
