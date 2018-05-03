
import nltk

texts = []

# TC1 
texts.append("Build a tower of height 5 at coordinate (0,1) with red block as the first block and black block as the last block.")
texts.append("Build a tower of height 5 at coordinates (0,1) with red block as the first block and black block as the last.")

texts.append("Build a tower of height 5 at coordinates (0,1) with a red block as the first block and a black block as the last block.")
texts.append("Build a tower of height 5 at coordinates (0,1) with a red block as the first block and a black block as the last.")

texts.append("A tower of height 5 at coordinates (0,1) with a red block as the first block and a black block as the last block.")

# abbv of height used
texts.append("A tower of ht 5 at coordinates (0,1) with a red block as the first block and a black block as the last block.")

texts.append("A tower 5 blocks tall at coordinates (0,1) with a red block at the bottom and black block at the top.")

texts.append("Red block at the bottom and black block at the top in a tower 5 blocks tall at coordinates (0,1).")

texts.append("Red block at the bottom, black block at the top in a tower 5 blocks tall at coordinates (0,1).")

texts.append("A tower five blocks tall at coordinates (0,1) with a red block as the first block and a black block as the last block.")

texts.append("A tower 5 blocks tall at coordinates (0,1) with a red block in position 0 and a black block in position 4.")

texts.append("A tower 5 blocks tall at coordinates (0,1) with a red block in 0th position and a black block in last position.")

texts.append("A tower 5 blocks tall at coordinates (0,1) with a red block in 0th position and a black block in 4th position.")

texts.append("A tower 5 blocks tall at coordinates (0,1) with a red block in 0th position, a black block in 4th position and any block at other positions.")

texts.append("A tower 5 blocks tall at coordinates (0,1) with a red block in 0th position, a black block in 4th position and block of any color at other positions.")

texts.append("A tower 5 blocks tall at coordinates 0,1 with a red block in 0th position, a black block in 4th position and block of any color at other positions.")

texts.append("A tower 5 blocks tall at any coordinates with a red block in 0th position, a black block in 4th position and block of any color at other positions.")

#TC#2
texts.append("A tower of height 2 at coordinate (0,0) with a black block above a red block")
texts.append("A tower 2 blocks tall at coordinate (0,0) with a black block above a red block")
texts.append("A tower of height 2 at coordinate (0,0) with a red block below a black block")
texts.append("A tower 2 blocks tall at coordinate (0,0) with a red block below a black block")

texts.append("A tower of height 2 at coordinate (0,0) with a red block at bottom and a black block at the top")
texts.append("A tower 2 blocks tall at coordinate (0,0) with a red block at bottom and a black block at the top")

texts.append("A tower of height 2 at coordinate (0,0) with a black block at the top and a red block at the bottom")
texts.append("A tower 2 blocks tall at coordinate (0,0) with a black block at the top and a red block at the bottom")

texts.append("A tower at coordinate (0,0) with red block at position 0 and black block at position 1")

texts.append("A tower with red block at position 0 and black block at position 1 and at coordinate (0,1)")

#TC#2 variant
texts.append("A tower of height 2 at coordinate (0,0) with red and black block")
texts.append("A tower of height 2 at coordinate (0,0) with a red block and a black block")
texts.append("A tower at coordinate (0,0) with a red block and a black block")
texts.append("A tower with a red block and a black block and at coordinate (0,0)")


# TC3 covered in following
texts.append("A tower seventeen blocks tall at any coordinate.")
texts.append("A tower 17 blocks tall at any coordinate.")

texts.append("A tower seventeen blocks tall at any position in xz plane.")
texts.append("A tower 17 blocks tall at any position in xz plane.")

texts.append("A tower anywhere and seventeen blocks tall.")
texts.append("A tower anywhere and 17 blocks tall.")

texts.append("A tower anywhere and with height seventeen.")
texts.append("A tower anywhere and with height 17.")

texts.append("A tower anywhere with seventeen blocks.")
texts.append("A tower anywhere with 17 blocks.")

texts.append("A tower with seventeen blocks and anywhere.")
texts.append("A tower with 17 blocks and anywhere.")

texts.append("Seventeen blocks stacked together anywhere.")
texts.append("17 blocks stacked together anywhere.")

texts.append("Any seventeen blocks stacked together anywhere.")
texts.append("Any 17 blocks stacked together anywhere.")

texts.append("Any seventeen blocks stacked together in a tower anywhere.")
texts.append("Any 17 blocks stacked together in a tower anywhere.")

texts.append("Seventeen blocks stacked one above another at any position in xz plane.")
texts.append("17 blocks stacked one above another at any position in xz plane.")

texts.append("Seventeen blocks in a tower at any position in xz plane.")
texts.append("17 blocks in a tower at any position in xz plane.")

texts.append("Anywhere build a tower seventeen blocks tall.")
texts.append("Anywhere build a tower 17 blocks tall.")

texts.append("Build a tower seventeen blocks tall anywhere.")
texts.append("Build a tower 17 blocks tall anywhere.")

texts.append("Build a tower of height seventeen anywhere.")
texts.append("Build a tower of height 17 anywhere.")

texts.append("Build a tower with seventeen blocks anywhere.")
texts.append("Build a tower with 17 blocks anywhere.")

texts.append("Build a tower with seventeen blocks.")
texts.append("Build a tower with 17 blocks.")

texts.append("Build a tower with seventeen blocks at any position in xz plane.")
texts.append("Build a tower with 17 blocks at any position in xz plane.")

texts.append("Build a tower anywhere with seventeen blocks.")
texts.append("Build a tower anywhere with 17 blocks.")

texts.append("Build a tower anywhere and with seventeen blocks.")
texts.append("Build a tower anywhere and with 17 blocks.")

texts.append("Build a tower at any position in xz plane and with seventeen blocks.")
texts.append("Build a tower at any position in xz plane and with 17 blocks.")

texts.append("Build a tower at any position in xz plane and with seventeen blocks.")
texts.append("Build a tower at any position in xz plane and with 17 blocks.")

def posTag():
    
    taggedTexts = {}

    for text in texts:
        taggedTexts[text] = nltk.pos_tag(nltk.word_tokenize(text))

    for text in texts:
        print(taggedTexts[text])
        print()