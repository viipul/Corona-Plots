import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")
df1=pd.read_csv('https://covid.ourworldindata.org/data/ecdc/full_data.csv')
#df1=pd.read_csv('C:\\Users\\VIPUL\\Downloads\\full_data.csv')
df=df1
df['date']=pd.to_datetime(df['date'])
df['date']=df['date'].dt.dayofyear
df=df[df.date!= 365]
world=df[df['location'].values=='World']
worldcases=world[['date','total_cases','total_deaths']]
daycount=df['date'][df['location'].values=='Afghanistan']
c=daycount.max()
totcount=df[df['date'].values==c]
Most_affected_nations=totcount['location'][totcount['total_cases'].values>=15000]
Most_affected_nations=Most_affected_nations[Most_affected_nations!='World']
Most_affected_nations = pd.DataFrame(Most_affected_nations)
l = Most_affected_nations.values.size
date = pd.to_datetime(2020 * 1000 + c, format='%Y%j')
date = date.strftime('%d/%m')
print('TODAY IS {}'.format(date))
today_total=totcount['total_cases'][totcount['location'].values=='World']
today_deaths=totcount['total_deaths'][totcount['location'].values=='World']
print('Total confirmed cases in the world=',today_total.values[0])
print('Total deaths in the world=',today_deaths.values[0])
print('Current global death rate=',round(100*today_deaths.values[0]/today_total.values[0],2))
ASIA=['China','Iran','Turkey','Saudi Arabia','India']
EUROPE=['France','Russia','Italy','United Kingdom']
AFRICA=['South Africa','Egypt','Algeria','Morocco','Ghana']
NAMERICA=['United States','Canada','Mexico','Panama','Dominican Republic']
SAMERICA=['Brazil','Peru','Chile','Ecuador','Colombia']
OCEANIA=['Australia','New Zealand','French Polynesia','New Caledonia','Fiji']
con=input('Press any key to start, press x stop=')
print('CHOOSE THE NUMBER CORRESPONDING TO ACTION YOU WANT TO PERFORM')
print('1-> To get list of countries having more than,less than or between particular number of cases')
print('2-> To get global scenario of cases and deaths')
print('3->  To get scenario of India')
print('4-> To get scenario any country')
print('5->  Top 5 most affected continents of any continents')
print('6->Compare countries')
print('7->No. of days taken by the world and the countries to reach particular number of cases since the first case')
while con!='x':
    choice=int(input('ENTER CHOICE NUMBER='))
    if choice==1:
        style.use('seaborn-darkgrid')
        limit=int(input('ENTER 0 TO GIVE LOWER LIMIT 1 TO GIVE UPPER LIMIT AND 2 TO GIVE BOTH LIMITS='))
        if limit==0:
            tot_cases=int(input('ENTER LOWER LIMIT OF CASES='))
            Most_affected_nations = totcount[['location','total_cases','total_deaths']][totcount['total_cases'].values >=tot_cases]
            Most_affected_nations = Most_affected_nations[Most_affected_nations != 'World']
            Most_affected_nations = Most_affected_nations.sort_values(by='total_cases', ascending=False)
            Most_affected_nations = Most_affected_nations.dropna()
            Most_affected_nations=Most_affected_nations.reset_index(drop=True)
            if Most_affected_nations.size==0:
                print('NO COUNTRIES FOUND')
            else:
                print('COUNTRIES HAVING CASES/DEATHS MORE THAN {} TILL {}'.format(tot_cases, date))
                print(Most_affected_nations)
            con = input('Press any key to continue, press x stop=')

        if limit==1:
            tot_cases = int(input('ENTER UPPER LIMIT OF CASES='))
            Most_affected_nations = totcount[['location', 'total_cases','total_deaths']][totcount['total_cases'].values <= tot_cases]
            Most_affected_nations = Most_affected_nations[Most_affected_nations != 'World']
            Most_affected_nations = Most_affected_nations.sort_values(by='total_cases', ascending=False)
            Most_affected_nations = Most_affected_nations.dropna()
            Most_affected_nations = Most_affected_nations.reset_index(drop=True)
            if Most_affected_nations.size==0:
                print('NO COUNTRIES FOUND')
            else:
                print('COUNTRIES HAVING CASES MORE THAN {} TILL {}'.format(tot_cases, date))
                print(Most_affected_nations)
            con = input('Press any key to continue, press x stop=')
        if limit==2:
            tot_casesl,tot_casesu = map(int,input('ENTER LOWER AND UPPER LIMIT OF CASES=').split(' '))
            Most_affected_nations = totcount[['location', 'total_cases','total_deaths']][totcount['total_cases'].values >= tot_casesl]
            Most_affected_nations = Most_affected_nations[['location', 'total_cases','total_deaths']][Most_affected_nations['total_cases'].values < tot_casesu]
            Most_affected_nations = Most_affected_nations[Most_affected_nations != 'World']
            Most_affected_nations=Most_affected_nations.sort_values(by='total_cases',ascending=False)
            Most_affected_nations=Most_affected_nations.dropna()
            Most_affected_nations = Most_affected_nations.reset_index(drop=True)
            if Most_affected_nations.size==0:
                print('NO COUNTRIES FOUND')
            else:
                print('COUNTRIES HAVING CASES BETWEEN {} AND {} TILL {}'.format(tot_casesl,tot_casesu,date))
                print(Most_affected_nations)
        if len(Most_affected_nations)!=0:
            askplot=input("WANT TO PLOT(input Y or y to plot )=")
            if askplot=='Y' or askplot=='y':
                for i in range(0, len(Most_affected_nations)):
                    a = Most_affected_nations.values[i]
                    c = a[0]
                    b = df[df['location'].values == c]
                    b = b[1:]
                    plt.plot(b[['date']], b[['total_cases']], label=c)
                    plt.ylabel('total_cases')
                    plt.xlabel('Subsequent Days')
                    plt.title('COVID-19 CASES TILL {}'.format(date))
                plt.legend()
                plt.show()
            else:
                pass

        con=input('Press any key to continue, press x stop=')

    if choice==2:
        plt.subplot(1,2,1)
        print('2-> ACROSS THE GLOBE')
        plt.plot(worldcases[['date']],worldcases[['total_cases']],label='World')
        plt.ylabel('total_cases')
        plt.xlabel('Subsequent Days since 01/01')
        plt.title('COVID-19 CASES TILL {}'.format(date))
        plt.legend()
        plt.subplot(1,2,2)
        plt.plot(worldcases[['date']], worldcases[['total_deaths']], label='World')
        plt.ylabel('total_cases')
        plt.xlabel('Subsequent Days since 01/01')
        plt.title('COVID-19 DEATHS TILL {}'.format(date))
        plt.legend()
        plt.show()
        b = df[df['location'].values == 'World']
        b = b[1:]
        a = b['total_cases'].values
        dates = b['date'].values
        dates = dates[1:]
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append(a[i + 1] - a[i])
        plt.subplot(1,2,1)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Increase in daily cases')
        plt.title('Daily growth of cases in the World')
        a = b['total_deaths'].values
        dates = b['date'].values
        dates = dates[1:]
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append(a[i + 1] - a[i])
        plt.subplot(1, 2, 2)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Increase in daily deaths')
        plt.title('Daily growth of deaths in the World')
        plt.show()
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append((a[i + 1] - a[i])/(a[i]+1)*100)
        plt.subplot(1,2,1)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Rate of increase in daily cases(%)/Total Cases')
        plt.title('Rate of the growth of cases in the World')
        diff_ind = []
        a = b['total_deaths'].values
        dates = b['date'].values
        dates = dates[1:]
        for i in range(0, len(a) - 1):
            diff_ind.append((a[i + 1] - a[i]) / (a[i]+1) * 100)
        plt.subplot(1, 2, 2)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Rate of increase in daily cases(%)/Total Deaths')
        plt.title('Rate of the growth of deaths in the World')
        plt.show()

        con=input('Press any key to continue, press x stop=')

    if choice==3:
        print('ACROSS INDIA')

        #HOW IT SPREAD IN INDIA
        today_deaths = totcount['total_deaths'][totcount['location'].values == 'India']

        b=df[df['location'].values=='India']
        b=b[1:]
        c10 = b['date'][b['total_cases'].values <= 10]
        d1 = b['date'][b['total_cases'].values > 1]
        date1 = d1.min()
        date1 = pd.to_datetime(2020 * 1000 + date1, format='%Y%j')
        date1 = date1.strftime('%d/%m/%y')
        tot = totcount['total_cases'][totcount['location'].values == 'India']
        print('FIRST CASE REPORTED ON {}'.format(date1))
        print('TOTAL CASES TILL {} ARE {}'.format(date,tot.values[0]))
        print('TOTAL DEATHS TILL {} ARE {}'.format(date,today_deaths.values[0]))
        print('CURRENT DEATH RATE=', round(100 * today_deaths.values[0] / tot.values[0], 2))

        if len(c10) == 0:
            t = 1
        else:
            t = c10.max()
        b = b[b['date'].values >=t]
        plt.subplot(1,2,1)
        plt.plot(b[['date']],b[['total_cases']],label='India')
        plt.ylabel('TOTAL CASES')
        plt.xlabel('Subsequent Days since 01/01')
        plt.title('COVID-19 CASES IN INDIA TILL {}'.format(date))
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(b[['date']], b[['total_deaths']], label='India')
        plt.ylabel('TOTAL DEATHS')
        plt.xlabel('Subsequent Days since 01/01')
        plt.title('COVID-19 DEATHS IN INDIA TILL {}'.format(date))
        plt.legend()
        plt.show()
        a = b['total_cases'].values
        dates = b['date'].values
        dates = dates[1:]
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append(a[i + 1] - a[i])
        plt.subplot(1,2,1)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Increase in daily cases')
        plt.title('Daily growth of cases in the India')
        a = b['total_deaths'].values
        dates = b['date'].values
        dates = dates[1:]
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append(a[i + 1] - a[i])
        plt.subplot(1,2,2)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Increase in daily deaths')
        plt.title('Daily growth of deaths in the India')
        plt.show()
        con=input('Press any key to continue, press x stop=')
    if choice==4:
        country=input('Enter the name of the country=')
        b = df[df['location'].values == country]
        b = b[1:]
        c10 = b['date'][b['total_cases'].values <= 10]
        d1 = b['date'][b['total_cases'].values>1]
        date1=d1.min()
        date1 = pd.to_datetime(2020 * 1000 + date1, format='%Y%j')
        date1= date1.strftime('%d/%m/%y')
        print('FIRST CASE REPORTED ON {}'.format(date1))
        tot = totcount['total_cases'][totcount['location'].values ==country]
        totd = totcount['total_deaths'][totcount['location'].values == country]
        print('TOTAL CASES TILL {} ARE {}'.format(date, tot.values[0]))
        print('TOTAL DEATHS TILL {} ARE {}'.format(date, totd.values[0]))
        print('DEATH RATE TILL {} IS {}'.format(date, round(100*totd.values[0])/tot.values[0],2))
        if len(c10)==0:
            t=1
        else:
            t = c10.max()
        b=b[b['date'].values>=t]
        plt.subplot(1,2,1)
        plt.plot(b[['date']], b[['total_cases']], label=country)
        plt.ylabel('TOTAL CASES')
        plt.xlabel('Subsequent Days since 01/01')
        plt.title('COVID-19 CASES IN {} TILL {}'.format(country,date))
        plt.legend()
        plt.subplot(1, 2,2)
        plt.plot(b[['date']], b[['total_deaths']], label=country)
        plt.ylabel('TOTAL DEATHS')
        plt.xlabel('Subsequent Days since 01/01')
        plt.title('COVID-19 DEATHS IN {} TILL {}'.format(country, date))
        plt.legend()
        plt.show()

        a = b['total_cases'].values
        dates = b['date'].values
        dates = dates[1:]
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append(a[i + 1] - a[i])
        plt.subplot(1,2,1)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Increase in daily cases')
        plt.title('Daily growth of cases in the {}'.format(country))
        a = b['total_deaths'].values
        dates = b['date'].values
        dates = dates[1:]
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append(a[i + 1] - a[i])
        plt.subplot(1, 2, 2)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Increase in daily deaths')
        plt.title('Daily growth of deaths in the {}'.format(country))
        plt.show()
        diff_ind = []
        for i in range(0, len(a) - 1):
            diff_ind.append((a[i + 1] - a[i]) / a[i] * 100)
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.bar(dates, diff_ind)
        plt.xlabel('No. of days since Jan 1, 2020')
        plt.ylabel('Rate of increase in daily cases(%)')
        plt.title('Daily growth of cases in the {}'.format(country))
        plt.show()

        con=input('Press any key to continue, press x stop=')

    if choice==5:
        print('ENTER THE NO. CORRESPONDING TO CONTINENT')
        print('1->ASIA')
        print('2->EUROPE')
        print('3->AFRICA')
        print('4->NORTH AMERICA')
        print('5->SOUTH AMERICA')
        print('6->OCEANIA')
        num=int(input('NUMBER='))
        if num==1:
            conti=ASIA
            name='ASIA'
        if num==2:
            conti=EUROPE
            name='EUROPE'
        if num==3:
            conti=AFRICA
            name='AFRICA'
        if num==4:
            conti=NAMERICA
            name='NORTH AMERICA'
        if num==5:
            conti=SAMERICA
            name='SOUTH AMERICA'
        if num==6:
            conti=OCEANIA
            name='OCEANIA'
        print('TOP 5 MOST AFFECTED NATIONS OF {}'.format(name))
        print('***************************CASES**********************************')
        for i in range(0, len(conti)):
            tot = totcount['total_cases'][totcount['location'].values == conti[i]]
            print('TOTAL CASES TILL {} IN {} ARE:{}'.format(date,conti[i],tot.values[0]))
        for i in range(0,len(conti)):
            a=conti[i]
            c=a
            b=df[df['location'].values==c]
            b = b[1:]
            c10 = b['date'][b['total_cases'].values <= 10]
            if len(c10) == 0:
                t = 1
            else:
                t = c10.max()
            b = b[b['date'].values >= t]
            c10 = b['date'][b['total_cases'].values <= 10]
            plt.subplot(1,2,1)
            plt.plot(b[['date']],b[['total_cases']],label=c)
            plt.ylabel('TOTAL CASES')
            plt.xlabel('Subsequent Days since 01/01')
            plt.title('COVID-19 CASES IN {} TILL {}'.format(name,date))
        plt.legend()
        print('**************************DEATHS*****************************')
        for i in range(0, len(conti)):
            tot = totcount['total_deaths'][totcount['location'].values == conti[i]]
            print('TOTAL DEATHS TILL {} IN {} ARE:{}'.format(date,conti[i],tot.values[0]))
        for i in range(0,len(conti)):
            a=conti[i]
            c=a
            b=df[df['location'].values==c]
            b = b[1:]
            c10 = b['date'][b['total_cases'].values <= 10]
            if len(c10) == 0:
                t = 1
            else:
                t = c10.max()
            b = b[b['date'].values >= t]
            c10 = b['date'][b['total_cases'].values <= 10]
            plt.subplot(1,2,2)
            plt.plot(b[['date']],b[['total_deaths']],label=c)
            plt.ylabel('TOTAL DEATHS')
            plt.xlabel('Subsequent Days since 01/01')
            plt.title('COVID-19 DEATHS IN {} TILL {}'.format(name,date))
        plt.legend()
        plt.show()

        con=input('Press any key to continue, press x stop=')
    if choice==6:
        print('ENTER NAMES OF COUNTRIES YOU WANT TO COMPARE(SEPARATED BY COMMA)')
        EUROPEIND2=list(map(str,input().split(',')))
        print('********************************CASES**********************************')
        for i in range(0, len(EUROPEIND2)):
            tot = totcount['total_cases'][totcount['location'].values == EUROPEIND2[i]]
            print('TOTAL CASES TILL {} IN {} ARE:{}'.format(date,EUROPEIND2[i],tot.values[0]))
        print('********************************DEATHS**********************************')
        for i in range(0, len(EUROPEIND2)):
            tot = totcount['total_deaths'][totcount['location'].values == EUROPEIND2[i]]
            print('TOTAL DEATHS TILL {} IN {} ARE:{}'.format(date,EUROPEIND2[i],tot.values[0]))
        for i in range(0,len(EUROPEIND2)):
            a=EUROPEIND2[i]
            c=a
            b=df[df['location'].values==c]
            b = b[1:]
            c10 = b['date'][b['total_cases'].values <= 10]
            if len(c10) == 0:
                t = 1
            else:
                t = c10.max()
            b = b[b['date'].values >= t]
            plt.subplot(1,2,1)
            plt.plot(b[['date']],b[['total_cases']],label=c)
            plt.ylabel('TOTAL CASES')
            plt.xlabel('Subsequent Days since 01/01')
            plt.title('COVID-19 CASES IN {} TILL {}'.format('COUNTRIES',date))
        plt.legend()
        for i in range(0,len(EUROPEIND2)):
            a=EUROPEIND2[i]
            c=a
            b=df[df['location'].values==c]
            b = b[1:]
            c10 = b['date'][b['total_deaths'].values <= 10]
            if len(c10) == 0:
                t = 1
            else:
                t = c10.max()
            b = b[b['date'].values >= t]
            plt.subplot(1,2,2)
            plt.plot(b[['date']],b[['total_deaths']],label=c)
            plt.ylabel('TOTAL DEATHS')
            plt.xlabel('Subsequent Days since 01/01')
            plt.title('COVID-19 DEATHS IN {} TILL {}'.format('COUNTRIES',date))
        plt.legend()
        plt.show()

         
        con=input('Press any key to continue, press x stop=')

    if choice==7:
        d10=[]
        a=int(input('ENTER NUMBER OF CASES='))
        #totcount=totcount[totcount['location'].values='World']
        totcount=totcount[totcount['location'].values!='International']
        CNAME=totcount['location'][totcount['total_cases'].values>=a]
        for i in CNAME:
            if i=='World' or i=='International':
                pass
            else:
                b=df[df['location'].values==i]
                b = b[1:]
                c10 = b['date'][b['total_cases'].values <= 10]
                if len(c10) == 0:
                    t = 1
                else:
                    t = c10.max()
                b = b[b['date'].values >= t]
                c10 = b['date'][b['total_cases'].values <= a]
                if len(c10)==0:
                    d10.append(0)
                else:
                    d10.append(c10.max())
        print('NO. of days to Reach first {} cases'.format(a))
        for i in range(0,len(d10)):
            print(' {} -> {}'.format(CNAME.values[i],d10[i]))
         
        con=input('Press any key to continue, press x stop=')
