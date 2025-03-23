from datetime import datetime
import pandas as pd

def getNextVist(visit):
    try:
        today = datetime.today()
        # Filter data for next_visit > today
        filtered_data = [item for item in visit if item['next_visit_date'] > today]
        # Find the closest next_visit
        closest = min(filtered_data, key=lambda x: x['next_visit_date'], default=None)
        if closest:
            return closest
        else:
            lastVisit = max(visit, key=lambda x: x['next_visit_date'], default=None)
            lastVisit['lastVisit'] = True
            return lastVisit
    except:
        try:
            lastVisitNoStudy = max(visit, key=lambda x: x['visit_date'], default=None)
            if lastVisitNoStudy['next_visit'].upper() == 'NOVISIT':
                lastVisit = {}
                lastVisit['next_visit'] = lastVisitNoStudy['next_visit']
                lastVisit['next_visit_date'] = "NA"
                return lastVisit
            else:
                closest = {}
                closest['next_visit'] = "NA"
                closest['next_visit_date'] = "NA"
                return closest
        except:
            closest = {}
            closest['next_visit'] = "NA"
            closest['next_visit_date'] = "NA"
            return closest

def convertVisitDate(row):
    subjectNumber = row['subjectNumber']
    if len(row['visit_data']) == 0:
        pass
    else:
        df_visit = pd.DataFrame(row['visit_data'])
        df_visit = df_visit.drop_duplicates(subset=['visit', 'visit_date'])
        df_visit = df_visit.drop(columns=['next_visit', 'next_visit_date','notes'])
        df_transposed = df_visit.set_index('visit').T
        df_transposed.columns = ['visit_' + col for col in df_transposed.columns]
        df_transposed['subjectNumber'] = subjectNumber
        df_transposed.columns = df_transposed.columns.str.upper()
        df_transposed = df_transposed.reset_index(drop=True)        
        return df_transposed

def convertPhoneCall(row):
    if isinstance(row['PhoneCallData'], list):        
        subjectNumber = row['subjectNumber']
        df_visit = pd.DataFrame(row['PhoneCallData'])
        df_transposed = df_visit.set_index('PhoneCall').T
        df_transposed.columns = ['PhoneCall_' + col for col in df_transposed.columns]
        df_transposed['subjectNumber'] = subjectNumber
        df_transposed.columns = df_transposed.columns.str.upper()
        df_transposed = df_transposed.reset_index(drop=True)
        return df_transposed

def createExcel(users):
    users = [{
        **i,
        'next_Visit': (nextVisit['next_visit'] if (nextVisit := getNextVist(i['visit_data'])) else "NA")
        if 'visit_data' in i else "NA",
        'next_Visit_Date': (nextVisit['next_visit_date'] if nextVisit else "NA")
        if 'visit_data' in i else "NA",
    }
    for i in users]
    df = pd.DataFrame(users)
    visit_date_list = df.apply(convertVisitDate, axis=1)
    visit_df = pd.concat(visit_date_list.to_list(), axis=0)
    visit_df = visit_df.sort_index(axis=1)
    phone_call_list = df.apply(convertPhoneCall, axis=1)
    phone_df = pd.concat(phone_call_list.to_list(), axis=0)
    phone_df = phone_df.sort_index(axis=1)
    df.columns = df.columns.str.upper()
    dfall = pd.merge(df,visit_df,how='left',on='SUBJECTNUMBER')
    dfall = pd.merge(dfall,phone_df,how='left',on='SUBJECTNUMBER')
    dfall = dfall.drop(columns=['VISIT_DATA', 'PHONECALLDATA','_ID'])
    return dfall
