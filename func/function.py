from datetime import datetime

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
        closest = {}
        closest['next_visit'] = "NA"
        closest['next_visit_date'] = "NA"
        return closest

