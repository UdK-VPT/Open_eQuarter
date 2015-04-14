library(shiny)

building_group_menu=as.list(BLD_GROUPS)
names(building_group_menu)<-as.vector(VERBOSE[BLD_GROUPS,]$title,mode="character")


# Define UI for miles per gallon application
shinyUI(pageWithSidebar(
  
  # Application title
  headerPanel("Miles Per Gallon"),
  
  # Sidebar with controls to select the variable to plot against mpg
  # and to specify whether outliers should be included
   sidebarPanel(),
  
  mainPanel(width = 6,
            selectInput("variable", "Variable:",
                        building_group_menu, width = 350),
 
             
            selectInput("variable", "Variable:",
                        list("POPULATION" = "pop", 
                             "BUILDINGS" = "build")) ,
            
            
            checkboxInput("outliers", "Show outliers", FALSE)
  )
))
