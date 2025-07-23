# AIVtoAIVJsonConverter <!-- omit in toc -->
This tool allows you to convert .aiv files to .aivjson files. This also works for bedouin lords with a small workaround.

# Table of Contents <!-- omit in toc -->

- [Description](#description)
- [Instructions to use the tool](#instructions-to-use-the-tool)
- [Requiered Libaries](#requiered-libaries)
- [Credits](#credits)

# Description
Convert your created castle to the Definitive Edition!

Tool features:
- convert .aiv files to .aivjson files
- convert "apple farm" to "bedouin stockade" for bedouin lords
- convert chosen units to bedouin units for bedouin lords

Under [aiv/IIJanII_aivs](src/aiv/IIJanII_aivs) you will find my created Castles, one for each old lord. With them works the conversion fine.

This tool was tested on windows. For mac or linux users there might be some issues.

# Instructions to use the tool
Click "Browse..." and select the AIV files you wish to convert to .aivjson. The default folder ist "aiv", but you can browse for your own folder. Optionally, you can specify a save folder where the new files will be stored; otherwise, the converted files will be saved in the folder "aivjson".

Since the old AIV Editor doesn't support the new Bedouin units, there's a small workaround for Bedouin Lords: In the AIV Editor, place an "apple farm" where you want to position the "Bedouin stockade". For the units, place a placeholder unit (for example, knights) where you intend the Bedouin units to be placed. Then click the "+" inside the tool and map the placeholder unit to the desired Bedouin unit. Currently, only two Bedouin units have been identified (Nomad uses Skirmisher and Kahin uses Eunuchs if you start with many troops. Technically, sentinel7.aivjson contains a new unit, but i will not be placed. Could be Demolishers or Healers).<br><br>You can find the link to the old AIV Editor <a href='http://stronghold.heavengames.com/downloads/getfile.php?id=7534&dd=1&s=0d0177bca23f6e96037b2db2b895c38f'>here</a>.

# Requiered Libaries
- [sourcehold-maps](https://github.com/sourcehold/sourcehold-maps)
- Pillow
- dclimplode
- numpy
- build
- opencv-python
- pyqt6

Install all needed libraries at once:
```console
pip install -r requirements.txt
```
# Credits
Special thanks to gynt and his team from "Sourcehold"! They did the most work decoding the .aiv files. See [Sourcehold](https://github.com/sourcehold/sourcehold-maps) for more information.

Thanks also to the UCP team, from where I got the inspiration for the design. Visit them here: [UCP](https://unofficialcrusaderpatch.github.io)

And thanks to Firefly for developing the Stronghold Crusader Definitive Edition!
