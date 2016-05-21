library(RMySQL)
library(lubridate)
library(ggplot2)
library(scales)
library(properties)

setwd('/Users/awoolford/backtesting-the-dow/prototype')
properties <- read.properties(file = 'backtesting_the_dow.properties')

con = dbConnect(MySQL(),
                user='awoolford',
                password='********',
                dbname='backtesting_the_dow',
                host='deepthought')

data <- dbReadTable(con, "predictit_prices")

data$timestamp <- ymd_hms(data$timestamp)

qplot(timestamp, last_trade_price, data = subset(data, short_name %in% c('Clinton', 'Trump', 'Sanders', 'Cruz')), geom = "line", group = short_name, color = short_name) +
  scale_y_continuous(label = dollar, limits = c(0, 1)) + scale_colour_manual(values=c('blue', 'orange', 'black', 'red')) +
  labs(title = "predictit.org intra-day historic prices", x = "", y = "last trade price")

ggsave("predictit_election_last_trade_prices.png")




