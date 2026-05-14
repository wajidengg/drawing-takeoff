import streamlit as st
import os
from core.pdf_loader import PDFLoader
from core.render import Renderer
from core.takeoff import Takeoff

# Streamlit page configuration
st.set_page_config(
    page_title="drawing-takeoff",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📐 drawing-takeoff")
st.markdown("PDF-based construction drawing symbol extraction and counting tool.")
st.markdown("---")

# Session state initialization
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = None
if 'detected_symbols' not in st.session_state:
    st.session_state.detected_symbols = []

# Sidebar controls
with st.sidebar:
    st.header("📋 Controls")
    
    # PDF Upload
    uploaded_file = st.file_uploader(
        "Upload a PDF drawing",
        type=["pdf"],
        help="Select a construction drawing PDF file"
    )
    
    if uploaded_file:
        # Save uploaded file temporarily
        pdf_path = f"temp_{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        
        # Load PDF
        pdf_loader = PDFLoader(pdf_path)
        st.session_state.pdf_data = {
            'loader': pdf_loader,
            'path': pdf_path,
            'page_count': pdf_loader.page_count
        }
        st.success(f"✅ PDF loaded: {pdf_loader.page_count} pages")
    
    st.markdown("---")
    
    if st.session_state.pdf_data:
        st.subheader("📄 Page Navigation")
        max_page = st.session_state.pdf_data['page_count'] - 1
        page_num = st.slider(
            "Select page",
            min_value=0,
            max_value=max_page,
            value=st.session_state.current_page,
            step=1
        )
        st.session_state.current_page = page_num
        st.caption(f"Page {page_num + 1} of {st.session_state.pdf_data['page_count']}")
        
        st.markdown("---")
        st.subheader("🔧 Takeoff Settings")
        
        confidence = st.slider(
            "Template matching confidence",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Lower = more matches, Higher = fewer, more confident matches"
        )
        
        min_distance = st.slider(
            "Minimum distance between matches (pixels)",
            min_value=5,
            max_value=100,
            value=30,
            step=5
        )

# Main content area
if st.session_state.pdf_data:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🖼️ Drawing Viewer")
        
        # Render current page
        pdf_loader = st.session_state.pdf_data['loader']
        image = pdf_loader.render_page(st.session_state.current_page)
        
        st.image(image, use_column_width=True, caption=f"Page {st.session_state.current_page + 1}")
    
    with col2:
        st.subheader("📊 Takeoff Summary")
        
        if st.session_state.detected_symbols:
            st.metric(
                "Symbols Detected",
                len(st.session_state.detected_symbols)
            )
            
            # Display detected symbols
            st.markdown("**Detections:**")
            for i, symbol in enumerate(st.session_state.detected_symbols, 1):
                st.caption(f"{i}. Confidence: {symbol['confidence']:.2%}")
        else:
            st.info("👀 No symbols detected yet.\n\nSelect a symbol from the legend to begin.")
        
        if st.button("📥 Export to CSV", use_container_width=True):
            st.success("✅ CSV export functionality coming in Phase 4!")

else:
    st.info("👈 **Start by uploading a PDF** in the sidebar to begin the takeoff workflow.")
    
    st.markdown("---")
    st.subheader("📖 How to use drawing-takeoff")
    
    with st.expander("**Phase 1: PDF Upload & Viewer**"):
        st.markdown("""
        1. **Upload a PDF** - Select a construction drawing
        2. **Navigate pages** - Use the slider to view different pages
        3. **View drawing** - See the rendered drawing in the main area
        """)
    
    with st.expander("**Phase 2: Symbol Selection (Coming Soon)**"):
        st.markdown("""
        1. **Identify legend** - Locate symbol legend on drawing
        2. **Click symbol** - Select a symbol from the legend
        3. **Extract template** - System extracts symbol template
        """)
    
    with st.expander("**Phase 3: Symbol Counting (Coming Soon)**"):
        st.markdown("""
        1. **Template matching** - System finds matching symbols
        2. **Adjust confidence** - Fine-tune detection sensitivity
        3. **Review detections** - Verify found symbols
        """)
    
    with st.expander("**Phase 4: Export Results (Coming Soon)**"):
        st.markdown("""
        1. **Generate report** - Create quantity summary
        2. **Export CSV** - Download results for estimating
        """)

st.markdown("---")
st.caption("🏗️ drawing-takeoff · Experimental PDF-based construction drawing analysis · [GitHub](https://github.com/wajidengg/drawing-takeoff)")
