# a-star-shortest-path
given a map terrain, the tool finds the shortest path to the destination using A* algorithm

### Cost Function
The cost function of a pixel is the attribute used to sort the elements in the queue
based on priority. The pixel with the lowest cost is put at the top of the queue so 
it can be searched immediately in the next round. </br>

The cost function was calculated by getting the distance 
from the start target to the current pixel location (gScore(pixel)) 
and adding it to the heuristic value of the current pixel (h(pixel)).

### Heuristic Function
The heuristic value of a pixel is calculated by how far that pixel is from the next target
on our route. It is simply the Euclidian distance between the 3d coordinates of the
current pixel and the next target. 

It also adds a penalty based on the type of terrain the current pixel is on. 
Lakes/Swamps/Marshes/Impassable vegetation have the highest penalty
which puts them in the queue as low-priority locations. This penalty ensures that
easy terrains will be prioritized in the search compared to other rougher terrains. 

This type of heuristic function in addition to the pixel's g score will ensure
a faster search by looking at pixels closest to the targets.

![image](https://github.com/gin7018/a-star-shortest-path/assets/79063763/eb95aa99-ac19-4751-be26-6422a46ecaa2)

