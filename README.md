# TarkovAutoSell2.1

Heya, this requires EFT (Escape From Tarkov to be open)
Currently functionally complete, but not to my inital goals.

I made this due to the act of selling stuff to the flea market after every raid is monotonous, formulaic and long - thus a perfect candidate to be automized!

This uses computer vision (numpy) to object-match with various hard-coded portions of the screen, thus we can use python libraries to move the mouse and navigate the on-game ui.

I used tkinter to make a rudimentary GUI, but interestingly this requires takes up the attention of a process (going back I realise threading would be better, since in this case it's purely I/O bound), since the UI is essentially a While loop listening for events: button presses etc, so I used the multiprocessing module to run computervision functions and mouse-movement recording functions simultaneous to running the GUI.

A big portion of time in this project was spent in making 'authentic mouse-movement' which couldn't be discerned from a human. I soon realised that this wasn't actually practical,
since anti-cheat would be looking at processes running in the background, or other methods, however the idea/solutions I thought of still proved fun and interesting to implement
thus I went ahead regardless.

I introduced degrees of randomness, aswell as an 'evolve' function that would change mouse movements, so they would be undiscernable from bots, but they would be slightly 
different each time - it was interesting creating a function that would preserve the general curvature of a mouse movement, but also be open to slowly modulate from 
1 stationary point > 2 stat. point; so I created a function that split the curve into N segments and calculated a deviation factor: deviationFactor = sum(N)/(N*deviationMedian),
and iterated multiple times. Unfortunately there was issues that required a big overhaul of mouse-movements or the EvoleCurve function.

Essentially, I combining a linearly-spaced dataset with a non-linearly spaced dataset, since I was splitting my curve in N equal distant segments and then calculating a 
devaiation factor at each segment, whereas the datapoints of the curve formed by - due to the rudimentary way of forming mouse movements purely from (x,y) co-ordinates with a constant polling rate, therefore for fast/slow arcs of mouse movements the datapoints are unevenly spaced apart. Sadly this required a hefty overhaul of either how I recorded mouse movements, or (more likely) reworking the function iterate over datapoints as opposed to linearly spaced pre-defined segments.

Well the bot was still functional - it does require EFT to be open which is a little lazy. 


