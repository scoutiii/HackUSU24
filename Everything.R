rm(list=ls())

ground<-read.csv("GroundContacts.csv", header=T)
plan<-read.csv("ManeuverPlan.csv")
payload<-read.csv("Payloadevents.csv")
rpoplan<-read.csv("Rpoplan.csv")

d1<-read.csv("ManeuverBranchId1.csv")
d2<-read.csv("ManeuverBranchId2.csv")
d3<-read.csv("ManeuverBranchId3.csv")
d4<-read.csv("ManeuverBranchId4.csv")
d5<-read.csv("ManeuverBranchId5.csv")
d6<-read.csv("ManeuverBranchId6.csv")
d7<-read.csv("ManeuverBranchId7.csv")
d8<-read.csv("ManeuverBranchId8.csv")
d9<-read.csv("ManeuverBranchId9.csv")
d10<-read.csv("ManeuverBranchId10.csv")
d11<-read.csv("ManeuverBranchId11.csv")
d12<-read.csv("ManeuverBranchId12.csv")
d13<-read.csv("ManeuverBranchId13.csv")
d14<-read.csv("ManeuverBranchId14.csv")
d15<-read.csv("ManeuverBranchId15.csv")
d16<-read.csv("ManeuverBranchId16.csv")
d17<-read.csv("ManeuverBranchId17.csv")
d18<-read.csv("ManeuverBranchId18.csv")
d19<-read.csv("ManeuverBranchId19.csv")
d20<-read.csv("ManeuverBranchId20.csv")
d21<-read.csv("ManeuverBranchId21.csv")
d22<-read.csv("ManeuverBranchId22.csv")
d23<-read.csv("ManeuverBranchId23.csv")
d24<-read.csv("ManeuverBranchId24.csv")
d25<-read.csv("ManeuverBranchId25.csv")
d26<-read.csv("ManeuverBranchId26.csv")
d27<-read.csv("ManeuverBranchId27.csv")
d28<-read.csv("ManeuverBranchId28.csv")
d29<-read.csv("ManeuverBranchId29.csv")
d30<-read.csv("ManeuverBranchId30.csv")
d31<-read.csv("ManeuverBranchId31.csv")
d32<-read.csv("ManeuverBranchId32.csv")
d33<-read.csv("ManeuverBranchId33.csv")
d34<-read.csv("ManeuverBranchId34.csv")
d35<-read.csv("ManeuverBranchId35.csv")
d36<-read.csv("ManeuverBranchId36.csv")
d37<-read.csv("ManeuverBranchId37.csv")
d38<-read.csv("ManeuverBranchId38.csv")
d39<-read.csv("ManeuverBranchId39.csv")
d40<-read.csv("ManeuverBranchId40.csv")
d41<-read.csv("ManeuverBranchId41.csv")
d42<-read.csv("ManeuverBranchId42.csv")
d43<-read.csv("ManeuverBranchId43.csv")
d44<-read.csv("ManeuverBranchId44.csv")
d45<-read.csv("ManeuverBranchId45.csv")

data_set<-rbind.fill(d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14,d15,d16,d17,d18,d19,d20,d21,d22,d23,d24,d25,d26,d27,d28,d29,d30,d31,d32,d33,d34,d35,d36,d37,d38,d39,d40,d41,d42,d43,d44,d45,d46,d47)
d46<-read.csv("ManeuverBranchId46.csv")

par(mfrow=c(2, 2))
plot(rpoplan$secondsSinceStart,rpoplan$positionDepRelToChiefEciX)
plot(rpoplan$secondsSinceStart,rpoplan$positionDepRelToChiefEciY)
plot(rpoplan$secondsSinceStart,rpoplan$positionDepRelToChiefEciZ)
plot(rpoplan$secondsSinceStart,rpoplan$relativeRange)

install.packages("plotly")
library(plotly)

