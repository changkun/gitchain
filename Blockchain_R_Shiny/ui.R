header <- dashboardHeader(title = "GitChain")

source("ui_body.R")
source("ui_sidebar.R")

ui <- dashboardPage(header = header, 
                    sidebar = sidebar, 
                    body = body)