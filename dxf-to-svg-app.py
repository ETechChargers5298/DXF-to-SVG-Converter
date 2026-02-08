import streamlit as st
import re
import io
import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing import svg, layout, config
from io import BytesIO

# Define team colors (based on typical ETech Chargers colors)
TEAM_BLUE_HEX = "#002060" # Used for primary text/headers
TEAM_GREEN_HEX = "#74B44C" # Used for buttons and success messages
BACKGROUND_COLOR = "#FFFFFF"

# --- Configuration for Logo and Colors ---
st.markdown(f"""
<style>
    /* Change primary color for general text/headers (based on .css-2trqyj from your file) */
    .st-emotion-cache-2trqyj {{
        color: {TEAM_BLUE_HEX};
    }}
    /* Style for buttons (background and border color) */
    .stButton>button {{
        background-color: {TEAM_GREEN_HEX} !important;
        border-color: {TEAM_GREEN_HEX} !important;
        color: white !important;
    }}
    /* Style for the success message background */
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
        # Placeholder for your logo file (e.g., sparky_logo.png)
        st.image("sparky_logo.png", width=100, output_format='PNG')
    except FileNotFoundError:
        # Show a warning if you haven't added the logo file to your directory
        st.warning("Logo file 'sparky_logo.png' not found.")

with col2:
    st.title("Glowforge DXF to SVG")

# Main Description (Not italicized)
st.markdown("Utility to convert .DXF files from OnShape to .SVG files to use with Glowforge Laser Cutter")

# New Italicized Link (Clickable)
st.markdown("*See app code at [github.com/ETechChargers5298/DXF-to-SVG-Converter](https://github.com/ETechChargers5298/DXF-to-SVG-Converter)*")
# --- End of Updated Headings ---


# 1. Units Toggle
unit_selection = st.radio("**1. CHOOSE ORIGINAL DXF UNITS FROM ONSHAPE**", ["Inches", "Millimeters"], horizontal=True)
scale_factor = 25.4 if unit_selection == "Inches" else 1.0

uploaded_file = st.file_uploader("**2. UPLOAD ONSHAPE DXF**", type="dxf")

if uploaded_file is not None:
    try:
        blob = uploaded_file.getvalue()
        doc, auditor = recover.read(BytesIO(blob))
        msp = doc.modelspace()
        
        ctx = RenderContext(doc)
        cfg = config.Configuration(
            background_policy=config.BackgroundPolicy.OFF,
            color_policy=config.ColorPolicy.COLOR
        )
        
        backend = svg.SVGBackend()
        frontend = Frontend(ctx, backend, config=cfg)
        frontend.draw_layout(msp, finalize=True)
        
        # 2. 1:1 Scaling
        page = layout.Page(0, 0, layout.Units.mm)
        settings = layout.Settings(scale=scale_factor, fit_page=False)
        
        # 3. Generate and Clean SVG
        svg_string = backend.get_string(page, settings=settings)
        
        # 4. AGGRESSIVE CLEANUP: Strip the bounding box
        clean_svg = re.sub(r'<rect\s+[^>]*/>', '', svg_string)
        clean_svg = re.sub(r'<rect\s+[^>]*>.*?</rect>', '', clean_svg, flags=re.DOTALL)

        st.subheader(f"Clean Preview ({unit_selection})")
        st.image(clean_svg, use_container_width=True)
        
        st.download_button(
            label="Download Clean 1:1 SVG",
            data=clean_svg,
            file_name=uploaded_file.name.replace(".dxf", ".svg"),
            mime="image/svg+xml"
        )
        
        st.success("File processed successfully!")

    except Exception as e:
        st.error(f"Conversion failed: {e}")

