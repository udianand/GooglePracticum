# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Library Import
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class Model_Conclusion():
    
    def __init__(self):
        self.model_results = []
        #  Stores the name of model
        self.model_name = []
        self.model_std = []
        self.font_size = 5
        # import the train test split
        from sklearn.model_selection import train_test_split
        
        # List to store results
        
        # Get current working directory
        cwd = os.getcwd()
        path = cwd + "/Model_inputs/"
        # Uses the input file generated from preprocessing
        input_file = path + 'input_WA.csv'
        input_price= path + "input_price.csv"
        
        self.input_data_temp = pd.read_csv(input_file)
        self.input_data_temp = self.input_data_temp.iloc[:, 3:]
        self.price_y = pd.read_csv(input_price)
        
        self.input_data, X_test, self.price, y_test = train_test_split(self.input_data_temp, self.price_y, test_size=0.0)
        
        # Making all column names UPPER CASE --> inline with the weather data file
        self.input_data.columns = map(str.upper, self.input_data.columns)
        
        # List of column names
        self.col_names = list(self.input_data)

        pass
    
    def Run_models(self):
        
        from sklearn.model_selection import cross_val_score
        # Stores the performance on test set.
        
        # Linear Regression
        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()
        
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("MLR")
        
        #Ridge Regression
        from sklearn.linear_model import Ridge
        regressor = Ridge()
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("Ridge")
        
        from sklearn.linear_model import Ridge
        regressor = Ridge(alpha = 0.1)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("Ridge0.1")
        
        #Lasso
        from sklearn.linear_model import Lasso
        regressor = Lasso()
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("Lasso")
        
        from sklearn.linear_model import Lasso
        regressor = Lasso(alpha=0.0001, max_iter=100000)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("Lasso_\n0.0001")
        
        #ElasticNet
        from sklearn.linear_model import ElasticNet
        regressor = ElasticNet(alpha=0.1, l1_ratio=0.7,max_iter = 100000)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("ElasticNet")
        
        #SVR
        from sklearn.svm import SVR
        regressor = SVR()
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("SVM")

        #Decision Tree
        
        from sklearn.tree import DecisionTreeRegressor
        regressor = DecisionTreeRegressor(random_state = 0)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("DT")
        
        #Random Forest
        from sklearn.ensemble import RandomForestRegressor
        regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("RF_10")
        
        from sklearn.ensemble import RandomForestRegressor
        regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("RF_100")
        
        from sklearn.ensemble import RandomForestRegressor
        regressor = RandomForestRegressor(n_estimators = 300, random_state = 0)
        accuracies = cross_val_score(estimator = regressor, X = self.input_data, y = self.price["Price"], cv = 10)
        self.model_results.append(accuracies.mean())
        self.model_std.append(accuracies.std())
        self.model_name.append("RF_300")
        self.model_results = list(map(lambda x: x*100, self.model_results)) 
        self.model_std = list(map(lambda x: x*100, self.model_std)) 
        
  

    def Results(self):
        def write_value_on_bar(ax, y_range):
            ax.set_ylim([0, y_range])
            for p in ax.patches:
                height = p.get_height()
                ax.text(p.get_x()+p.get_width()/2.,
                        height + 0.5,
                        '{:1.2f}'.format(height),
                        ha="center") 
                
        result_list = sorted(zip(self.model_name, self.model_results, self.model_std), key = lambda x:x[1] ,reverse=True)
      
        sns.set(style="whitegrid")
        
        # Set up the matplotlib figure
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11, 7), sharex=True)
        # Generate some sequential data
        x = np.asarray(["Accuracy", "Std"])
        
        y1 = np.asarray(result_list[0][1:])
        y2 = np.asarray(result_list[1][1:])
        y3 = np.asarray(result_list[2][1:])
        y_range = 70
        plot_1 = sns.barplot(x, y1, palette="BuGn_d", ax=ax1)
        plot_2 = sns.barplot(x, y2, palette="BuGn_d", ax=ax2)
        plot_3 = sns.barplot(x, y3, palette="BuGn_d", ax=ax3)

        write_value_on_bar(plot_1, y_range)
        write_value_on_bar(plot_2, y_range)
        write_value_on_bar(plot_3, y_range)
        
        ax1.set_ylabel("Percentage")
        ax1.set_title(result_list[0][0])
        ax2.set_title(result_list[1][0])
        ax3.set_title(result_list[2][0])
        
        plt.show()
        pass
    
        
    
    def Details(self):
                
        from matplotlib import cm
        from sklearn.model_selection import cross_val_score
        from sklearn.ensemble import RandomForestRegressor
        
        def write_value_on_bar(ax):
            for p in ax.patches:
                height = p.get_height()
                ax.text(p.get_x()+p.get_width()/2.,
                        height + 0.5,
                        '{:1.2f}'.format(height),
                        ha="center") 
        
        result_list = sorted(zip(self.model_name, self.model_results, self.model_std), key = lambda x:x[1] ,reverse=True)
        sorted_model_names = [ i[0] for i in result_list ]
        sorted_accuracies = [ i[1] for i in result_list ]
        sorted_stds = [ i[2] for i in result_list ]

        sns.set(style="whitegrid")
        
        plot_1 = sns.barplot(np.asarray(sorted_model_names), np.asarray(sorted_accuracies), palette=sns.cubehelix_palette(start=.5, rot=-.75))
        plot_1.set_title("Model Accuracies")
        plot_1.set_ylabel("Percentage")
        write_value_on_bar(plot_1)
        plt.show()
        
        plot_2 =sns.barplot(np.asarray(sorted_model_names), np.asarray(sorted_stds), palette=sns.cubehelix_palette(start=.5, rot=-.75))
        plot_2.set_title("Standard Deviations")
        plot_2.set_ylabel("Percentage")
        write_value_on_bar(plot_2)
        plt.show()
        
        
        
        # Heatmap
        corr_data = self.input_data_temp
        corr_data = pd.concat([corr_data, self.price.iloc[:, -3:]], axis=1)
        correlation_matrix = np.corrcoef(corr_data.values.T)
        heat_map_column_names = list(corr_data)
        sns.set(font_scale = 0.7)
        plt.figure(figsize = (12,12))
        hm = sns.heatmap(correlation_matrix,
            cbar=True,
            annot=True,
            square=True,
            fmt='.2f',
            annot_kws={'size': 7},
            yticklabels=heat_map_column_names,
            xticklabels=heat_map_column_names)
        plt.show()
        
        
        
        
        
        
        
        
        
        
        #Time lag analysis
        
        
        from sklearn.model_selection import train_test_split
        
        accuracy_df = pd.DataFrame(0,index = range(13), columns = ["Price", "Price_discounted"])
        
        def rf_300_model_test(price_data, weather_data, time_lag):
            
            price_drop_range = []
            weather_drop_range = []
            for i in range(time_lag):
                price_drop_range.append(i)
                weather_drop_range.append((-1)*(i + 1))
            time_lag_price = price_data.drop(self.price_y.index[price_drop_range])
            time_lag_weather = weather_data.drop(weather_data.index[weather_drop_range])
            temp_weather, X_test, temp_price, y_test = train_test_split(time_lag_weather, time_lag_price, test_size=0.0)
            results = []
            
            regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
            accuracies = cross_val_score(estimator = regressor, X = temp_weather, y = temp_price["Price"], cv = 10)
            results.append(accuracies.mean())
            
            accuracies = cross_val_score(estimator = regressor, X = temp_weather, y = temp_price["Discounted_Price"], cv = 10)
            results.append(accuracies.mean())
            
            return results
        

        for i in range(13):
            scores = rf_300_model_test(self.price_y, self.input_data_temp, i)
            accuracy_df.loc[i, "Price"] = scores[0]
            accuracy_df.loc[i, "Price_discounted"] = scores[1]
        index_name = []
        for i in range(13):
            index_name.append("+" + str(i) + " Months")
        accuracy_df.index = index_name
        print(accuracy_df)
        
        graph = accuracy_df.plot(kind='bar', figsize=(10, 5))
        graph.set_title("Time Lag Analysis [Random Forest 10]", fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.ylabel('Accuracy', fontsize=14)
        plt.xlabel('Time Lags', fontsize=14)
        plt.legend()
        plt.show()
        
        # Give each bar separate color
        '''
        color_code_vector = random.sample(range(1, 100), len(self.model_name))
        reg_color_code_vector = map(lambda x: x/max(color_code_vector), color_code_vector)
        reg_color_code_vector = list(reg_color_code_vector)
        colors = cm.hsv(reg_color_code_vector)
        
        # Expressing accuracy in percentage
        model_results_percentage = list(map(lambda x: x*100, self.model_results))
        
        y_pos = np.arange(len(self.model_name))
        
        plt.rcdefaults() # white background, gets rid of gray
        plt.figure(figsize = (2*self.font_size,self.font_size))
        plt.bar(y_pos, model_results_percentage, align='center', alpha=0.5, width=0.4, color = colors)
        plt.xticks(y_pos, self.model_name, fontsize = 3*self.font_size)
        plt.ylabel('Accuracy in perecentage', fontsize=3*self.font_size)
        plt.title('Accuracy: Regression Models', fontsize=3*self.font_size, fontweight='bold')
        plt.show()
        
        
        # Give each bar separate color
        color_code_vector = random.sample(range(1, 100), len(self.model_name))
        reg_color_code_vector = map(lambda x: x/max(color_code_vector), color_code_vector)
        reg_color_code_vector = list(reg_color_code_vector)
        colors = cm.hsv(reg_color_code_vector)
        
        
        # Expressing accuracy in percentage
        model_std_percentage = list(map(lambda x: x*100, self.model_std))
        
        y_pos = np.arange(len(self.model_name))
        
        plt.rcdefaults() # white background, gets rid of gray
        plt.figure(figsize = (2*self.font_size,self.font_size))
        plt.bar(y_pos, model_std_percentage, align='center', alpha=0.5, width=0.4, color = colors)
        plt.xticks(y_pos, self.model_name, fontsize = 3*self.font_size)
        plt.ylabel('STD in perecentage', fontsize=3*self.font_size)
        plt.yticks(range(0,100,10), fontsize = 3*self.font_size)
        plt.title('STD: Regression Models', fontsize=3*self.font_size, fontweight='bold')
        plt.show()
        '''
        pass
    


#ps
#Risk-free rate for 1986 - 2016 : 9.34% ( 30-year Treasury Constant Maturity Rate at 1986 )
# Monthly discount rate = 1/1.000248 

# Splitting Data into Training and Test






