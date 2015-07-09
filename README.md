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

### main.py
This basically just wraps deepdream.py and it mostly came from the google sample. Additionally it adds much needed argument support. The current options are as follows

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('-o', '--outputdir', default='out', type=str)
    parser.add_argument('-s', '--scaleCoef', default=0.05, type=float)
    parser.add_argument('-i', '--iterations', default=100, type=int)
    parser.add_argument('-a', '--blob', default=blobs.rand(), type=str)
    args = parser.parse_args()
    
filename is the only one that's required at this time. blob sets to a random blob by default, or dreams once on all blobs if set to all (this was previously done by tryallblobs.py).

### opticalflow.py
This is a script I found posted on reddit once. I've never used it, but in theory it makes a smooth video out of deepdream output and it is really damn cool. If anyone knows who wrote this, they should really be credited here.

### tryallblobs.py
This one was written by reddit's legendary Cranial_Vault and it basically just tries all possible dream types on an image. Should be modified to import deepdream.py so we don't have lots of versions of those functions running around.

DELETED: This function has been merged into main.py. Instead, run

    $ python main.py -f source/file.jpg --blob all

More to come, hopefully. Hop on board!
