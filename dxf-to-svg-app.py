import streamlit as st
import re
import io
import ezdxf
from ezdxf import recover, bbox
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing import svg, layout, config
from io import BytesIO

# Define team colors
TEAM_BLUE_HEX = "#002060" 
TEAM_GREEN_HEX = "#74B44C" 

# --- Configuration for Logo and Colors ---
st.markdown(f"""
<style>
    .st-emotion-cache-2trqyj {{
        color: {TEAM_BLUE_HEX};
    }}
    
    .stButton>button, .stDownloadButton>button {{
        background-color: {TEAM_GREEN_HEX} !important;
        border-color: {TEAM_GREEN_HEX} !important;
        color: white !important;
    }}
    
    .stButton>button:hover, .stDownloadButton>button:hover {{
        background-color: #5e923d !important;
        border-color: #5e923d !important;
        color: white !important;
    }}

    .stSuccess {{
        background-color: #E8F5E9;
        color: {TEAM_GREEN_HEX};
    }}
</style>
""", unsafe_allow_html=True)

# --- Interface Headings and Layout ---
col1, col2 = st.columns((1, 4))

with col1:
    try:
        # FIX: Explicitly using the new width syntax for the logo
        st.image("sparky_logo.png", width=100) 
    except FileNotFoundError:
        st.warning("Logo file 'sparky_logo.png' not found.")

with col2:
    st.title("Glowforge DXF to SVG File Converter")

st.markdown("Utility to convert .DXF files from OnShape to .SVG files to use with Glowforge Laser Cutter")
st.markdown("*See app code at [github.com/ETechChargers5298/DXF-to-SVG-Converter](https://github.com/ETechChargers5298/DXF-to-SVG-Converter)*")

# 1. Units Toggle
st.subheader(f"1. Choose Units")
unit_selection = st.radio("Select original .dxf units from OnShape:", ["Inches", "Millimeters"], horizontal=True)
scale_factor = 25.4 if unit_selection == "Inches" else 1.0

st.subheader(f"2. Upload DXF File")
uploaded_file = st.file_uploader("Select .dxf file from OnShape:", type="dxf")

if uploaded_file is not None:
    try:
        blob = uploaded_file.getvalue()
        doc, auditor = recover.read(BytesIO(blob))
        msp = doc.modelspace()
        
        ctx = RenderContext(doc)
        cfg = config.Configuration(
            background_policy=config.BackgroundPolicy.OFF,
            color_policy=config.ColorPolicy.BLACK 
        )
        
        backend = svg.SVGBackend()
        frontend = Frontend(ctx, backend, config=cfg)
        frontend.draw_layout(msp, finalize=True)
        
        page = layout.Page(0, 0, layout.Units.mm)
        settings = layout.Settings(scale=scale_factor, fit_page=False)
        
        svg_string = backend.get_string(page, settings=settings)
        
        clean_svg = re.sub(r'<rect\s+[^>]*/>', '', svg_string)
        background_rect = '<rect width="100%" height="100%" fill="white" />'
        clean_svg = re.sub(r'(<svg[^>]*>)', r'\1' + background_rect, clean_svg)

        st.success("File processed successfully!")

        st.subheader(f"3. Preview SVG File ({unit_selection})")
        
        # FIX: Explicitly using the new width syntax for the preview
        st.image(clean_svg, width="stretch")

        try:
            extents = bbox.extents(msp)
            width_dxf = abs(extents.extmax.x - extents.extmin.x)
            height_dxf = abs(extents.extmax.y - extents.extmin.y)
            
            display_w = width_dxf if unit_selection == "Inches" else width_dxf / 25.4
            display_h = height_dxf if unit_selection == "Inches" else height_dxf / 25.4
            
            st.info(f"**Calculated Size:** {display_w:.3f}\" wide x {display_h:.3f}\" high")
        except:
            pass 

        st.subheader(f"4. Download SVG")
        st.download_button(
            label="Click to Download SVG File",
            data=clean_svg,
            file_name=uploaded_file.name.replace(".dxf", ".svg"),
            mime="image/svg+xml"
        )

    except Exception as e:
        st.error(f"Conversion failed: {e}")
