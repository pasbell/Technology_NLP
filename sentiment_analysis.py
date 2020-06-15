import pandas as pd

#Sentiment Analysis
def get_nrc_data():
    nrc = "NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    count=0
    emotion_dict=dict()
    with open(nrc,'r') as f:
        all_lines = list()
        for line in f:
            if count < 46:
                count+=1
                continue
            line = line.strip().split('\t')
            if int(line[2]) == 1:
                if emotion_dict.get(line[0]):
                    emotion_dict[line[0]].append(line[1])
                else:
                    emotion_dict[line[0]] = [line[1]]
    return emotion_dict


emotion_dict = get_nrc_data()

def emotion_analyzer(text,emotion_dict=emotion_dict):
    #Set up the result dictionary
    emotions = {x for y in emotion_dict.values() for x in y}
    emotion_count = dict()
    for emotion in emotions:
        emotion_count[emotion] = 0

    #Analyze the text and normalize by total number of words
    total_words = len(text.split())
    for word in text.split():
        if emotion_dict.get(word):
            for emotion in emotion_dict.get(word):
                emotion_count[emotion] += 1/len(text.split())
    return emotion_count



def comparative_emotion_analyzer(doc_tuples):
    import pandas as pd
    df = pd.DataFrame(columns=['doc_id','Anger','Fear','Trust','Negative',
                           'Positive','Joy','Disgust','Anticipation',
                           'Sadness','Surprise','Net_Sentiment'],)
    df.set_index("doc_id",inplace=True)
    
    output = df    
    for text_tuple in doc_tuples:
        text = text_tuple[1] 
        result = emotion_analyzer(text)
        df.loc[text_tuple[0]] = [result['anger'],result['fear'],result['trust'],
                  result['negative'],result['positive'],result['joy'],result['disgust'],
                  result['anticipation'],result['sadness'],result['surprise'],
                                result['positive'] - result['negative']]
    return output


def comparative_emotion_analyzer(doc_df):
    import pandas as pd
    
    output = pd.concat([doc_df,doc_df['text'].apply(lambda x: emotion_analyzer(x)).apply(pd.Series)], axis = 1)
    
    return output




bodies1 = pd.read_csv("top_bodies1.csv").drop(columns = {"Unnamed: 0", "urls"})
bodies2 = pd.read_csv("top_bodies2.csv").drop(columns = {"Unnamed: 0", "urls"})
bodies3 = pd.read_csv("top_bodies3.csv").drop(columns = {"Unnamed: 0", "urls"})

all_bodies = pd.concat([bodies1, bodies2, bodies3])
all_bodies['text'] = all_bodies['text'].astype(str)
all_bodies['Month'] = pd.to_datetime(all_bodies['Month'],format='(%Y, %m)')
all_bodies['year'] = all_bodies['Month'].apply(lambda x: x.year)
all_bodies['month'] = all_bodies['Month'].apply(lambda x: x.month)
all_bodies = all_bodies.drop(columns = {'Month'})


emotions_df = comparative_emotion_analyzer(all_bodies)
emotions_df['month'] = emotions_df['month'].apply(lambda x:"%02d"%x)
emotions_df['year'] = emotions_df['year'].apply(lambda x:"%04d"%x)
emotions_df['yyyymm'] = emotions_df.apply(lambda x: x['year'] + x['month'], 1)

averages_emotions = emotions_df.groupby(['yyyymm']).mean().reset_index()
year_averages_emotions = emotions_df.groupby('year').mean().reset_index()
averages_emotions = averages_emotions.set_index('yyyymm')
year_averages_emotions = year_averages_emotions.set_index('year')



#Visualization
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
output_notebook()

from bokeh.io import output_notebook, show
from bokeh.layouts import gridplot
from bokeh.plotting import figure
import pandas as pd


p1 = figure(title="Trust over Time",
          x_axis_label = "time",y_axis_label = "level of emotion",x_axis_type="datetime",
          tools="pan,box_zoom, crosshair,reset, save")

p1.line(pd.to_datetime(year_averages_emotions.index,format="%Y"), year_averages_emotions['trust'],legend="trust")


p2 = figure(title="Joy over Time",
          x_axis_label = "time",y_axis_label = "level of emotion",x_axis_type="datetime",
          tools="pan,box_zoom, crosshair,reset, save")

p2.line(pd.to_datetime(year_averages_emotions.index,format="%Y"), year_averages_emotions['joy'],legend="joy",color="green")

p3 = figure(title="Anger over Time",
          x_axis_label = "time",y_axis_label = "level of emotion",x_axis_type="datetime",
          tools="pan,box_zoom, crosshair,reset, save")

p3.line(pd.to_datetime(year_averages_emotions.index,format="%Y"), year_averages_emotions['anger'],legend="anger",color="red")


p4 = figure(title="Fear over time",
          x_axis_label = "time",y_axis_label = "level of emotion",x_axis_type="datetime",
          tools="pan,box_zoom, crosshair,reset, save")

p4.line(pd.to_datetime(year_averages_emotions.index,format="%Y"), year_averages_emotions['fear'],legend="fear",color="orange")


p5 = figure(title="Surprise over time",
          x_axis_label = "time",y_axis_label = "level of emotion",x_axis_type="datetime",
          tools="pan,box_zoom, crosshair,reset, save")

p5.line(pd.to_datetime(year_averages_emotions.index,format="%Y"), year_averages_emotions['surprise'],legend="surprise",color="orange")


p6 = figure(title="Disgust over Time",
          x_axis_label = "time",y_axis_label = "level of emotion",x_axis_type="datetime",
          tools="pan,box_zoom, crosshair,reset, save")

p6.line(pd.to_datetime(year_averages_emotions.index,format="%Y"), year_averages_emotions['disgust'],legend="disgust",color="purple")



grid = gridplot([[p1,p2,p5], [p3, p4,p6]],sizing_mode="scale_both",merge_tools=False)



show(grid)




