# DXF-to-SVG-Converter
_Utility to convert .DXF files from OnShape to .SVG files to use with Glowforge Laser Cutter_


**1. GET DXF FILE FROM ONSHAPE**
  * Create CAD file in [OnShape](https://cad.onshape.com/)
  * Click on the face of the part (or whole sketch) that you want to export
  * Click ```Export as DWG/DXF```
  * Save as .DXF file
       
**2. CONVERT TO .SVG FILE**
  * Go to online [DXF-to-SVG Converter](https://etech-svg.streamlit.app/)
  * Choose the default units from the OnShape file as ```inches``` or ```mm```
  * Upload ```.svg``` file
  * Download ```.svg``` file
    
**3. RUN .SBP FILE ON SHOPBOT**
  * Open [Glowforge Software](https://app.glowforge.com)
  * Log in with provided username & password
  * Upload ```.svg``` file
  * Setup cut & run machine

