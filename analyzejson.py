import json

class Node():
    def __init__(self, d, coordinates, t, p, np):
        """Constructor for Character"""
        self.selfnodedate = d
        self.nodecoordinates = coordinates
        self.tone = t
        self.stockprice = p
        self.stocknextprice = np
        # self.value = v
        # self.value = value

def values(stock_pre, stock_post, tone, value):
    if(stock_post-stock_pre > 0):
        if(tone> 0):
            value = value*2
            return value
        if(tone< 0):
            #account for the fact that not every location is reported , some reported more than other
            #so should divide if wrong
            value = value/2
            return value
        if(tone ==0):
            return value
    if(stock_post-stock_pre < 0):
        if(tone< 0):
            value = value*2
            return value
        if(tone> 0):
            #account for the fact that not every location is reported , some reported more than other
            #so should divide if wrong
            value = value/2
            return value
        if(tone ==0):
            return value
    else:
        return value

def analyzejson():
    with open('static/goldman.geojson') as f:
        data = json.load(f)
    with open('static/goldman2.geojson') as f:
        stocks = json.load(f)
    article = 0
    articles = []
    date_price = {}
    prices=[]
    i = 0
    date = 0
    price = 0
    nextprice = 0
    for feature in stocks['features']:
        #print(feature['geometry']['type'])
        # print(feature['geometry']['coordinates'])
        # print(feature['properties']['date'])
        # print(feature['properties']['tone'])
        # print(feature['properties']['price'])
        if (date != feature['date']):
            prices.append(feature['price'])
        date = feature['date']
        # print(date)
        date_price[feature['date']] = feature['price']

    print(prices)
    for feature in data['features']:
        if (date != feature['properties']['date']):
            i=i+1
        if (i <29):
            if (prices[i-1] != -1.0):
                # print(prices[i-1])
                price = prices[i-1]
                nextprice= prices[i]
                if (prices[i]==-1.0):
                    nextprice= prices[i+1]
                    if (prices[i+1]==-1.0):
                        nextprice= prices[i+2]
            else:
                price = prices[i-2]
                if (prices[i-2]==-1.0):
                    price = prices[i-3]
                nextprice= prices[i]
                if (prices[i]==-1.0):
                    nextprice= prices[i+1]
            # print(price)
            # print(nextprice)
            # print(feature['geometry']['coordinates'])
            article = Node(feature['properties']['date'], feature['geometry']['coordinates'], feature['properties']['tone'], price, nextprice)
            articles.append(article)
            # article_num = article_num +1
        date = feature['properties']['date']

    coord_values={}
    j = 0
    for j in range(len(articles)):
        coordinate_string = ','.join(str(e) for e in articles[j].nodecoordinates)
        coord_values[coordinate_string] = 1
        j = j+1
    k = 0
    for j in range(len(articles)):
        coordinate_string = ','.join(str(e) for e in articles[j].nodecoordinates)
        coord_values[coordinate_string] = values(articles[j].stockprice, articles[j].stocknextprice, articles[j].tone, coord_values[coordinate_string])
        j=j+1


    # print(prices)
    # print(date_price)
    #
    # print(prices)
    # print(len(prices))
    # print(i)
    # print(articles[0].value)
    max_value = max(coord_values.values())
    max_keys = [k for k, v in coord_values.items() if v == max_value]
    # print(coord_values)
    print(max_value, max_keys)



if __name__ == '__main__':
	analyzejson()
