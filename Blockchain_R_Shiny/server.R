server <- function(input, output, session) {
  
  prices_filt <- reactive({
    names <- c(input$hot_list_name1, input$hot_list_name2)
    df <- prices %>% 
      dplyr::filter(currency_name %in% names)
    df
  })  
  
  output$currency_names_ui <- renderUI({
    parameter <- prices$currency_name %>% unique()
    parameter_list <- as.list(parameter)
    names(parameter_list) <- parameter
    selectizeInput(inputId = "currency_name", 
                   multiple = T,
                   selected = c("bitcoin","ethereum"),
                   label = "Crypto Currency", 
                   choices = parameter_list)
  })
  
  output$hot_list1 <- renderUI({
    parameter <- prices$currency_name %>% unique()
    parameter_list <- as.list(parameter)
    names(parameter_list) <- parameter
    selectizeInput(inputId = "hot_list_name1", 
                   multiple = F,
                   selected = "bitcoin",
                   label = "Crypto Currency", 
                   choices = parameter_list)
  })
  
  
  output$hot_list2 <- renderUI({
    parameter <- prices$currency_name %>% unique()
    parameter_list <- as.list(parameter)
    names(parameter_list) <- parameter
    selectizeInput(inputId = "hot_list_name2", 
                   multiple = F,
                   selected = "ethereum",
                   label = "Crypto Currency", 
                   choices = parameter_list)
  })
  
  currency_article_nr <- reactive({
    df <- bcm_text %>% 
      dplyr::filter (grepl(pattern = input$hot_list_name1[1], x = body)) %>% 
      dplyr::group_by(timestamp) %>% 
      dplyr::mutate(count = length(grep(pattern = input$hot_list_name1[1], x = body)))
    df
    })
  
  currency_sentiment <- reactive({
    df <- bcm_text %>% 
      dplyr::filter (grepl(pattern = input$hot_list_name1[1], x = body)) %>% 
      dplyr::mutate(count = length(grep(pattern = input$hot_list_name1[1], x = body))) %>% 
      dplyr::filter (count > 2) %>% 
      group_by(timestamp) %>% 
      unnest_tokens(output = word, input = body) %>% 
      ungroup() %>% 
      anti_join(stop_words) %>% 
      inner_join(sentiments, by = "word")  
    df$sentiment[df$sentiment == "positive"] <- 1
    df$sentiment[df$sentiment == "negative"] <- -1
    df <- df %>% 
      dplyr::group_by(timestamp) %>% 
      dplyr::summarise (sentiment_count = n(),
                        sentiment_diff = sum(as.numeric(sentiment), na.rm=T),
                        sentiment_ratio = sentiment_diff / sentiment_count)
    df
  })
  
  price_currency_sentiment <- reactive({
    df <- prices_filt() %>%
      dplyr::filter(currency_name == input$hot_list_name1[1]) %>% 
      left_join(currency_sentiment(), by = "timestamp") 
    df$return <- NA
    n <- nrow(df)
    df$return[2:n] <- (df$Close[2:n] - df$Close[1:(n-1)]) / df$Close[1:(n-1)]
    df
  })
  
  price_currency_commit <- reactive({
    df <- prices_filt() %>%
      dplyr::filter(currency_name == input$hot_list_name1[1]) %>% 
      left_join(commits, by = "timestamp") %>% 
      filter(!duplicated(timestamp))
    df$return <- NA
    n <- nrow(df)
    df$return[2:n] <- (df$Close[2:n] - df$Close[1:(n-1)]) / df$Close[1:(n-1)]
    df
  })
  
  
  price_currency_article <- reactive({
    df <- prices_filt() %>%
      dplyr::filter(currency_name == input$hot_list_name1[1]) %>% 
      left_join(currency_article_nr(), by = "timestamp") 
    df$return <- NA
    n <- nrow(df)
    df$return[2:n] <- (df$Close[2:n] - df$Close[1:(n-1)]) / df$Close[1:(n-1)]
    df
  })
  

  output$price_time_dygraph <- renderDygraph({
    if (length(input$currency_name) > 0) {
      name1 <- input$currency_name[1]
      curr_xts <- xts(x = prices$Close[prices$currency_name == name1], 
                       order.by = prices$timestamp[prices$currency_name == name1])
      colnames(curr_xts) <- name1
    }
    if (length(input$currency_name) > 1) {
      name2 <- input$currency_name[2]
      curr2_xts <- xts(x = prices$Close[prices$currency_name == name2], 
                       order.by = prices$timestamp[prices$currency_name == name2])
      curr_xts <- cbind(curr_xts, curr2_xts)
      colnames(curr_xts) <- c(name1, name2)
    }
    if (length(input$currency_name) > 2) {
      name3 <- input$currency_name[3]
      curr3_xts <- xts(x = prices$Close[prices$currency_name == name3], 
                       order.by = prices$timestamp[prices$currency_name == name3])
      curr_xts <- cbind(curr_xts, curr3_xts)
      colnames(curr_xts) <- c(name1, name2, name3)
    }      
    dygraph(data = curr_xts, 
            main = paste("Cryptocurrency Price Development of", c(colnames(curr_xts))), 
            xlab = "Time", 
            ylab = "Price Change [%]", 
            group = "linked_plot") %>% 
      dyRebase(value = 100) %>% 
      dyRangeSelector(dateWindow = c("2016-01-01", "2016-12-31")) %>% 
      dyLegend(show = "always", hideOnMouseOut = FALSE) %>% 
      dyHighlight(highlightCircleSize = 5, 
                  highlightSeriesBackgroundAlpha = 0.2,
                  hideOnMouseOut = FALSE)
  })
  
  output$curr_sent_dygraph <- renderDygraph({
    df <-currency_sentiment() %>% 
      left_join(currency_article_nr()) %>% 
      full_join(price_currency_commit())
      
    curr_sent_xts1 <- xts(df$sentiment_ratio*10, order.by = df$timestamp)
    curr_sent_xts2 <- xts(df$count * 2, order.by = df$timestamp)
    curr_sent_xts3 <- xts(df$value, order.by = df$timestamp)
    
    curr_sent_xts <- cbind(curr_sent_xts1, curr_sent_xts2, curr_sent_xts3)
    colnames(curr_sent_xts) <- c("Sentiments", "Articles-Count", "Commit-Count")
    dygraph(data = curr_sent_xts,
            main = paste("Sentiment/Articles/Github Commits on", isolate(input$hot_list_name1)),
            xlab = "Time",
            group = "linked_plot") %>% 
      dyAxis("y", label = "Sentiment/Articles [-]") %>%
      dyRangeSelector(dateWindow = c("2016-01-01", "2016-12-31")) %>% 
      dyRoller(rollPeriod = 5) %>% 
      dyHighlight(highlightCircleSize = 5, 
                  highlightSeriesBackgroundAlpha = 0.2,
                  hideOnMouseOut = FALSE) %>% 
      dyOptions(fillGraph = TRUE, fillAlpha = 0.4) 
  })

  output$price_sentiment_corr <- renderPlot(bg = "transparent", {
    df <- price_currency_sentiment()
    
    g <- ggplot(df, aes(return, sentiment_ratio))
    g <- g + geom_point()
    g <- g + geom_smooth(method = "lm", se = F)
    g <- g + coord_cartesian(ylim = c(-1, 1), xlim = c(-.2, .2))
    g <- g + labs (title = "Correlation for Sentiment and Returns", x = "Returns [-]", y = "Sentiment [-]")
    g <- g + theme(
      axis.text.x = element_text(colour="grey20",size=14,angle=90,hjust=.5,vjust=.5,face="plain"),
      axis.text.y = element_text(colour="grey20",size=14,angle=0,hjust=1,vjust=0,face="plain"),  
      axis.title.x = element_text(colour="grey20",size=14,angle=0,hjust=.5,vjust=0,face="plain"),
      axis.title.y = element_text(colour="grey20",size=14,angle=90,hjust=.5,vjust=.5,face="plain"),
      axis.title = element_text(colour="grey20",size=20,angle=0,hjust=.5,vjust=0,face="plain"),
      panel.background = element_blank(),
      plot.background = element_blank(),
      legend.background = element_blank()
    )
    g
  })
  
  
  output$price_article_corr <- renderPlotly( {
    article <- price_currency_article() %>% 
      rename(value = count) %>% 
      select(return, value)
    article$method <- "articles"
    commits <- price_currency_commit() %>% 
      select(return, value)
    commits$method <- "commits"
    sentiments <- price_currency_sentiment() %>% 
      rename (value = sentiment_ratio) %>% 
      select(return, value)
    sentiments$method <- "sentiment"
    df <- bind_rows(article, commits, sentiments)
    
    g <- ggplot(df, aes(x = return, y = value, col = method))
    g <- g + geom_point()
    g <- g + geom_smooth(method = "lm", se = F)
    g <- g + coord_cartesian(xlim = c(-.2, .2))
    g <- g + labs (title = "Correlation for Articles/Commits and Returns", x = "Returns [-]", y = "Sentiment [-]")
    g <- g + theme(
      axis.text.x = element_text(colour="grey20",size=14,angle=90,hjust=.5,vjust=.5,face="plain"),
      axis.text.y = element_text(colour="grey20",size=14,angle=0,hjust=1,vjust=0,face="plain"),  
      axis.title.x = element_text(colour="grey20",size=14,angle=0,hjust=.5,vjust=0,face="plain"),
      axis.title.y = element_text(colour="grey20",size=14,angle=90,hjust=.5,vjust=.5,face="plain"),
      axis.title = element_text(colour="grey20",size=20,angle=0,hjust=.5,vjust=0,face="plain"),
      panel.background = element_blank(),
      plot.background = element_blank(),
      legend.background = element_blank()
    )
    ggplotly(g)
  })
  
  output$price_commit_corr <- renderPlot(bg = "transparent", {
    df <- price_currency_commit()
    
    g <- ggplot(df, aes(return, value))
    g <- g + geom_point()
    g <- g + geom_smooth(method = "lm", se = F)
    g <- g + coord_cartesian(xlim = c(-.2, .2), ylim = c(0, 10))
    g <- g + labs (title = "Correlation for Nr. of Github Commits and Returns", x = "Returns [-]", y = "Github Commits [-]")
    g <- g + theme(
      axis.text.x = element_text(colour="grey20",size=14,angle=90,hjust=.5,vjust=.5,face="plain"),
      axis.text.y = element_text(colour="grey20",size=14,angle=0,hjust=1,vjust=0,face="plain"),  
      axis.title.x = element_text(colour="grey20",size=14,angle=0,hjust=.5,vjust=0,face="plain"),
      axis.title.y = element_text(colour="grey20",size=14,angle=90,hjust=.5,vjust=.5,face="plain"),
      axis.title = element_text(colour="grey20",size=20,angle=0,hjust=.5,vjust=0,face="plain"),
      panel.background = element_blank(),
      plot.background = element_blank(),
      legend.background = element_blank()
    )
    g
  })
  
  output$hot_list_gauge1 <- renderGauge({
    name1 <- input$hot_list_name1
    curr_xts <- xts(x = prices_filt()$Close[prices_filt()$currency_name == name1], 
                    order.by = prices_filt()$timestamp[prices_filt()$currency_name == name1])
    fit <- ets(curr_xts)
    value <- round((forecast(fit, 30)$mean[length(forecast(fit, 30)$mean)] / curr_xts[length(curr_xts)]-1) * 100, 1)
    gauge(value = value, min = -100, max = 100, label = "Pred. Return", symbol = "%",
          sectors = gaugeSectors(success = c(5, 100), warning = c(-5, 5), danger = c(-100, -5)))
  })
  
  
  output$hot_list_gauge2 <- renderGauge({
    name2 <- input$hot_list_name2
    curr_xts <- xts(x = prices_filt()$Close[prices_filt()$currency_name == name2], 
                    order.by = prices_filt()$timestamp[prices_filt()$currency_name == name2])
    fit <- ets(curr_xts)
    value <- round((forecast(fit, 30)$mean[length(forecast(fit, 30)$mean)] / curr_xts[length(curr_xts)]-1) * 100, 1)
    gauge(value = value, min = -100, max = 100, label = "Pred. Return", symbol = "%",
          sectors = gaugeSectors(success = c(5, 100), warning = c(-5, 5), danger = c(-100, -5)))
  })
  
  output$forecast_hot1 <- renderPlot({
    name1 <- input$hot_list_name1
    curr_xts <- xts(x = prices_filt()$Close[prices_filt()$currency_name == name1], 
                    order.by = prices_filt()$timestamp[prices_filt()$currency_name == name1])
    fit <- ets(curr_xts)
    plot(forecast(fit, 30), shaded = F, PI = F)
    
  })
  
  
  output$forecast_hot2 <- renderPlot({
    name2 <- input$hot_list_name2
    curr_xts <- xts(x = prices_filt()$Close[prices_filt()$currency_name == name2], 
                    order.by = prices_filt()$timestamp[prices_filt()$currency_name == name2])
    fit <- ets(curr_xts)
    plot(forecast(fit, 30), shaded = F, PI = F)
    
  })
}  # end server