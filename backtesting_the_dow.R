library(RMySQL)
library(lubridate)
library(ggplot2)
library(scales)
library(properties)
library(randomForest)

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

qplot(climb_trigger_percentage, percentage_change, data = subset(data, transaction_cost == 9), alpha=I(1/5)) + scale_x_continuous(label=percent) + scale_y_continuous(label=percent)

ggsave(file = "climb_trigger_percent.png", width = 8, height = 6)

qplot(fall_trigger_percentage, percentage_change, data = subset(data, transaction_cost == 9), alpha=I(1/5)) + scale_x_continuous(label=percent) + scale_y_continuous(label=percent)

ggsave(file = "fall_trigger_percent.png", width = 8, height = 6)
