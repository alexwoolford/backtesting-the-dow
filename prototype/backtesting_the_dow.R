library(RMySQL)
library(lubridate)
library(ggplot2)
library(scales)
library(properties)
library(randomForest)
library(plyr)

properties <- read.properties(file = 'backtesting_the_dow.properties')

con = dbConnect(MySQL(),
                user=properties$mysql.user,
                password=properties$mysql.password,
                dbname=properties$mysql.database,
                host=properties$mysql.host)

data <- dbReadTable(con, "scenario_outcome")

randomForestModel <- randomForest(data = data, percentage_change ~ transaction_cost + transaction_size + fall_trigger_percentage + climb_trigger_percentage)

importance_data <- importance(randomForestModel)

print(importance_data)


climb_trigger_percentage_change <- ddply(subset(data, transaction_cost == 9), .(climb_trigger_percentage), summarize, mean_percentage_change = mean(percentage_change))

qplot(climb_trigger_percentage, mean_percentage_change, data = climb_trigger_percentage_change, geom = "line") + scale_x_continuous(label=percent) + scale_y_continuous(label=percent)

ggsave(file = "climb_trigger_percent.png", width = 8, height = 6)


fall_trigger_percentage_change <- ddply(subset(data, transaction_cost == 9), .(fall_trigger_percentage), summarize, mean_percentage_change = mean(percentage_change))

qplot(fall_trigger_percentage, mean_percentage_change, data = fall_trigger_percentage_change, geom = "line") + scale_x_continuous(label=percent) + scale_y_continuous(label=percent)

ggsave(file = "fall_trigger_percent.png", width = 8, height = 6)

