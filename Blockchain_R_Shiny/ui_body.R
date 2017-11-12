body <- dashboardBody(
  tabItems(
    tabItem(tabName = "timeseries",
            h2("Timeseries"),
            p("Choose out of 837 different crypto-currencies."),
            fluidRow(column(4, uiOutput(outputId = "currency_names_ui"))),
            fluidRow(column(12, withSpinner(dygraphOutput(outputId = "price_time_dygraph")))),
            fluidRow(column(12, withSpinner(dygraphOutput(outputId = "curr_sent_dygraph")))),
            shinyBS::bsPopover(id = "currency_names_ui", title = "Currency Names", content = "Max. 3 currencies are shown in plot.")
  ),
  tabItem(tabName = "correlation",
          h2("Correlation"),
          withSpinner(plotlyOutput("price_article_corr"))),
  tabItem(tabName = "hot_list",
          h2("Hot List"),
          fluidRow(column(4, uiOutput(outputId = "hot_list1")),
                   column(8, withSpinner(gaugeOutput("hot_list_gauge1")))
                   ),
          fluidRow(column(4, uiOutput(outputId = "hot_list2")),
                   column(8, withSpinner(gaugeOutput("hot_list_gauge2")))
                   )
          ),
  tabItem(tabName = "prediction",
          h2("Forecast"),
          withSpinner(plotOutput("forecast_hot1")),
          withSpinner(plotOutput("forecast_hot2")))
)
)
