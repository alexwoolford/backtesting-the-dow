library(RMySQL)
library(lubridate)
library(ggplot2)
library(scales)
library(properties)
library(reshape2)

properties <- read.properties(file = '/Users/awoolford/backtesting-the-dow/prototype/backtesting_the_dow.properties')

con = dbConnect(MySQL(),
user=properties$mysql.user,
password=properties$mysql.password,
dbname=properties$mysql.database,
host=properties$mysql.host)

data <- dbReadTable(con, "scenario_outcome")

data$transaction_cost <- NULL

qplot(climb_trigger, portfolio_percentage_change, data = data, geom = "line") +
facet_grid(fall_trigger ~ transaction_size) +
scale_y_continuous(label=percent) +
scale_x_continuous(label=dollar) +
theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
labs(x = "climb trigger", y = "portfolio % change", title = "SCHX backtest scenarios (Mar 28th, 2016 -> May 20th, 2016); column facet: transaction size; row facet: fall trigger")

ggsave("/Users/awoolford/scenario_outcome_fixed.pdf", height = 15, width = 50, limitsize=FALSE)

