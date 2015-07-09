# openDream

I've been seeing a whole lot of pastebin on reddit lately and it's getting ridiculous. It's getting about time we get more organized. So, I've taken the liberty of making a centralized github page for individuals playing around and/or experimenting to put their code. Message SlimeQ (or another owner) here or on reddit if you want to be added to the deepdream-community organization and/or contribute. I have basically no idea how organizations work on here, so feel free to make suggestions or help out in any way. 

For starters, I'm adding a modularized version of the original Python code from Google and an opticalflow flow script that I found randomly on reddit yesterday that is *very* cool.

## Scripts
### deepdream.py
This is where the magic happens. Do not run this directly! It should only be imported into another script like

    import deepdream

or

    import deepdream as dd
  
or

    from deepdream import showarray, preprocess, deprocess, make_step, deepdream, net
    
All the heavy lifting is done here, or at least should be done here.

### basic.py
This basically just wraps deepdream.py and it mostly came from the google sample. Additionally it adds much needed argument support.

### opticalflow.py
This is a script I found posted on reddit once. I've never used it, but in theory it makes a smooth video out of deepdream output and it is really damn cool. If anyone knows who wrote this, they should really be credited here.

### tryallblobs.py
This one was written by reddit's legendary Cranial_Vault and it basically just tries all possible dream types on an image. Should be modified to import deepdream.py so we don't have lots of versions of those functions running around.


More to come, hopefully. Hop on board!
