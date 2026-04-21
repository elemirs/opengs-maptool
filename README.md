<img width="350" height="350" alt="ogs-mt-logo" src="https://github.com/user-attachments/assets/d03854c8-c2e1-468f-9f8a-269f498d169c" />

# Open Grand Strategy - Map Tool (Modern Version)

> **Credit & Acknowledgement**: This repository is a modernized fork and enhancement of the original [OpenGS Maptool by Thomas-Holtvedt](https://github.com/Thomas-Holtvedt/opengs-maptool). We've built upon their fantastic core algorithms!

The OpenGS Map Tool is a specialized utility designed to streamline the creation of map data for use in grand strategy games. Province and territory maps form the backbone of these games, defining the geographical regions that players interact with.

## ✨ New in this Version: "Liquid Glass" Modernization
- **Liquid Glass GUI**: A completely redesigned, dark-themed, sleek UI with smooth interactions and a wizard-style workflow.
- **Smart Paint System (Boundary-Only Mode)**: You no longer need separate sea and boundary images. Upload a single B/W boundary map, click on the sea areas using the new Smart Paint System, and let the tool automatically flood-fill and generate regions intelligently!
- **Internationalization (i18n)**: Fully supports **English and Turkish**, changing the entire UI dynamically via the language button.
- **In-App Modal Alerts**: Removed clunky Windows pop-ups in favor of smooth, centered, glass-pane styled overlay warnings.

## Features
- Generate and Export province maps
- Generate and Export province data
- Generate and Export territory maps
- Generate and Export territory data
- Density image support for controlling province/territory distribution
- Lake support — lakes are automatically detected and become individual provinces
- Exclude ocean from density influence per generation step
- Jagged borders — optional natural-looking borders for land and ocean regions
- Terrain system — import a terrain image to assign terrain types to provinces

## Showcase
Output territory Map:
![example](/example_output/territores.png)
Output Province Map:
![example2](/example_output/provinces.png)


## How to install
### Option 1 (Windows only):
1. "Releases" section in Github
2. Download and unpack "ogs_maptool.zip"
3. Run the Executable

### Option 2:
1. Clone the repository
2. Download the necessary libraries by running `pip install -r requirements.txt` in your terminal, inside the project directory.
3. Start project by running `python main.py`

## How to use the tool

### Smart Paint System (Only Land)
If you choose the **"Only Land"** mode on the welcome screen, you only need to provide a single Black/White map representing your borders.
- Click the sea/ocean areas with your left mouse button to paint them blue.
- If you don't paint any sea, all areas are treated as land.

### Land Image (Standard Setup)
The first tab takes an image that specifies the ocean and lake areas of the map.
- **Ocean** must be RGB color (5, 20, 18)
- **Lakes** must be RGB color (0, 255, 0)
- Everything else is considered land

See examples in the folder "example_input".

### Boundary Image
The boundary map defines the bounds that the provinces and territories need to adhere to. The boundary borders must be pure black, RGB (0, 0, 0), everything else will be ignored.

### Density Image
Allows you to import a density image that controls how provinces and territories are distributed. Darker areas attract more seeds, resulting in smaller and denser regions. A normalize preset and an equator distribution preset are available. The "Exclude Ocean" checkboxes let you ignore the density image for ocean regions.

### Terrain Image
Allows you to import a terrain image that assigns terrain types to provinces after generation.
Each pixel color maps to a specific terrain type. 

### Territory Image
Generates the territory map based on your boundary/land maps. Use the sliders to adjust the number of territories on land and ocean. Check "Jagged Land Borders" to produce natural-looking, irregular borders instead of straight Voronoi edges. Territory map and definitions can be exported from this screen.

### Province Image
Generates the province map by subdividing the generated territories. Use the sliders to adjust the number of provinces on land and ocean. Lakes are automatically detected. Province maps, province data files, and history files can be exported from this section.

## Contributions
Contributions can come in many forms and all are appreciated: Feedback, Code improvements, Added functionality.

## Discord 
Follow and/or support the project on [OpenGS Discord Server](https://discord.gg/6pRc9f6g6S)

## Delivered and maintained by 
<img width="350" height="350" alt="gsi-logo" src="https://github.com/user-attachments/assets/e7210566-7997-4d82-845e-48f249d439a0" />
