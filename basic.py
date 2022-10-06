from flask import Flask, request, redirect
import csv  
import datetime
 
app = Flask(__name__)
 

@app.route('/')
def index():
    return 'Index Page'


@app.route('/test_api/', methods=['GET','POST'])
def test_api():
    if request.method == 'POST':
        value = request.form.get('value')
        visualize = request.form.get('visualize')

    #test from browser at /test_api?value=xx&visualize=True
    elif request.method == 'GET':
        value = request.args.get('value')
        visualize = request.args.get('visualize')
    
    #csv export
    header = ['value']
    data = [[value]]      
    title = datetime.datetime.now()
    title = str(title).replace(':', '-')
    title = title[:10] + "-" + title[11:16] + '_export.csv'
    
    with open(title, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            writer.writerow(d)
    
    #visualization
    if visualize == "True":
        return redirect((f"/visualize/{value}"))
        
    return 'Export Success'


@app.route('/visualize/<value>') 
def visualize(value):
    return 'Visualization'


if __name__ == '__main__':
    app.run(host='0.0.0.0')