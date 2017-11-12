library(shiny)
library(shinydashboard)
library(shinyBS)
library(shinycssloaders)
library(tidyverse)
library(plotly)
library(dygraphs)
library(xts)
library(tidytext)
library(flexdashboard)
library(forecast)

# load data
prices <- readRDS("./data/CurrencyPrices.RDS")
bcm_text <- readRDS("./data/BCM_Text_Corpus.RDS")
sentiments <- readRDS("./data/Sentiments.RDS")


commits <- read_csv("./data/commits.csv")
commits$timestamp <- as.POSIXct(commits$time, origin = "1970-01-01", tz = 'UTC') %>% 
  as.Date()
