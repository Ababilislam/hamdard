#item_API
# http://127.0.0.1:8000/hamdard_api/medicine/get_rx_medicine
def index():
    return 'Welcome to mReporting.'

def get_rx_medicine():
    response.view = 'generic.json'

    medRecords = 'select `name`, `brand`, `generic`, `strength`, `formation`, `company` from medicine_list limit 0,20000;'
    medRecords = db.executesql(medRecords, as_dict=True)

    res_data=medRecords

    return dict(res_data=res_data)