# Create a 3D scatter plot
plot_ly(x = rpoplan$positionDepRelToChiefEciX, y = rpoplan$positionDepRelToChiefEciY, z = rpoplan$positionDepRelToChiefEciZ, type = "scatter3d", mode = "markers")
plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers")
plot_ly(x = rpoplan$attitudeDeputyEci2BodyQx, y = rpoplan$attitudeDeputyEci2BodyQz, z = rpoplan$attitudeDeputyEci2BodyQz, type = "scatter3d", mode = "markers")
plot(rpoplan$secondsSinceStart,sqrt(rpoplan$positionDepRelToChiefLvlhZ^2 + rpoplan$positionDepRelToChiefLvlhY^2 + rpoplan$positionDepRelToChiefLvlhX^2))
plot(rpoplan$secondsSinceStart,rpoplan$storedData)
plot_ly(x = rpoplan$secondsSinceStart, y = rpoplan$positionDepRelToChiefLvlhZ, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers")

plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers",marker = list(color = rpoplan$secondsSinceStart, colorscale = "Viridis", size = 5))
plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers",marker = list(color = rpoplan$sensorAngleToSun, colorscale = "Viridis", size = 5))
plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers",marker = list(color = rpoplan$sensorAngleToMoon, colorscale = "Viridis", size = 5))
plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers",marker = list(color = rpoplan$relativeVelocity, colorscale = "Viridis", size = 5))
plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers",marker = list(color = rpoplan$storedData, colorscale = "Viridis", size = 5))


check_conditions <- function(x) {
  # Check if all conditions are met for the current row
  bool1<-FALSE
  for (i in 1:nrow(ground)) {
    # Check if conditions are met for the current row
    if (ground$startSeconds[i] <= x && x <= ground$stopSeconds[i])
    {
      bool1<-TRUE
    }
  }
  return(bool1)
}

plot_ly(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "markers",marker = list(color = colors, colorscale = "Viridis", size = 5))

bool1 <- (5980 <= rpoplan$secondsSinceStart)

#do this first
check_conditions <- function(x) {
  # Check if any condition is met for the current x value
  for (i in 1:nrow(ground)) {
    # Check if x is between startSeconds and stopSeconds
    if (ground$startSeconds[i] <= x && x <= ground$stopSeconds[i]) {
      if (ground$groundSite[i] == 1)
        return("50")
      else if (ground$groundSite[i] == 2)
        return("100")
      else if (ground$groundSite[i] == 3)
        return("150")
      else
        return("200")
    }
  }
  return(0)
}

# Apply the check_conditions function to each element of rpoplan$secondsSinceStart
colors <- sapply(rpoplan$secondsSinceStart, function(x) check_conditions(x))

#do this second                 
# Define custom color palette for each category
category_colors <- c("0" = "black", "50" = "#1b9e77", "100" = "#d95f02", "150" = "#7570b3", "200" = "#e7298a")

#do this third
# Map the 'category' column to colors
colors <- category_colors[sapply(rpoplan$secondsSinceStart, function(x) check_conditions(x))]

# Create a 3D scatter plot
plot <- plot_ly(type = "scatter3d", mode = "markers")

# Add first set of points (first 3D graph)
plot <- plot %>% add_trace(x = d40$positionDepRelToChiefLvlhZ, y = d40$positionDepRelToChiefLvlhY, z = d40$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "lines", line = list(colors = d40$relativeRange, colorscale = "Viridis", width = 5))

# Add second set of points (second 3D graph)
plot <- plot %>% add_trace(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "lines", line = list(color = colors, opacity = 0, width = 5))

# Show the plot
plot

d47<-read.csv("ManeuverBranchId47.csv")

list.files(pattern=".csv")

# Create an empty plot
plot <- plot_ly()

# Loop through the datasets d1 to d40
for (i in 1:47) {
  # Dynamically access the dataset name (e.g., d1, d2, ..., d47)
  dataset <- get(paste0("d", i))
  
  # Add the trace for each dataset to the plot
  plot <- plot %>% add_trace(
    x = dataset$positionDepRelToChiefLvlhZ,
    y = dataset$positionDepRelToChiefLvlhY,
    z = dataset$positionDepRelToChiefLvlhX,
    type = "scatter3d",
    mode = "lines",
    line = list(color = dataset$relativeRange, colorscale = "Viridis", width = 5)
  )
}

plot <- plot %>% add_trace(x = rpoplan$positionDepRelToChiefLvlhZ, y = rpoplan$positionDepRelToChiefLvlhY, z = rpoplan$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "lines", line = list(color = colors, opacity = 0, width = 5))

# Show the plot
plot

#do this fourth
plot_single <- function(x) {
  data1 <- get(paste0("d", x))
  data <- rpoplan[which(rpoplan$secondsSinceStart > data1$secondsSinceStart[1] - 12000 & rpoplan$secondsSinceStart < data1$secondsSinceStart[1]),]
  return(data)
}

data2 <- plot_single(46)
data3 <- get(paste0("d", 46))
plot <- plot_ly()
plot <- plot %>% add_trace(x = data2$positionDepRelToChiefLvlhZ, y = data2$positionDepRelToChiefLvlhY, z = data2$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "lines",line = list(color = colors, width = 5))
plot <- plot %>% add_trace(x = data3$positionDepRelToChiefLvlhZ, y = data3$positionDepRelToChiefLvlhY, z = data3$positionDepRelToChiefLvlhX, type = "scatter3d", mode = "lines", line = list(color = -data3$relativeRange, colorscale = "Viridis", width = 5))
plot
