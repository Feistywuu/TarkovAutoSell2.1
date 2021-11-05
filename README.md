# TarkovAutoSell2.1

Heya, this requires EFT (Escape From Tarkov to be open)
Currently functionally complete, but not to my inital goals.

I made this due to the act of selling stuff to the flea market after every raid is monotonous, formulaic and long - thus a perfect candidate to be automized!

This uses computer vision (numpy) to object-match with various hard-coded portion of the screen, thus we can use python libraries to move the mouse 

A big portion of time in this project was spent in making 'authentic mouse-movement' which couldn't be discerned from a human. I soon realised that this wasn't actually practical,
since anti-cheat would be looking at processes running in the background, or other methods, however the idea/solutions I thought of still proved fun and interesting to implement
thus I went ahead regardless.

I introduced degrees of randomness, aswell as an 'evolve' function that would change mouse movements, so they would be undiscernable from bots, but they would be slightly 
different each time - it was interesting creating a function that would preserve the general curvature of a mouse movement, but also be open to slowly modulate from 
1 stationary point > 2 stat. point; so I created a function that split the curve into N segments and calculated a deviation factor: deviationFactor = sum(N)/(N*deviationMedian),
and iterated multiple times. Unfortunately there was issues that required a big overhaul of mouse-movements or the EvoleCurve function.

Essentially, I combining a linearly-spaced dataset with a non-linearly spaced dataset, since I was splitting my curve in N equal distant segments and then calculating a 
devaiation factor at each segment, whereas the datapoints of the curve formed by - due to the rudimentary way of forming mouse movements purely from (x,y) co-ordinates with a constant time

I did 

