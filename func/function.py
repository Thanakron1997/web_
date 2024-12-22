from datetime import datetime

def getNextVist(visit):
    try:
        today = datetime.today()
        # Filter data for next_visit > today
        filtered_data = [item for item in visit if item['next_visit_date'] > today]
        # Find the closest next_visit
        closest = min(filtered_data, key=lambda x: x['next_visit_date'], default=None)
    except:
        closest = {}
        closest['next_visit'] = "error"
        closest['next_visit_date'] = "error"
    return closest

