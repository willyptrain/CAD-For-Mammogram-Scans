import random as rand
import matplotlib.pyplot as plt


class Line: 
   def __init__(self, m, b): 
      self.m = m
      self.b = b
      
lines = []
costsOverTime = []
xStr = "4 9 10 14 4 7 12 22 1 3 8 11 5 6 10 11 16 13 13 10"
yStr = "390 580 650 730 410 530 600 790 350 400 590 640 450 520 690 690 770 700 730 640"

x = map(float,xStr.split(" "))
y = map(float,yStr.split(" "))
def generateGenePool(Line1): 
   lines.append(Line1)
   for i in range(0, 500): 
      lines.append(Line(rand.randint(0,1000), rand.randint(0,1000)))


def getFittest(): 
   costOfLines = []
   avgCost = 0
   for i in lines:
      for c in range(0,len(x)): 
         guess = i.m*c + i.b
         avgCost = avgCost + (guess-y[c])
      costOfLines.append(abs(avgCost/len(x)))
      avgCost = 0
   lowestCost = costOfLines[0]
   lowestCostIndex = 0
   for i in range(0, len(costOfLines)): 
      if(costOfLines[i] < lowestCost): 
         lowestCost = costOfLines[i]
         lowestCostIndex = i
   costsOverTime.append(lowestCost)
   return Line(lines[lowestCostIndex].m,lines[lowestCostIndex].b)
   
def evolve(): 
   generateGenePool(Line(0,0))
   fittest = getFittest()
   iter = 0
   while(iter < 500): 
      iter += 1
      print(iter)
      generateGenePool(fittest)
      fittest = getFittest()
   return Line(getFittest().m,getFittest().b)
   
if __name__ == '__main__':
   fittest = evolve()
   #plt.xlim(0,30)
   #plt.ylim(300,800)
   #plt.scatter(x,y)
   #plt.plot([1, 22], [(fittest.m+fittest.b), ((fittest.m*22)+fittest.b)], 'k-', lw=2)
   #plt.show()
   print(costsOverTime)
   plt.plot(costsOverTime)
   plt.show()