sidebar <- dashboardSidebar(
  sidebarMenu(id = "sidebar",
              menuItem("Hot List", 
                       tabName = "hot_list",
                       icon = icon("free-code-camp")),
              menuItem("Timeseries", 
                       tabName = "timeseries"
                       , icon = icon("line-chart")
                       ),
              menuItem("Correlation",
                       tabName = "correlation",
                       icon = icon("area-chart")),
              menuItem("Prediction",
                       tabName = "prediction",
                       icon = icon("bullseye"))
              )
  )

